import streamlit as st
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.agents import initialize_agent, AgentType
from langchain.tools import StructuredTool, Tool

# --- ARCHITECTURE CORE: SECURE API LOADING ---
# This automatically finds your .env file and loads the key invisibly
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

# --- ARCHITECTURE CORE: IMPORTING YOUR ARSENAL ---
from predictor_tool import predict_property_price
from rag_tool import search_dubai_laws

# --- UI/UX MASTERY: PAGE CONFIGURATION & CSS ---
st.set_page_config(page_title="Dubai Sovereign Intelligence", page_icon="🏙️", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0b0f19; color: #e2e8f0; }
    [data-testid="stSidebar"] { background: rgba(15, 23, 42, 0.8) !important; border-right: 1px solid rgba(212, 175, 55, 0.2); }
    h1, h2, h3 { color: #d4af37 !important; font-family: 'Helvetica Neue', sans-serif; font-weight: 300; }
    .stTextInput>div>div>input { background-color: #1e293b; color: #d4af37; border: 1px solid rgba(212, 175, 55, 0.5); border-radius: 8px; }
    .stButton>button { background: linear-gradient(90deg, #d4af37 0%, #b8860b 100%); color: #000000; font-weight: bold; border-radius: 8px; }
    </style>
""", unsafe_allow_html=True)

# --- SYSTEM INITIALIZATION ---
st.title("🏙️ Sovereign Intelligence Matrix")
st.markdown("*Autonomous Property, Market Forecasting & Legal Engine*")

# --- THE NEURAL LINK: MULTI-TOOL ORCHESTRATION ---
if api_key:
    # 1. Initialize the Cloud Brain (Using the upgraded Llama 3.3 model)
    llm = ChatGroq(model_name="llama-3.3-70b-versatile", temperature=0.1)

    # 2. Tool 1: The ML Predictor
    ml_tool = StructuredTool.from_function(
        func=predict_property_price,
        name="Dubai_Price_Predictor",
        description="ALWAYS use this tool when a user asks for a property price prediction, estimate, or valuation in Dubai. You must extract and pass: location_name (str), bedrooms (int), sqft (float). If sqft is missing, assume 1000. If location is missing, assume 'Marina'."
    )
    
    # 3. Tool 2: The RAG Legal Memory
    rag_tool = Tool(
        name="Dubai_Law_Database",
        func=search_dubai_laws,
        description="ALWAYS use this tool when a user asks about Dubai real estate laws, Golden Visa, visas, escrow accounts, D33 agenda, or rental caps."
    )
    
    # 4. Create the Ultimate Agent with BOTH tools
    agent = initialize_agent(
        tools=[ml_tool, rag_tool],
        llm=llm,
        agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
        handle_parsing_errors=True,
        verbose=True
    )
    st.sidebar.success("Neural Link, ML Predictor & RAG Memory Fully Synced & Secured.")
else:
    st.sidebar.error("CRITICAL: API Key not found. Please ensure your .env file is configured correctly.")

# --- UI/UX MASTERY: THE ARCHITECT CREDENTIAL ---
st.sidebar.markdown("<br><br>", unsafe_allow_html=True)
st.sidebar.markdown("""
    <div style='background-color: #1e293b; padding: 15px; border-radius: 8px; border-left: 3px solid #d4af37; box-shadow: 0 4px 6px rgba(0,0,0,0.3);'>
        <p style='color: #94a3b8; font-size: 0.75rem; font-weight: 600; margin-bottom: 2px; letter-spacing: 1px;'>LEAD SYSTEM ARCHITECT</p>
        <p style='color: #d4af37; font-size: 1.1rem; font-weight: bold; margin-bottom: 2px;'>Aadil Mohamed</p>
        <p style='color: #e2e8f0; font-size: 0.80rem; margin-bottom: 4px;'>B.Tech AI & Data Science</p>
        <p style='color: #64748b; font-size: 0.70rem; margin-bottom: 0px;'>Class of 2026</p>
    </div>
""", unsafe_allow_html=True)

# --- THE INTERFACE LOOP ---
query = st.text_input("Enter Market Query, Prediction Request, or Legal Question:")

if st.button("Initialize Analysis"):
    if not api_key:
        st.error("System Offline. Missing Authorization.")
    elif query:
        with st.spinner("Agent is reasoning across ML models and Legal databases..."):
            try:
                response = agent.run(query)
                st.markdown("### 📊 Sovereign Output")
                st.success(response)
            except Exception as e:
                st.error(f"System Fault: {e}")