import os
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from .schemas import SimulationRequest, SimulationResponse
from .agents import run_simulation, demo_result
from .qwen_client import qwen_is_configured
from .database import (
    check_db_connection,
    save_simulation,
    get_simulation_history,
    get_simulation_by_id,
)

# Standard local development origins
allowed_origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:3000",
    "http://localhost:4173",
    "http://127.0.0.1:4173",
]

# Read FRONTEND_URL from environment (comma-separated or single URL)
frontend_env = os.getenv("FRONTEND_URL", "").strip()
if frontend_env:
    for item in frontend_env.split(","):
        cleaned = item.strip().rstrip("/")
        if cleaned and cleaned not in allowed_origins:
            allowed_origins.append(cleaned)

app = FastAPI(title="FutureMind AI API", version="1.0.0")

# If FRONTEND_URL is set to '*', allow all origins; otherwise allow configured origins + Vercel domains
if "*" in allowed_origins:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
else:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=allowed_origins,
        allow_origin_regex=r"^https:\/\/.*\.vercel\.app$",
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

@app.get("/")
async def root():
    return {
        "message": "FutureMind AI API is running",
        "docs": "/docs",
        "status": "healthy"
    }

@app.get("/api/health")
async def health():
    db_info = check_db_connection()
    return {
        "status": "ok",
        "ai_mode": "qwen" if qwen_is_configured() else "demo",
        "db_status": "connected" if db_info.get("connected") else "disconnected",
        "db_details": {
            "status": db_info.get("status"),
            "database": db_info.get("database"),
            "message": db_info.get("message")
        }
    }

@app.post("/api/simulate")
async def simulate(req: SimulationRequest):
    if not qwen_is_configured():
        result = demo_result(req)
    else:
        try:
            result = await run_simulation(req)
        except Exception as exc:
            # Do not expose credentials or raw provider details to the browser.
            raise HTTPException(status_code=502, detail=(
                "Qwen analysis failed. Check your API key, endpoint, model name and backend terminal."
            )) from exc

    # Prepare document for persistence including all simulation elements
    sim_data = {
        **result,
        "category": req.category,
        "context": req.context,
        "time_horizon": req.time_horizon,
        "constraints": req.constraints,
    }
    saved_id = save_simulation(sim_data)
    result["id"] = saved_id
    result["saved_to_db"] = bool(saved_id)
    result["category"] = req.category
    return result

@app.get("/api/simulations")
async def list_simulations(limit: int = Query(default=50, ge=1, le=100)):
    items = get_simulation_history(limit=limit)
    return {"simulations": items, "total": len(items)}

@app.get("/api/simulations/{simulation_id}")
async def get_single_simulation(simulation_id: str):
    sim = get_simulation_by_id(simulation_id)
    if not sim:
        raise HTTPException(status_code=404, detail="Simulation not found")
    return sim

if __name__ == "__main__":
    import uvicorn
    # Support Render's PORT environment variable with fallback to 8000
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("app.main:app", host="0.0.0.0", port=port, reload=False)
