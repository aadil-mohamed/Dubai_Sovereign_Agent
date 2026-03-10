from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import uvicorn
import traceback

app = FastAPI()

# Start empty so the server boots in 0.1 seconds
GRAPH_ENGINE = None

class Query(BaseModel):
    query: str
    image: str = None

@app.post("/api/analyze")
async def analyze(q: Query):
    global GRAPH_ENGINE
    
    try:
        # Lazy load: Only build the brain when the first query comes in
        if GRAPH_ENGINE is None:
            print("IGNITING SOVEREIGN INTELLIGENCE ENGINE...")
            from graph import build_graph 
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
        
    except Exception as e:
        # If ANYTHING fails, catch it and send it to the UI
        error_msg = f"SYSTEM FAILURE: {str(e)}"
        print("CRITICAL PIPELINE ERROR:")
        print(traceback.format_exc())
        
        return {
            "grade": "D",
            "outOfMarket": True,
            "summary": error_msg,
            "baseVal": 0, "adjustedVal": 0, "roi": 0, "multiplier": 1.0,
            "goldenVisa": False, "dldFee": 0, "commission": 0,
            "topRisk": "Backend connection failed. Check Render Logs.",
            "listings": [], 
            "agentLog": [{"agent": "supervisor", "ms": 0, "out": error_msg}]
        }

# Serve React build
app.mount("/", StaticFiles(directory="propiq-ui/dist", html=True), name="static")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
