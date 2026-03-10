from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional
import uvicorn
import json

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
        from graph import build_graph
        graph = build_graph()
        
        # THE FIX: We must pass 'query', not 'raw_query'
        result = await graph.ainvoke({
            "query": q.query,
            "image_bytes": None
        })
        
        # Safely parse the supervisor's JSON verdict
        verdict_str = result.get("final_verdict", "{}")
        try:
            verdict = json.loads(verdict_str)
        except:
            verdict = {}

        grade = verdict.get("investment_grade", "C")
        summary = verdict.get("executive_summary", "Analysis complete.")
        
        # Safely calculate financial outputs
        base_val = result.get("ml_price", 0)
        dld_fee = base_val * 0.04
        commission = base_val * 0.02
        
        # Check if Golden Visa is mentioned in the debate log
        golden_visa = any("Eligible" in str(f) for f in result.get("debate_log", []))
        
        return JSONResponse({
            "grade": grade,
            "baseVal": base_val,
            "adjustedVal": base_val,
            "roi": 6.5,
            "multiplier": result.get("cv_multiplier", 1.0),
            "goldenVisa": golden_visa,
            "dldFee": dld_fee,
            "commission": commission,
            "outOfMarket": result.get("out_of_market", False),
            "summary": summary,
            "topRisk": "Market Volatility",
            "listings": result.get("listings", []),
            "agentLog": result.get("debate_log", [])
        })
    except Exception as e:
        import traceback
        return JSONResponse(
            {"error": str(e), "trace": traceback.format_exc()},
            status_code=500
        )

app.mount("/", StaticFiles(directory="propiq-ui/dist", html=True), name="static")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)