# FUTUREMIND AI — Explore Tomorrow Before Deciding Today

> AI-powered decision simulation through multi-agent intelligence.

FUTUREMIND AI helps users explore the possible consequences of complex decisions before taking action.

The application transforms a real-world decision into structured future scenarios using three specialist AI agents:

- People Impact Agent
- Operations & Cost Agent
- Risk & Opportunity Agent

The system combines their analysis using Qwen AI to generate best-case, most-likely, and worst-case scenarios with transparent assumptions and recommendations.

FUTUREMIND AI also uses MongoDB Atlas to persist simulation reports and maintain decision history.

---

## 🚀 Live Demo

**Frontend:** https://future-mind-ai.vercel.app

**Backend API:**  https://futuremind-ai-backend.onrender.com

## 📌 Problem

Making complex decisions often involves uncertainty.

Businesses, educational institutions, startups, and organizations must evaluate multiple factors before choosing a course of action.

However, decision-makers often face challenges such as:

- Understanding the impact of a decision on different people.
- Estimating operational costs and resource requirements.
- Identifying potential risks and opportunities.
- Comparing positive and negative outcomes.
- Evaluating long-term consequences.
- Making decisions with incomplete information.

Traditional decision-making approaches may require considerable time, research, and coordination.

FUTUREMIND AI aims to simplify this process through AI-powered scenario analysis.

---

## 💡 Solution

FUTUREMIND AI combines multi-agent intelligence, scenario planning, and persistent data storage to help users evaluate possible future outcomes.

The platform allows users to enter:

- A decision or What-if question.
- Decision category.
- Additional context.
- Time horizon.
- Constraints and requirements.

Three specialist AI agents independently analyze the decision from different perspectives.

A synthesis engine combines their findings and generates structured future scenarios, risk analysis, and recommendations.

The platform supports demo mode for testing and Qwen-powered analysis when API credentials are configured.

---

## ✨ Features

### 1. Decision Simulation

Users can enter different types of real-world decisions using natural language.

Example:

"What if our college introduces a four-day working week?"

Additional context and constraints help the AI agents produce more relevant analysis.

### 2. Multi-Agent Intelligence

FUTUREMIND AI uses three specialist agents.

**People Impact Agent**

Analyzes the potential effects of a decision on people, employees, students, customers, and other stakeholders.

**Operations & Cost Agent**

Evaluates operational requirements, resource allocation, financial implications, and implementation challenges.

**Risk & Opportunity Agent**

Identifies potential threats, uncertainties, opportunities, and possible mitigation strategies.

### 3. Future Scenario Generation

The synthesis engine generates three possible outcomes:

- **Best-case scenario:** A favorable possible outcome.
- **Most-likely scenario:** A plausible outcome based on the supplied assumptions.
- **Worst-case scenario:** Potential challenges and negative consequences.

### 4. Risk Analysis

The platform identifies potential risks and provides recommendations for managing them.

### 5. Final Recommendations

Combines the findings from all three agents into actionable suggestions and decision insights.

### 6. Demo Mode

The application supports demo mode so users can explore the complete simulation workflow without configuring a live Qwen API key.

### 7. Qwen AI Integration

Uses Qwen chat completions through Alibaba Cloud DashScope for AI-powered agent analysis and scenario synthesis.

### 8. Persistent Simulation History

MongoDB Atlas stores previous simulation results so users can retrieve their decision history after refreshing or reopening the application.

### 9. Simulation Retrieval

Users can access previously saved simulations through the history interface and reopen individual reports.

---

## 🏗️ Architecture

FUTUREMIND AI uses a frontend, backend, AI processing, and database architecture.

```text
                  ┌─────────────────────────┐
                  │          USER           │
                  │   Decision & Context    │
                  └────────────┬────────────┘
                               │
                               ▼
                  ┌─────────────────────────┐
                  │      React + Vite       │
                  │      Web Interface     │
                  └────────────┬────────────┘
                               │
                               ▼
                  ┌─────────────────────────┐
                  │      FastAPI Backend    │
                  │     Request Handling    │
                  └────────────┬────────────┘
                               │
                ┌──────────────┴──────────────┐
                │                             │
                ▼                             ▼
       ┌──────────────────┐         ┌──────────────────┐
       │  People Impact   │         │ Operations & Cost│
       │      Agent       │         │      Agent       │
       └────────┬─────────┘         └────────┬─────────┘
                │                             │
                └──────────────┬──────────────┘
                               │
                               ▼
                     ┌──────────────────┐
                     │ Risk & Opportunity│
                     │       Agent       │
                     └────────┬─────────┘
                              │
                              ▼
                     ┌──────────────────┐
                     │   Qwen AI Engine │
                     │ Scenario Synthesis│
                     └────────┬─────────┘
                              │
                              ▼
                     ┌──────────────────┐
                     │ Future Scenarios │
                     │ Recommendations  │
                     └────────┬─────────┘
                              │
                              ▼
                     ┌──────────────────┐
                     │   MongoDB Atlas  │
                     │ Simulation History│
                     └──────────────────┘
```

---

## 🗄️ MongoDB Atlas Database

MongoDB Atlas is used as the cloud-hosted database for storing simulation information.

PyMongo connects the FastAPI backend to MongoDB Atlas.

### Database

`futuremind_ai`

### Collection

#### 1. `simulations`

Stores generated decision simulations.

Important fields include:

- `_id`
- `decision`
- `category`
- `context`
- `time_horizon`
- `constraints`
- `agents`
- `scenarios`
- `recommendation`
- `created_at`

The agent results contain the analysis produced by the three specialist agents.

The scenarios contain best-case, most-likely, and worst-case outcomes.

### Database Workflow

```text
User Decision
     |
     ▼
FastAPI Backend
     |
     ▼
AI Agent Analysis
     |
     ▼
Qwen Scenario Synthesis
     |
     ▼
Simulation Result
     |
     ▼
MongoDB Atlas
     |
     ▼
Persistent Simulation History
```

This allows simulation reports to remain available beyond the current browser session.

---

## 🔄 How the Simulation Workflow Works

When a user starts a simulation:

```text
1. User enters a decision and context
                |
                ▼
2. React sends the request to FastAPI
                |
                ▼
3. Backend processes the simulation request
                |
                ▼
4. Three specialist agents analyze the decision
                |
                ▼
5. Qwen synthesizes their findings
                |
                ▼
6. Best, likely and worst scenarios are generated
                |
                ▼
7. Final recommendations are produced
                |
                ▼
8. Simulation is saved to MongoDB Atlas
                |
                ▼
9. User can retrieve the simulation from history
```

---

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| React 18 | Frontend user interface |
| Vite 6 | Frontend development and build |
| Lucide React | Interface icons |
| Vanilla CSS | Application styling |
| Python 3.10+ | Backend development |
| FastAPI | Backend API framework |
| Uvicorn | ASGI server |
| Pydantic v2 | Request and response validation |
| Qwen AI | Multi-agent analysis and scenario synthesis |
| Alibaba Cloud DashScope | Qwen API access |
| MongoDB Atlas | Persistent simulation storage |
| PyMongo | MongoDB integration |
| Vercel | Frontend deployment |
| Render | Backend deployment |
| GitHub | Source code management |

---

## 📂 Project Structure

```text
FutureMind-AI/
│
├── .gitignore
├── README.md
│
├── backend/
│   ├── .env.example
│   ├── requirements.txt
│   │
│   └── app/
│       ├── __init__.py
│       ├── main.py
│       ├── database.py
│       ├── agents.py
│       ├── qwen_client.py
│       └── schemas.py
│
└── frontend/
    ├── .env.example
    ├── vercel.json
    ├── index.html
    ├── package.json
    ├── package-lock.json
    ├── vite.config.js
    │
    └── src/
        ├── main.jsx
        ├── App.jsx
        └── style.css
```

---

## 🔌 API Reference

The FastAPI backend exposes endpoints for health monitoring, simulation generation, and simulation history.

### 1. `/api/health`

**Method:** GET

Checks backend availability and reports AI and MongoDB connection status.

### 2. `/api/simulate`

**Method:** POST

Processes a decision simulation.

Example request:

```json
{
  "decision": "What if our college introduces a four-day working week?",
  "category": "Education & Academics",
  "context": "A college with 2000 students and 120 faculty members",
  "time_horizon": "6 months",
  "constraints": "Maintain required teaching hours and lab access"
}
```

The response contains agent analysis, future scenarios, and recommendations.

### 3. `/api/simulations`

**Method:** GET

Retrieves previously saved simulations.

Example:

```text
/api/simulations?limit=20
```

### 4. `/api/simulations/{simulation_id}`

**Method:** GET

Retrieves an individual simulation using its database ID.

### API Documentation

After starting the backend, access:

```text
http://127.0.0.1:8000/docs
```

---

## 💻 Getting Started

### Prerequisites

Make sure you have installed:

- Python 3.10 or later
- Node.js and npm
- Git
- MongoDB Atlas account
- Qwen API credentials (optional for demo mode)

### Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/FutureMind-AI.git
```

Move into the project directory:

```bash
cd FutureMind-AI
```

### Backend Setup

Open a terminal:

```bash
cd backend
```

Create a virtual environment:

```bash
py -m venv .venv
```

Activate it on Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

### Environment Variables

Create a `.env` file inside the `backend` folder using `.env.example` as a template.

Configure:

```env
QWEN_API_KEY=your_qwen_api_key
QWEN_BASE_URL=https://dashscope-intl.aliyuncs.com/compatible-mode/v1
QWEN_MODEL=qwen-plus

MONGODB_URI=your_mongodb_atlas_connection_string
MONGODB_DATABASE=futuremind_ai

PORT=8000
FRONTEND_URL=http://localhost:5173
```

Qwen credentials are optional when using the built-in demo mode.

Never commit the actual `.env` file.

### Start the Backend

```bash
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Backend:

```text
http://127.0.0.1:8000
```

API documentation:

```text
http://127.0.0.1:8000/docs
```

### Frontend Setup

Open a second terminal:

```bash
cd frontend
```

Install dependencies:

```bash
npm install
```

Start the frontend:

```bash
npm run dev
```

Open:

```text
http://localhost:5173
```

---

## 🚀 Deployment

FUTUREMIND AI uses separate deployment platforms for the frontend, backend, and database.

### 1. GitHub

The source code is maintained in GitHub.

Push the project:

```bash
git add .
git commit -m "Deploy FutureMind AI"
git push origin main
```

Ensure that `.env`, API keys, and database credentials are excluded through `.gitignore`.

### 2. Backend Deployment — Render

The FastAPI backend is deployed using Render.

Service configuration:

| Setting | Value |
|---|---|
| Runtime | Python 3 |
| Root Directory | `backend` |
| Build Command | `pip install -r requirements.txt` |
| Start Command | `uvicorn app.main:app --host 0.0.0.0 --port $PORT` |

Configure these environment variables in Render:

```env
MONGODB_URI=your_mongodb_atlas_connection_string
MONGODB_DATABASE=futuremind_ai

QWEN_API_KEY=your_qwen_api_key
QWEN_BASE_URL=https://dashscope-intl.aliyuncs.com/compatible-mode/v1
QWEN_MODEL=qwen-plus

FRONTEND_URL=your_vercel_frontend_url
```

After deployment, test:

```text
https://your-backend.onrender.com/api/health
```

### 3. Frontend Deployment — Vercel

The React frontend is deployed through Vercel.

Project configuration:

| Setting | Value |
|---|---|
| Framework | Vite |
| Root Directory | `frontend` |
| Build Command | `npm run build` |
| Output Directory | `dist` |

Add the environment variable:

```env
VITE_API_URL=https://your-backend.onrender.com
```

Deploy the application and copy the generated Vercel URL.

Update `FRONTEND_URL` in Render with the deployed frontend URL to complete the CORS configuration.

### 4. Database Deployment — MongoDB Atlas

MongoDB Atlas provides the hosted database.

Configure:

- Database user with appropriate read/write permissions.
- Network access for the deployed backend.
- MongoDB connection URI in Render environment variables.
- Database name: `futuremind_ai`.

---

## 🔐 Security

FUTUREMIND AI uses environment variables to protect sensitive configuration.

Security practices include:

- MongoDB credentials remain on the backend.
- Qwen API keys are not exposed in frontend code.
- `.env` files are excluded from GitHub.
- Frontend communicates with FastAPI through API endpoints.
- CORS is configured for approved frontend origins.
- Database errors should not expose connection credentials.

---

## 📚 What I Learned

Building FUTUREMIND AI helped me understand:

- Designing a multi-agent AI architecture.
- Integrating Qwen AI using an API.
- Developing REST APIs with FastAPI.
- Building interactive applications using React and Vite.
- Connecting Python applications to MongoDB Atlas.
- Designing persistent simulation storage.
- Managing environment variables and API credentials.
- Building AI-powered scenario analysis workflows.
- Deploying full-stack applications using Vercel and Render.
- Managing project versions and source code using GitHub.

---

## 🔮 Future Improvements

Possible future improvements include:

- Compare multiple decisions side by side.
- Interactive scenario timelines.
- Advanced risk and impact visualizations.
- PDF export of simulation reports.
- User authentication and personalized history.
- Real-world data integration for evidence-based analysis.
- Custom AI agents for different industries.
- Decision tracking and outcome comparison.
- More advanced confidence and uncertainty analysis.

---

## 🔗 Links

### Live Demo

[Add Vercel URL]

### GitHub Repository

[Add GitHub repository URL]

### Backend API

[Add Render URL]

### API Documentation

[Add Render URL]/docs

---

## ⚠️ Disclaimer

FUTUREMIND AI generates possible scenarios based on user-provided information and AI analysis.

These outputs are exploratory decision-support insights, not guaranteed forecasts or substitutes for professional advice. Actual outcomes may differ.

---

## 👩‍💻 Project

**FUTUREMIND AI — Explore Tomorrow Before Deciding Today**

An AI-powered decision-simulation platform combining multi-agent intelligence, scenario planning, and persistent data storage.

If you find this project interesting, feel free to explore the repository and try the live demo.
