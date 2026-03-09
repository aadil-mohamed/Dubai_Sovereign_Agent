# Dubai Sovereign Real Estate Agent (PropIQ)

## 🚀 Live Demo
**Production URL:** `[INSERT RENDER OR STREAMLIT URL HERE]`

## 🏗️ Architecture
- **Frontend:** React + Vite (Custom UI replacing default Streamlit)
- **Backend Graph:** LangGraph (Stateful Multi-Agent Orchestration)
- **Vector Database:** Supabase pgvector (Legal Precedents & RAG)
- **LLM Engine:** Groq (Llama-3.3-70b-versatile) for near-zero latency
- **Vision Models:** Groq LLaVA / GitHub Vision
- **Financial Model:** XGBoost (Local ML mapping)

## 🔒 Environment Setup
Requires `.env` with: `GROQ_API_KEY`, `SUPABASE_URL`, `SUPABASE_ANON_KEY`, `TAVILY_API_KEY`.
