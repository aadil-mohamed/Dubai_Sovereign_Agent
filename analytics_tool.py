import os
import uuid
from datetime import datetime
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")

def get_supabase_client():
    if not url or not key:
        return None
    return create_client(url, key)

def log_feedback(rating: int, comment: str, state_data: dict):
    """Pushes user feedback directly to the Supabase Cloud."""
    supabase = get_supabase_client()
    if not supabase:
        print("⚠️ Supabase Credentials Missing.")
        return False
    
    try:
        supabase.table("feedback").insert({
            "session_id": str(uuid.uuid4()),
            "rating": rating,
            "comment": comment,
            "area": state_data.get("area", "Unknown"),
            "budget_aed": state_data.get("budget_aed", 0),
            "timestamp": datetime.utcnow().isoformat(),
            "cv_used": state_data.get("cv_multiplier", 1.0) != 1.0
        }).execute()
        return True
    except Exception as e:
        print(f"CRITICAL Analytics Error: {e}")
        return False

def get_live_stats() -> dict:
    """Pulls live metrics from the Supabase RPC function."""
    supabase = get_supabase_client()
    if not supabase: 
        return {"total_sessions": 0, "pct_positive": 0}
    
    try:
        result = supabase.rpc("get_feedback_stats").execute()
        if result.data:
            return result.data[0]
    except Exception as e:
        print(f"Analytics RPC Error: {e}")
        
    return {"total_sessions": 0, "pct_positive": 0}