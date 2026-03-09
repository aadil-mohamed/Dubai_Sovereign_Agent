import streamlit as st
import asyncio
import json
import os
import hashlib
import inspect

from graph import build_graph
from pdf_tool import generate_investment_dossier
from analytics_tool import get_live_stats, log_feedback
import agents

# --- UI/UX MASTERY: PAGE CONFIGURATION & CSS ---
st.set_page_config(page_title="PropIQ UAE", page_icon="🏙️", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0b0f19; color: #e2e8f0; }
    [data-testid="stSidebar"] { background: rgba(15, 23, 42, 0.8) !important; border-right: 1px solid rgba(212, 175, 55, 0.2); }
    h1, h2, h3 { color: #d4af37 !important; font-family: 'Helvetica Neue', sans-serif; font-weight: 700; }
    .stButton>button { background: linear-gradient(90deg, #d4af37 0%, #b8860b 100%); color: #000000; font-weight: bold; border-radius: 8px; border: none; }
    .stTextInput>div>div>input { background-color: #1e293b; color: #d4af37; border: 1px solid rgba(212, 175, 55, 0.5); }
    div[data-testid="stFileUploader"] { background-color: #1e293b; border-radius: 8px; padding: 10px; border: 1px dashed #d4af37; }
    </style>
""", unsafe_allow_html=True)

# --- LANGGRAPH SESSION ISOLATION ---
def get_graph_version() -> str:
    source = inspect.getsource(agents)
    return hashlib.md5(source.encode()).hexdigest()[:8]

def init_session():
    current_version = get_graph_version()
    # ADD THIS
    # Force graph rebuild every single run to kill the cache bug
    st.session_state.propiq_graph = build_graph()
        
    st.session_state.graph_version = current_version
    print(f"♻️ [GRAPH] Recompiled. Version: {current_version}")
        
    if 'final_state' not in st.session_state:
        st.session_state.final_state = None
    if 'agent_log' not in st.session_state:
        st.session_state.agent_log = []

# Initialize the secure session for the current user
init_session()



# --- SIDEBAR: THE ARCHITECT CREDENTIAL & LIVE ANALYTICS ---
with st.sidebar:
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("""
        <div style='background-color: #1e293b; padding: 15px; border-radius: 8px; border-left: 3px solid #d4af37; box-shadow: 0 4px 6px rgba(0,0,0,0.3);'>
            <p style='color: #94a3b8; font-size: 0.75rem; font-weight: 600; margin-bottom: 2px; letter-spacing: 1px;'>LEAD SYSTEM ARCHITECT</p>
            <p style='color: #d4af37; font-size: 1.1rem; font-weight: bold; margin-bottom: 2px;'>H. Aadil Mohamed</p>
            <p style='color: #e2e8f0; font-size: 0.80rem; margin-bottom: 4px;'>B.Tech AI & Data Science</p>
            <p style='color: #64748b; font-size: 0.70rem; margin-bottom: 0px;'>Class of 2026</p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### 📡 Global Platform Metrics")
    stats = get_live_stats()
    st.metric("Live Sessions Tracked", stats.get("total_sessions", 0))
    st.metric("User Satisfaction Rate", f"{stats.get('pct_positive', 0)}% 👍")
    
    st.markdown("---")
    if st.button("♻️ Force Recompile Graph", type="secondary"):
        keys_to_clear = ["propiq_graph", "graph_version", "final_state"]
        for key in keys_to_clear:
            if key in st.session_state:
                del st.session_state[key]
        st.cache_resource.clear()
        st.success("Graph memory wiped. System recompiled.")
        st.rerun()
    if "graph_version" in st.session_state:
        st.caption(f"Graph Core v{st.session_state.graph_version}")

# --- MAIN DASHBOARD HEADER ---
st.title("🏙️ PropIQ UAE: Sovereign Intelligence Matrix")
st.markdown("**Autonomous Multi-Agent Property Forecasting, Visual Analysis & Legal Engine**")
st.markdown("---")

# --- THE INPUT MATRIX ---
col_input1, col_input2 = st.columns([2, 1])
with col_input1:
    query = st.text_input("Enter Investment Query (e.g., 'I have 4.5M, looking for a 3 bed in Downtown'):")
with col_input2:
    uploaded_image = st.file_uploader("Upload Property Image (For CV Luxury Assessment):", type=["jpg", "jpeg", "png"])

# --- THE EXECUTION CORE (SESSION ISOLATED) ---
if st.button("Initialize Multi-Agent Analysis"):
    if not query:
        st.warning("⚠️ System Notice: Please enter a property query to begin.")
    else:
        st.markdown("### 🧠 Live Agent Thought Log")
        log_container = st.container()
        
        with st.spinner("Orchestrating Sovereign Matrix..."):
            try:
                async def run_backend():
                    img_bytes = uploaded_image.getvalue() if uploaded_image else None
                    state_input = {"query": query, "image_bytes": img_bytes}
                    
                    # THE AMNESIA FIX: This master memory keeps all data from every agent
                    master_memory = state_input.copy()
                    
                    async for event in st.session_state.propiq_graph.astream(state_input):
                        for node, state_update in event.items():
                            with log_container:
                                if node == "parser":
                                    st.info("🟡 **Agent 1 (Query Parser):** Normalizing input data...")
                                elif node == "cv_vision":
                                    st.info("🔵 **Agent 2 (Vision Engine):** Analyzing aesthetics...")
                                elif node == "financial":
                                    st.success("🟢 **Agent 3 (Financial Analyst):** Running XGBoost ML valuation...")
                                elif node == "scout":
                                    st.warning("🟠 **Agent 4 (Market Scout):** Querying live listings...")
                                elif node == "legal":
                                    st.error("🔴 **Agent 5 (Legal/Risk):** Verifying compliance...")
                                elif node == "supervisor":
                                    st.markdown("👑 **Agent 6 (Supervisor):** Finalizing verdict...")
                            
                            # CRITICAL: Merge this agent's work into the master memory
                            master_memory.update(state_update)
                            
                    return master_memory
                    
                st.session_state.final_state = asyncio.run(run_backend())
                
            except Exception as e:
                st.error(f"CRITICAL SYSTEM FAULT: {str(e)}")

# --- OUTPUT RENDERING ---
if st.session_state.final_state:
    final_state = st.session_state.final_state
    
    try:
        verdict = json.loads(final_state.get("final_verdict", "{}"))
        grade = verdict.get("investment_grade", "N/A")
        summary = verdict.get("executive_summary", "Analysis complete.")
    except:
        grade = "ERROR"
        summary = "Failed to parse Supervisor JSON."

    st.markdown("---")
    st.markdown("### 📊 Sovereign Intelligence Output")
    
    

    # The Geographic Warning Banner
    if final_state.get("out_of_market") and final_state.get("market_warning"):
        st.warning(f"⚠️ **Out-of-Market Query Detected:**\n\n{final_state.get('market_warning')}")
    
    metric1, metric2, metric3 = st.columns(3)
    metric1.metric("Investment Grade", grade)
    metric2.metric("Computed ML Valuation", f"AED {final_state.get('ml_price', 0):,.2f}")
    metric3.metric("CV Luxury Premium", f"{final_state.get('cv_multiplier', 1.0)}x")
    
    st.markdown("#### 📝 Executive Summary")
    st.info(summary)
    
    st.markdown("#### 🌐 Live Market Comparables (Scraped via Tavily)")
    for idx, listing in enumerate(final_state.get("listings", [])[:3], 1):
        st.write(f"**{idx}. {listing.get('title', 'Property Listing')}**")
        st.write(f"🔗 [View Live Listing]({listing.get('url', '#')})")
    
    st.markdown("---")
    st.markdown("### 📄 Institutional Export")
    pdf_filename = generate_investment_dossier(final_state, "Sovereign_Dossier.pdf")
    with open(pdf_filename, "rb") as pdf_file:
        PDFbyte = pdf_file.read()
    st.download_button(label="⬇️ Download Official PDF Dossier", data=PDFbyte, file_name="PropIQ_Dossier.pdf", mime='application/octet-stream')
    
    # --- PRODUCT LAYER: USER FEEDBACK ---
    st.markdown("---")
    st.markdown("### 📈 Help Calibrate the Matrix")
    with st.form("feedback_form"):
        st.write("Was this valuation accurate and helpful?")
        rating_col1, rating_col2 = st.columns(2)
        with rating_col1:
            is_up = st.checkbox("👍 Yes, highly accurate")
        with rating_col2:
            is_down = st.checkbox("👎 No, needs adjustment")
            
        comment = st.text_area("Additional thoughts (Optional):")
        submitted = st.form_submit_button("Submit Intelligence Feedback")
        
        if submitted:
            if is_up and is_down:
                st.warning("Please select only one rating.")
            elif not is_up and not is_down:
                st.warning("Please select a rating before submitting.")
            else:
                rating_val = 1 if is_up else -1
                if log_feedback(rating_val, comment, final_state):
                    st.success("✅ Feedback securely transmitted to the Global Database.")
                else:
                    st.error("⚠️ Error transmitting feedback.")