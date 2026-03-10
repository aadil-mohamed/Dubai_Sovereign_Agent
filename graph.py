import os
import json
import asyncio
from langgraph.graph import StateGraph, END
from langchain_core.messages import SystemMessage, HumanMessage

# Import our Pydantic State
from state import AgentState

# THE FIX: Import ALL 6 agents from agents.py, including the real supervisor!
from agents import (
    query_parser_node, cv_vision_node, financial_analyst_node,
    market_scout_node, legal_risk_node, supervisor_node
)

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
    builder.add_node("supervisor", supervisor_node) # Using the real deterministic node
    
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