from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import uvicorn
import asyncio
# PROACTIVE FIX: Pre-import the graph engine
from graph import build_graph 

app = FastAPI()

# Global variable to hold the initialized graph
GRAPH_ENGINE = None

@app.on_event("startup")
async def startup_event():
    global GRAPH_ENGINE
    print("IGNITING SOVEREIGN INTELLIGENCE ENGINE...")
    GRAPH_ENGINE = build_graph()

class Query(BaseModel):
    query: str
    image: str = None

@app.post("/api/analyze")
async def analyze(q: Query):
    global GRAPH_ENGINE
    
    # If for some reason graph isn't built yet, build it
    if GRAPH_ENGINE is None:
        GRAPH_ENGINE = build_graph()
        
    result = await GRAPH_ENGINE.ainvoke({
        "raw_query": q.query,
        "image_bytes": None
    })
    
    return {
        "grade": result["supervisor_result"]["investment_grade"],
        "baseVal": result["ml_result"]["base_price_aed"],
        "adjustedVal": result["financial_result"]["adjusted_price_aed"],
        "roi": result["financial_result"]["roi_percent"],
        "multiplier": result["vision_result"]["multiplier"],
        "goldenVisa": result["legal_result"]["golden_visa_eligible"],
        "dldFee": result["legal_result"]["dld_fee_aed"],
        "commission": result["legal_result"]["commission_aed"],
        "outOfMarket": result.get("out_of_market", False),
        "summary": result["supervisor_result"]["executive_summary"],
        "topRisk": result["supervisor_result"]["top_risk"],
        "listings": result["market_result"]["comparables"],
        "agentLog": result.get("agent_log", [])
    }

# Serve React build
app.mount("/", StaticFiles(directory="propiq-ui/dist", html=True), name="static")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)