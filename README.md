# FUTUREMIND AI — Explore Tomorrow Before Deciding Today

A decision-simulation intelligence platform powered by FastAPI, React, Qwen AI, and MongoDB Atlas. Enter any complex decision, let three specialist AI agents analyze different perspectives (People Impact, Operations & Cost, Risk & Opportunity), and explore synthesized best-case, most-likely, and worst-case scenarios with transparent assumptions and recommendations.

---

## Tech Stack & Architecture

- **Frontend**: React 18, Vite 6, Lucide React, vanilla CSS (Dark Cyber/Space theme).
- **Backend**: Python 3.10+, FastAPI, Uvicorn, Pydantic v2.
- **AI Engine**: Qwen chat completions via Alibaba Cloud DashScope (with built-in fallback demo mode).
- **Database**: MongoDB Atlas (via PyMongo) for persistent simulation history and audit trail.
- **Deployment**:
  - Frontend on **Vercel**
  - Backend on **Render**
  - Database on **MongoDB Atlas**

---

## Project Structure

```text
FutureMind-AI/
├── .gitignore               # Excludes .env, .venv, node_modules, dist, etc.
├── README.md                # Full documentation & deployment guide
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py          # FastAPI application, CORS, and API routing
│   │   ├── database.py      # MongoDB Atlas client, ping test, and history operations
│   │   ├── agents.py        # 3 specialist agents + scenario synthesis logic
│   │   ├── qwen_client.py   # Async Qwen / DashScope API integration
│   │   └── schemas.py       # Pydantic request & response data models
│   ├── .env.example         # Template for backend secrets
│   └── requirements.txt     # Python dependencies
└── frontend/
    ├── .env.example         # Template for frontend environment variables
    ├── vercel.json          # Vercel SPA rewrite configuration
    ├── index.html
    ├── package.json
    ├── vite.config.js
    └── src/
        ├── main.jsx
        ├── App.jsx          # Studio UI, history drawer, and scenario viewer
        └── style.css        # Full styling
```

---

## 1. Local Development Setup

### Backend Setup (PowerShell on Windows)

```powershell
cd backend
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt

# Create .env from example
Copy-Item .env.example .env
```

Open `backend/.env` and configure your credentials:
```env
# Optional: Set your Qwen API key for live AI simulation (leave empty for demo mode)
QWEN_API_KEY=your_qwen_api_key
QWEN_BASE_URL=https://dashscope-intl.aliyuncs.com/compatible-mode/v1
QWEN_MODEL=qwen-plus

# MongoDB Atlas connection (replace <db_password> with your actual password)
MONGODB_URI=mongodb+srv://<username>:<password>@cluster0.example.mongodb.net/
MONGODB_DATABASE=futuremind_ai

# Server configuration
PORT=8000
FRONTEND_URL=http://localhost:5173
```

Start the backend:
```powershell
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```
- API Docs: `http://127.0.0.1:8000/docs`
- Health Check: `http://127.0.0.1:8000/api/health`

### Frontend Setup

In a new terminal:
```powershell
cd frontend
npm install
npm run dev
```
Open `http://localhost:5173` in your browser.

---

## 2. GitHub Preparation

The root `.gitignore` is pre-configured to ensure no secrets or environment files are ever tracked.

1. Initialize Git and stage your files:
```powershell
git init
git add .
git status
```
> **Security Check**: Verify that `backend/.env` or any file containing passwords is **NOT** listed under `Changes to be committed`.

2. Commit and push to your GitHub repository:
```powershell
git commit -m "feat: complete FutureMind AI platform with MongoDB Atlas and deployment configuration"
git branch -M main
git remote add origin https://github.com/<your-username>/<your-repo-name>.git
git push -u origin main
```

---

## 3. MongoDB Atlas Configuration

1. In [MongoDB Atlas](https://cloud.mongodb.com/):
   - **Database Access**: Create a database user (e.g. `futuremind_user`) with read/write access. Keep note of the password.
   - **Network Access**: Add an IP access rule:
     - Click **Add IP Address** -> Select **Allow Access From Anywhere (`0.0.0.0/0`)** so cloud platforms like Render can connect.
   - **Connection String**: Go to Database -> **Connect** -> **Drivers** (Python). Copy the connection string.
2. In your connection string, substitute `<password>` with your database user password (remove the `< >` brackets).

---

## 4. Deploying the Backend to Render

1. Log in to [Render](https://render.com/) and click **New +** -> **Web Service**.
2. Connect your GitHub repository.
3. Configure service settings:
   - **Name**: `futuremind-ai-backend`
   - **Region**: Choose the closest region to you (e.g., Singapore, Frankfurt, Oregon)
   - **Root Directory**: `backend`
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
4. In the **Environment Variables** section, add:
   - `MONGODB_URI`: Your MongoDB Atlas connection URI (e.g. `mongodb+srv://user:pass@cluster0.xxx.mongodb.net/`)
   - `MONGODB_DATABASE`: `futuremind_ai`
   - `QWEN_API_KEY`: Your Qwen API key (optional for live AI mode)
   - `QWEN_BASE_URL`: `https://dashscope-intl.aliyuncs.com/compatible-mode/v1`
   - `QWEN_MODEL`: `qwen-plus`
   - `FRONTEND_URL`: URL of your deployed frontend (e.g. `https://futuremind-ai.vercel.app`), or leave empty initially and update after Vercel deployment.
5. Click **Create Web Service**.
6. Once deployed, copy your Render service URL: `https://<service-name>.onrender.com`. Test it by opening `https://<service-name>.onrender.com/api/health` in your browser.

---

## 5. Deploying the Frontend to Vercel

1. Log in to [Vercel](https://vercel.com/) and click **Add New...** -> **Project**.
2. Select your GitHub repository.
3. In the project configuration:
   - **Framework Preset**: `Vite`
   - **Root Directory**: Click edit and select `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`
4. Under **Environment Variables**, add:
   - `VITE_API_URL`: Your deployed Render backend URL (e.g. `https://futuremind-ai-backend.onrender.com`)
5. Click **Deploy**.
6. When Vercel deployment finishes, copy your frontend URL (e.g. `https://futuremind-ai.vercel.app`).
7. *(Optional)* Return to your Render backend dashboard -> **Environment Variables** -> update `FRONTEND_URL` to your Vercel URL to complete the CORS whitelist.

---

## 6. API Reference

### Health Check
`GET /api/health`
Returns connection statuses for the AI engine and MongoDB Atlas:
```json
{
  "status": "ok",
  "ai_mode": "qwen",
  "db_status": "connected",
  "db_details": {
    "status": "connected",
    "database": "futuremind_ai",
    "message": "Successfully connected to MongoDB Atlas database 'futuremind_ai'."
  }
}
```

### Run Simulation
`POST /api/simulate`
```json
{
  "decision": "What if our college introduces a four-day working week?",
  "category": "Education & Academics",
  "context": "A college with 2,000 students and 120 faculty members",
  "time_horizon": "6 months",
  "constraints": "Maintain required teaching hours and lab access"
}
```

### History Endpoints
- `GET /api/simulations?limit=20`: List saved simulation history.
- `GET /api/simulations/{simulation_id}`: Retrieve a specific saved simulation.

---

## 7. Security Best Practices

- Never commit `.env` or paste database passwords into client-side files.
- MongoDB credentials and Qwen keys remain exclusively on the FastAPI backend server.
- The root `.gitignore` enforces strict ignoring of sensitive environment files and build outputs.
