import os
import re
import logging
from datetime import datetime, timezone
from typing import Optional, Any
from pathlib import Path
from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, PyMongoError
from bson import ObjectId
from bson.errors import InvalidId

_env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=_env_path)
load_dotenv()

logger = logging.getLogger("futuremind.database")

_mongo_client: Optional[MongoClient] = None
_last_uri: Optional[str] = None

def sanitize_error(err: Any) -> str:
    """Strips credentials or passwords from error strings so secrets are never logged or exposed."""
    s = str(err)
    return re.sub(r":([^@/\s]+)@", ":****@", s)

def reload_env():
    """Reloads environment variables from backend/.env."""
    load_dotenv(dotenv_path=_env_path, override=True)

def get_mongo_uri() -> str:
    reload_env()
    return os.getenv("MONGODB_URI", "").strip()

def get_database_name() -> str:
    reload_env()
    return os.getenv("MONGODB_DATABASE", "futuremind_ai").strip() or "futuremind_ai"

def has_password_placeholder(uri: str) -> bool:
    """Checks whether the URI contains unreplaced placeholder tokens or angle brackets."""
    if not uri:
        return False
    if "<db_password>" in uri or "<password>" in uri or "<username>" in uri:
        return True
    # Matches patterns like :<anything>@
    if re.search(r":<[^>]+>@", uri):
        return True
    return False

def is_db_configured() -> bool:
    uri = get_mongo_uri()
    return bool(uri and not has_password_placeholder(uri))

def get_mongo_client() -> Optional[MongoClient]:
    global _mongo_client, _last_uri
    uri = get_mongo_uri()

    if not is_db_configured():
        if _mongo_client is not None:
            try:
                _mongo_client.close()
            except Exception:
                pass
            _mongo_client = None
            _last_uri = None
        return None

    # Reconnect if URI has been changed in .env
    if _mongo_client is None or uri != _last_uri:
        if _mongo_client is not None:
            try:
                _mongo_client.close()
            except Exception:
                pass
        try:
            # Set short timeout so neither server startup nor health checks block
            _mongo_client = MongoClient(
                uri,
                serverSelectionTimeoutMS=4000,
                connectTimeoutMS=4000,
                socketTimeoutMS=5000,
                appname="FutureMindAI"
            )
            _last_uri = uri
        except Exception as e:
            logger.error(f"Failed to create MongoClient: {sanitize_error(e)}")
            _mongo_client = None
            _last_uri = None

    return _mongo_client

def check_db_connection() -> dict[str, Any]:
    """Tests connection to MongoDB Atlas and returns status details without exposing credentials."""
    reload_env()
    uri = get_mongo_uri()
    db_name = get_database_name()

    if not uri:
        return {
            "connected": False,
            "status": "not_configured",
            "message": "MONGODB_URI is not set in backend/.env",
            "database": db_name
        }

    if has_password_placeholder(uri):
        return {
            "connected": False,
            "status": "placeholder_credentials",
            "message": "Password placeholder found in MONGODB_URI. In backend/.env, replace <db_password> (including the angle brackets < >) with your actual MongoDB Atlas database user password.",
            "database": db_name
        }

    client = get_mongo_client()
    if client is None:
        return {
            "connected": False,
            "status": "client_error",
            "message": "Could not initialize MongoDB client. Please verify the connection string in backend/.env.",
            "database": db_name
        }

    try:
        # Ping admin database with 4s timeout
        client.admin.command("ping")
        return {
            "connected": True,
            "status": "connected",
            "database": db_name,
            "message": f"Successfully connected to MongoDB Atlas database '{db_name}'."
        }
    except (ConnectionFailure, PyMongoError) as err:
        err_msg = sanitize_error(err)
        logger.warning(f"MongoDB connection check failed: {err_msg}")
        return {
            "connected": False,
            "status": "connection_failed",
            "message": f"Could not connect to MongoDB Atlas. Ensure your password is correct and your IP address is allowed in Atlas Network Access (e.g. 0.0.0.0/0). Error: {err_msg}",
            "database": db_name
        }
    except Exception as err:
        err_msg = sanitize_error(err)
        logger.warning(f"Unexpected MongoDB check error: {err_msg}")
        return {
            "connected": False,
            "status": "error",
            "message": f"Error: {err_msg}",
            "database": db_name
        }

def get_simulations_collection():
    """Returns the 'simulations' collection if MongoDB is accessible."""
    client = get_mongo_client()
    if client is None:
        return None
    try:
        db = client[get_database_name()]
        return db["simulations"]
    except Exception as e:
        logger.error(f"Error accessing simulations collection: {sanitize_error(e)}")
        return None

def serialize_simulation(doc: dict) -> dict:
    """Formats a MongoDB simulation document for JSON response."""
    if not doc:
        return {}
    res = dict(doc)
    if "_id" in res:
        res["id"] = str(res.pop("_id"))
    # Ensure created_at is an ISO string
    if isinstance(res.get("created_at"), datetime):
        res["created_at"] = res["created_at"].isoformat()
    return res

def save_simulation(data: dict) -> Optional[str]:
    """
    Saves a completed simulation into MongoDB Atlas 'simulations' collection.
    Includes question, category, agent analysis, scenarios, recommendations, and metadata.
    """
    collection = get_simulations_collection()
    if collection is None:
        return None

    try:
        # Extract primary recommendation
        recs = data.get("recommendations", [])
        final_rec = recs[0] if recs else "Proceed with measured steps and checkpoints."

        document = {
            # User question / decision
            "question": data.get("decision", ""),
            "decision": data.get("decision", ""),
            "category": data.get("category", "General"),
            "context": data.get("context", ""),
            "time_horizon": data.get("time_horizon", "6 months"),
            "constraints": data.get("constraints", ""),
            # Specialist agent analysis
            "agent_analysis": data.get("agent_insights", []),
            "agent_insights": data.get("agent_insights", []),
            # Scenarios
            "scenarios": data.get("scenarios", []),
            # Recommendations
            "final_recommendation": final_rec,
            "recommendations": recs,
            "key_assumptions": data.get("key_assumptions", []),
            "confidence": data.get("confidence", ""),
            # Metadata
            "mode": data.get("mode", "demo"),
            "disclaimer": data.get("disclaimer", ""),
            "created_at": datetime.now(timezone.utc).isoformat()
        }

        result = collection.insert_one(document)
        return str(result.inserted_id)
    except Exception as e:
        logger.error(f"Failed to save simulation to MongoDB: {sanitize_error(e)}")
        return None

def get_simulation_history(limit: int = 50) -> list[dict]:
    """Retrieves recent simulations from the database."""
    collection = get_simulations_collection()
    if collection is None:
        return []

    try:
        # Fetch recent simulations sorted by creation time
        cursor = collection.find().sort("created_at", -1).limit(limit)
        return [serialize_simulation(doc) for doc in cursor]
    except Exception as e:
        logger.error(f"Failed to retrieve simulation history: {sanitize_error(e)}")
        return []

def get_simulation_by_id(simulation_id: str) -> Optional[dict]:
    """Fetches a specific simulation by its string ID."""
    collection = get_simulations_collection()
    if collection is None:
        return None

    try:
        obj_id = ObjectId(simulation_id)
        doc = collection.find_one({"_id": obj_id})
        return serialize_simulation(doc) if doc else None
    except (InvalidId, PyMongoError, Exception) as e:
        logger.error(f"Failed to fetch simulation by id {simulation_id}: {sanitize_error(e)}")
        return None
