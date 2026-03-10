# PropIQ UAE — Sovereign Investment Intelligence

> **6-agent LangGraph AI system for Dubai real estate valuation.**  
> Live demo: [propiq-uae.onrender.com](https://propiq-uae.onrender.com)

---

## What This Is

PropIQ UAE is a production multi-agent AI pipeline that delivers an institutional-grade investment verdict on any Dubai property query in under 10 seconds.

A broker types: *"2BR apartment Dubai Marina under AED 2.5M off-plan"*  
PropIQ returns: a deterministic investment grade (A/B/C/D), a live-computed valuation, ROI projection, Golden Visa eligibility, legal cost breakdown, and three live comparable listings — all in one cinematic React UI.

This is not a demo. It is a deployed, revenue-generating system.

---

## Architecture

```
User Query (Natural Language)
        │
        ▼
┌─────────────────────────────────────────────────────────┐
│                  LangGraph DAG (6 Agents)                │
│                                                         │
│  01 Query Parser ──► 02 GPT-4o Vision                   │
│       │                     │                           │
│       ▼                     ▼                           │
│  03 XGBoost Engine ──► 04 Market Scout                  │
│       │                     │                           │
│       ▼                     ▼                           │
│  05 Legal / Risk ───► 06 Supervisor AI                  │
│                             │                           │
│                    Deterministic Grade Override          │
└─────────────────────────────────────────────────────────┘
        │
        ▼
FastAPI /api/analyze endpoint
        │
        ▼
React v4 Cinematic UI
```

### Agent Responsibilities

| Agent | Model | Purpose |
|---|---|---|
| Query Parser | Groq LLaMA-3.3-70B | NLP → strict Pydantic JSON |
| GPT-4o Vision | GitHub Models GPT-4o | Luxury multiplier from property image |
| XGBoost Engine | XGBoost (10K DLD records) | Base price prediction |
| Market Scout | Tavily API | Live Bayut + PropertyFinder scraping |
| Legal / Risk | Supabase pgvector RAG | Golden Visa, DLD fee, risk flags |
| Supervisor AI | Groq LLaMA-3.3-70B | Executive synthesis + grade override |

### Deterministic Override Logic

The Supervisor does not rely solely on LLM optimism bias. A hard Python rule enforces:

```python
if ml_price > budget * 1.20:
    grade = "D"  # Override regardless of LLM output
```

This is the core research contribution: **deterministic guardrails on top of probabilistic LLM output.**

---

## Tech Stack

```
Backend      FastAPI + Uvicorn
AI Pipeline  LangGraph (stateful DAG)
LLM          Groq LLaMA-3.3-70B (free tier)
Vision       GPT-4o via GitHub Models (free tier)
ML Model     XGBoost trained on 10,000 Dubai DLD records
Vector DB    Supabase pgvector (legal RAG)
Live Data    Tavily API (real-time property scraping)
PDF Export   ReportLab institutional dossier
Frontend     React 18 + Vite
Deployment   Render.com (Docker) + Cloudflare DNS
Domain       propiqae.com
```

---

## Key Engineering Decisions

**Why LangGraph over a simple chain?**  
Each agent writes to a shared `AgentState` Pydantic object. Downstream agents read upstream outputs directly. This eliminates prompt chaining fragility and makes the pipeline deterministic and testable node by node.

**Why Groq over OpenAI?**  
Free tier with 30 req/min on LLaMA-3.3-70B. For a broker demo system where queries are sequential, this removes infrastructure cost entirely at early stage.

**Why XGBoost over a neural model?**  
10,000 DLD records is insufficient for a neural network. XGBoost handles tabular real estate data with high accuracy at this data volume, runs in under 100ms, and is fully explainable — critical for a financial product.

**Why the AED 800K price floor?**  
DLD data contains registration errors below this threshold. The floor prevents the model from outputting non-credible valuations that would destroy broker trust.

**Why FastAPI instead of Streamlit alone?**  
Streamlit cannot serve a compiled React build. FastAPI mounts the React `dist/` as static files and exposes the Python pipeline as a POST endpoint. One Docker container. One URL. No architectural split.

---

## Local Development

```bash
# Clone
git clone https://github.com/[username]/propiq-uae.git
cd propiq-uae

# Python backend
pip install -r requirements.txt
cp .env.example .env  # fill in your keys

# React frontend
cd propiq-ui
npm install
npm run build
cd ..

# Run
uvicorn main:app --reload --port 8000
# Visit http://localhost:8000
```

### Required Environment Variables

```
GROQ_API_KEY=
GITHUB_TOKEN=
SUPABASE_URL=
SUPABASE_ANON_KEY=
SUPABASE_DB_URL=
TAVILY_API_KEY=
VISION_PROVIDER=github
```

---

## Project Structure

```
propiq-uae/
├── main.py              # FastAPI server + static mount
├── agents.py            # LangGraph DAG (6 nodes)
├── predictor_tool.py    # XGBoost inference + OOD detection
├── vector_store.py      # Supabase pgvector legal RAG
├── vision_provider.py   # GPT-4o / Groq vision abstraction
├── requirements.txt     # Pinned dependencies
├── Dockerfile           # Production container
├── render.yaml          # Render.com config
└── propiq-ui/
    ├── src/
    │   └── PropIQ.jsx   # React v4 cinematic UI
    ├── dist/            # Compiled production build
    └── package.json
```

---

## Live System

| Endpoint | Purpose |
|---|---|
| `GET /` | Cinematic React UI |
| `POST /api/analyze` | LangGraph pipeline |
| `GET /health` | Uptime check |

**Production URL:** [propiq-uae.onrender.com](https://propiq-uae.onrender.com)

---

## Roadmap

- [ ] Stripe integration (AED 499/month broker subscription)
- [ ] PDF dossier email delivery
- [ ] Off-plan project database (RERA registry scraper)
- [ ] Arabic language query support
- [ ] Mobile-optimised UI

---

## About

Built by **Aadil** — B.Tech AI & Data Science, Anna University (2025).  
Final-year portfolio project demonstrating production multi-agent systems on real UAE economic data.

> *"The grade is not generated. It is computed, verified, and enforced."*

---

## License

MIT — use freely, attribute clearly.
