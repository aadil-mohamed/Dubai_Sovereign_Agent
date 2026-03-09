import os
import json
import asyncio
from langgraph.graph import StateGraph, END
from langchain_core.messages import SystemMessage, HumanMessage

# Import our Pydantic State
from state import AgentState

# Import our 5 base agents (Notice: 'llm' is completely removed)
from agents import (
    query_parser_node, cv_vision_node, financial_analyst_node,
    market_scout_node, legal_risk_node
)

# Import the secure Tenacity hub for the Supervisor
from groq_client import call_groq_with_retry

# ==========================================
# AGENT 6: THE SUPERVISOR
# ==========================================
SUPERVISOR_PROMPT = """
You are the Chief Investment Intelligence Officer at PropIQ UAE.
You receive the shared debate log from 4 specialist agents.
Synthesize all agent outputs into ONE final investment verdict.

Output ONLY valid JSON using EXACTLY this format:
{
  "investment_grade": "A",
  "executive_summary": "Your 3-sentence executive summary goes here..."
}
"""

def supervisor_node(state: AgentState) -> dict:
    print("▶️ [Agent 6] Supervisor: Synthesizing final investment verdict...")
    debate_context = "\n".join(state.debate_log)
    user_msg = f"Property: {state.bedrooms} Bed in {state.area}\nBudget: AED {state.budget_aed}\n\nAgent Debate Log:\n{debate_context}"
    
    # CRITICAL FIX 4: The Supervisor now uses the Tenacity-backed secure hub
    parsed = call_groq_with_retry(prompt=user_msg, system=SUPERVISOR_PROMPT)
    
    # Graceful fallback in case of JSON parse failure
    if not isinstance(parsed, dict):
        parsed = {"investment_grade": "N/A", "executive_summary": "Error parsing agent logic."}
        
    log_entry = f"Supervisor Verdict: Grade {parsed.get('investment_grade', 'N/A')}. {parsed.get('executive_summary', '')}"
    
    return {
        "final_verdict": json.dumps(parsed),
        "debate_log": [log_entry]
    }

# ==========================================
# LANGGRAPH COMPILATION (SEQUENTIAL STABILITY)
# ==========================================
def build_graph():
    print("⚙️ Compiling LangGraph Directed Acyclic Graph (DAG)...")
    builder = StateGraph(AgentState)
    
    # 1. Add all Nodes (The Brains)
    builder.add_node("parser", query_parser_node)
    builder.add_node("cv_vision", cv_vision_node)
    builder.add_node("financial", financial_analyst_node)
    builder.add_node("scout", market_scout_node)
    builder.add_node("legal", legal_risk_node)
    builder.add_node("supervisor", supervisor_node)
    
    # 2. Define the Routing (Sequential for absolute stability)
    builder.set_entry_point("parser")
    builder.add_edge("parser", "cv_vision")
    builder.add_edge("cv_vision", "financial")
    builder.add_edge("financial", "scout")
    builder.add_edge("scout", "legal")
    builder.add_edge("legal", "supervisor")
    builder.add_edge("supervisor", END)
    
    return builder.compile()

# Create the executable graph instance
propiq_graph = build_graph()