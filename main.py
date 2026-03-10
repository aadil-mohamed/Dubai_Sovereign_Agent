from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional
import uvicorn

app = FastAPI()

class Query(BaseModel):
    query: str
    image: Optional[str] = None

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.post("/api/analyze")
async def analyze(q: Query):
    try:
        from agents import build_graph
        graph = build_graph()
        result = graph.invoke({
            "raw_query": q.query,
            "image_bytes": None
        })
        return JSONResponse({
            "grade": result["supervisor_result"].get("investment_grade","C"),
            "baseVal": result["ml_result"].get("base_price_aed", 0),
            "adjustedVal": result["financial_result"].get("adjusted_price_aed", 0),
            "roi": result["financial_result"].get("roi_percent", 0),
            "multiplier": result["vision_result"].get("multiplier", 1.0),
            "goldenVisa": result["legal_result"].get("golden_visa_eligible", False),
            "dldFee": result["legal_result"].get("dld_fee_aed", 0),
            "commission": result["legal_result"].get("commission_aed", 0),
            "outOfMarket": result.get("out_of_market", False),
            "summary": result["supervisor_result"].get("executive_summary",""),
            "topRisk": result["supervisor_result"].get("top_risk",""),
            "listings": result["market_result"].get("comparables", []),
            "agentLog": result.get("agent_log", [])
        })
    except Exception as e:
        import traceback
        return JSONResponse(
            {"error": str(e), "trace": traceback.format_exc()},
            status_code=500
        )

# StaticFiles MUST be mounted LAST
# This is the fix — it was intercepting /api/analyze
app.mount("/", StaticFiles(directory="propiq-ui/dist", html=True), name="static")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)