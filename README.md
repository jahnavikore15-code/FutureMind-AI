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

## 🚀Features

Decision Simulation: Enter any decision or What-if question.

People Impact Agent: Analyzes how decisions affect people and stakeholders.

Operations & Cost Agent: Evaluates resources, costs, and operational challenges.

Risk & Opportunity Agent: Identifies possible risks and opportunities.

Scenario Planning: Generates best-case, most-likely, and worst-case outcomes.

AI Recommendations: Provides structured insights to support better decisions.

Simulation History: Saves and retrieves previous simulations using MongoDB Atlas.

Demo Mode: Explore the application even without a Qwen API key.

## Architecture

FUTUREMIND AI uses a frontend, backend, AI processing, and database architecture.

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

## 🛠️ Tech Stack

Technology                      Purpose

React + Vite                    Frontend

Python + FastAPI                Backend

Qwen AI                        AI analysis

MongoDB Atlas                   Database

PyMongo                      Database connection

Vercel                        Frontend deployment

Render                        Backend deployment

## ⚙️ Local Setup

1. Clone the repository

git clone https://github.com/YOUR_USERNAME/FutureMind-AI.git
cd FutureMind-AI

2. Setup the backend

cd backend
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt

Create a .env file using .env.example and configure your Qwen and MongoDB credentials.

Start the backend:

python -m uvicorn app.main:app --reload --port 8000

3. Setup the frontend

Open another terminal:

cd frontend
npm install
npm run dev

Open http://localhost:5173 in your browser.

## 🌐 Deployment

Component                     Platform

Frontend                       Vercel

Backend                        Render

Database                     MongoDB Atlas

Source Code                    GitHub

## 🔐 Security

API keys and database credentials are stored in environment variables.

.env files are excluded from GitHub.

MongoDB credentials are accessible only through the backend.

CORS is configured for the frontend.

## 🔮 Future Enhancements

Interactive scenario visualizations.

PDF report generation.

Decision comparison.

User authentication.

Advanced risk analysis.

## 🔗 Project Links

Live Demo: https://future-mind-ai.vercel.app

GitHub: Add your repository URL.

API Documentation: http://127.0.0.1:8000/docs#/

Medium Article
https://medium.com/@madhurib4555/building-a-lost-found-caller-with-postgresql-and-call-e-7a938885abcf

## 👩‍💻 Author
K.sai jahnavi

B.Tech AIML Student

GitHub:
https://github.com/MadhuriBaja

## ⚠️ Disclaimer

FUTUREMIND AI provides exploratory scenarios and decision-support insights. Its AI-generated outcomes are not guaranteed predictions.

FUTUREMIND AI — Explore Tomorrow Before Deciding Today.

