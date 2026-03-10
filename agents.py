import os
import json
import asyncio
from rag_tool import query_legal, legal_rag_tool
from state import AgentState
from predictor_tool import predict_property_price
from vision_provider import analyze_image 
from tavily_cache import search_comparables
from groq_client import call_groq_with_retry
from typing import Optional

# ==========================================
# AGENT 1: THE QUERY PARSER
# ==========================================
QUERY_PARSER_PROMPT = """
You are an input normalization agent for a UAE real estate intelligence system.
Extract: area, budget_aed, bedrooms, property_type, is_offplan.

CRITICAL GEOGRAPHIC RULE:
- You must preserve the EXACT location the user mentioned.
- Do NOT convert "Ras Al Khaimah" to "Dubai Marina".
- Do NOT convert "Abu Dhabi" to "Downtown".
- If the user mentions another Emirate, KEEP that exact name. The ML engine will handle the mapping.

Convert budget strings to integers ("3M" -> 3000000). Output ONLY valid JSON.
"""

def query_parser_node(state: AgentState) -> dict:
    print("▶️ [Agent 1] Query Parser: Normalizing input...")
    parsed = call_groq_with_retry(prompt=state.query, system=QUERY_PARSER_PROMPT)
    
    # BRUTAL FIX: Intercept 'null' or weird strings from the LLM
    try:
        budget = float(parsed.get("budget_aed") or 0.0)
    except (ValueError, TypeError):
        budget = 0.0
        
    try:
        beds = int(parsed.get("bedrooms") or 1)
    except (ValueError, TypeError):
        beds = 1

    area = parsed.get("area")
    
    return {
        "area": str(area) if area else "Dubai Marina",
        "budget_aed": budget,
        "bedrooms": beds,
        "is_offplan": bool(parsed.get("is_offplan"))
    }

# ==========================================
# AGENT 2: THE CV VISION NODE
# ==========================================
async def cv_vision_node(state: AgentState) -> dict:
    print("▶️ [Agent 2] CV Vision: Scanning property imagery...")
    image_data = state.image_bytes if hasattr(state, 'image_bytes') and state.image_bytes else None
    cv_result = await analyze_image(image_data) # Fixed function name
    multiplier = cv_result.get("premium_multiplier", 1.0)
    log_entry = f"CV Agent: Assigned {multiplier}x premium. Note: {cv_result.get('assessment', '')}"
    return {"cv_multiplier": multiplier, "debate_log": [log_entry]}

# ==========================================
# ==========================================
# AGENT 3: THE FINANCIAL ANALYST
# ==========================================
FINANCIAL_ANALYST_PROMPT = """
You are a Senior Quantitative Real Estate Analyst specializing in the UAE property market.
Calculate the final adjusted price by multiplying the raw ML price by the CV multiplier.
Output ONLY valid JSON in this exact format: {"adjusted_price_aed": <insert_calculated_number_here>, "confidence": 0.85, "analyst_note": "..."}
"""

def financial_analyst_node(state: AgentState) -> dict:
    print(f"▶️ [Agent 3] Financial Analyst: Calculating ML valuations for {state.area}...")
    
    # We pass the flat state variables, NOT state.parsed_query
    ml = predict_property_price(
        location_name = state.area,
        bedrooms      = state.bedrooms,
        sqft          = state.bedrooms * 800,
        is_offplan    = state.is_offplan
    )
    
    raw_price = ml.get("price", 800000.0)
    
    user_msg = f"Raw ML Price: {raw_price}\nCV Multiplier: {state.cv_multiplier}"
    parsed = call_groq_with_retry(prompt=user_msg, system=FINANCIAL_ANALYST_PROMPT)
    
    adjusted_price = parsed.get("adjusted_price_aed", 0)
    if adjusted_price <= 0:
        adjusted_price = raw_price * state.cv_multiplier
        
    log_entry = f"Financial Analyst: Base AED {raw_price:,.2f} | Adjusted AED {adjusted_price:,.2f}."
    if ml.get("out_of_market"):
        log_entry += f" [GEOGRAPHY WARNING TRIGGERED]"
    
    # Return directly mapping to AgentState
    return {
        "ml_price": float(adjusted_price), 
        "out_of_market": ml.get("out_of_market", False),
        "market_warning": ml.get("market_warning", ""),
        "debate_log": [log_entry]
    }

# ==========================================
# ==========================================
# AGENT 4: THE MARKET SCOUT
# ==========================================
MARKET_SCOUT_PROMPT = """
You are a live real estate market intelligence agent for the UAE.
You receive raw scraped listings from Bayut and PropertyFinder via Tavily search.
Compute: median price, price per sqft, days-on-market average. Identify the top 3 comparables.
Output ONLY valid JSON.
"""

def market_scout_node(state: AgentState) -> dict:
    print("▶️ [Agent 4] Market Scout: Analyzing live web listings...")
    
    # THE FIX: Combine the 4 arguments into a single search string for the old Tavily tool
    search_term = f"{state.bedrooms} bedroom property in {state.area} under {state.budget_aed} AED"
    if state.is_offplan:
        search_term += " off-plan"
        
    # Now we pass exactly 1 argument
    raw_listings = search_comparables(search_term)
    
    user_msg = f"Raw Scraped Data:\n{raw_listings}"
    parsed = call_groq_with_retry(prompt=user_msg, system=MARKET_SCOUT_PROMPT)
    median_price = parsed.get("median_price_aed", 0)
    log_entry = f"Market Scout: Scraped Median AED {median_price:,.2f}. Confidence: {parsed.get('confidence', 0.8)}"
    return {"listings": parsed.get("top_comparables", raw_listings), "debate_log": [log_entry]}

# ==========================================
# AGENT 5: THE LEGAL & RISK AGENT
# ==========================================
LEGAL_RISK_PROMPT = """
You are a UAE Real Estate Legal Compliance Officer.
Verify Golden Visa eligibility (threshold: AED 2,000,000 minimum).
Output ONLY valid JSON: {"golden_visa_eligible": true, "compliance_notes": "...", "legal_risks": []}
"""

def legal_risk_node(state: AgentState) -> dict:
    print("▶️ [Agent 5] Legal/Risk: Verifying DLD compliance & Visas...")
    rag_context = query_legal("Golden visa threshold and real estate laws")
    user_msg = f"Property Budget: AED {state.budget_aed}\nIs Offplan: {state.is_offplan}\nRAG Context:\n{rag_context}"
    parsed = call_groq_with_retry(prompt=user_msg, system=LEGAL_RISK_PROMPT)
    visa_status = "Eligible" if parsed.get("golden_visa_eligible") else "Not Eligible"
    log_entry = f"Legal Agent: Golden Visa {visa_status}. Notes: {parsed.get('compliance_notes', '')}"
    return {"legal_flags": parsed.get("legal_risks", []), "debate_log": [log_entry]}
# ==========================================
# ==========================================
# ==========================================
# ==========================================
# AGENT 6: THE SUPERVISOR (UPGRADE 3)
# ==========================================
SUPERVISOR_PROMPT = """
You are the Lead Investment Architect for PropIQ UAE.
Write a 3-sentence executive summary based on the debate log and financial status.
Do NOT assign an investment grade. The system has already assigned the grade deterministically.

Return ONLY valid JSON in this exact structure:
{
  "executive_summary": "..."
}
"""

def supervisor_node(state: AgentState) -> dict:
    print("▶️ [Agent 6] Supervisor: Running deterministic grade logic...")
    
    budget = float(state.budget_aed)
    price = float(state.ml_price)
    
    print(f"🟡 [SUPERVISOR] ml_price={price:,.2f} | budget={budget:,.2f}")
    
    forced_grade = "A"
    
    if budget > 0 and price > 0:
        ratio = price / budget
        print(f"🟡 [SUPERVISOR] price/budget ratio: {ratio:.2f}")
        
        # If price is more than 20% over budget, force a D
        if ratio > 1.20:
            forced_grade = "D"
            print("⚠️ [SUPERVISOR] Severe Deficit. Forcing Grade D.")
        # If price is 5% to 20% over budget, force a C
        elif ratio > 1.05:
            forced_grade = "C"
            print("⚠️ [SUPERVISOR] Slight Deficit. Forcing Grade C.")
            
    # Geographic downgrade
    if state.out_of_market and forced_grade in ["A", "B"]:
        forced_grade = "C"
        print("⚠️ [SUPERVISOR] Out of market query. Downgrading to C.")

    context = f"Budget: {budget} | Price: {price} | Pre-Assigned Grade: {forced_grade}\nLog:\n{state.debate_log}"
    
    # Let LLM write the summary, but NOT pick the grade
    parsed = call_groq_with_retry(prompt=context, system=SUPERVISOR_PROMPT)
    
    # Override the JSON with our Python math grade
    parsed["investment_grade"] = forced_grade
    print(f"🟢 [SUPERVISOR] Final grade locked: {forced_grade}")
    
    return {"final_verdict": json.dumps(parsed)}