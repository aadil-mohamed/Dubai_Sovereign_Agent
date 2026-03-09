import hashlib
import json
import os
import streamlit as st
from upstash_redis import Redis
from tavily import TavilyClient
from dotenv import load_dotenv

load_dotenv()

@st.cache_resource
def get_redis():
    """Initializes the persistent connection to the Upstash Cloud."""
    url = os.getenv("UPSTASH_REDIS_REST_URL")
    token = os.getenv("UPSTASH_REDIS_REST_TOKEN")
    if not url or not token:
        print("⚠️ Upstash credentials missing. Caching offline.")
        return None
    return Redis(url=url, token=token)

@st.cache_resource
def get_tavily():
    return TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

def make_cache_key(area: str, bedrooms: int, budget_aed: float) -> str:
    """Normalizes the budget into AED 500K bands to maximize cache hits."""
    try:
        budget_band = (int(budget_aed) // 500000) * 500000
    except:
        budget_band = 0
    raw = f"{area.lower().strip()}:{bedrooms}:{budget_band}"
    return f"tavily:{hashlib.md5(raw.encode()).hexdigest()}"

def search_comparables(area: str, bedrooms: int, budget_aed: float, is_offplan: bool = False, ttl_seconds: int = 86400) -> list:
    """The Upgraded Scraper: Checks Cloud Memory first, scrapes only if necessary."""
    redis = get_redis()
    cache_key = make_cache_key(area, bedrooms, budget_aed)

    # 1. ATTEMPT CACHE RETRIEVAL (Zero Cost, 0 Latency)
    if redis:
        try:
            cached_result = redis.get(cache_key)
            if cached_result:
                print(f"🟢 Market Scout: CACHE HIT! Serving free data for [{cache_key}]")
                return json.loads(cached_result)
        except Exception as e:
            print(f"⚠️ Redis read error: {e}")

    # 2. CACHE MISS: DEPLOY LIVE SCRAPER (Costs API Credits)
    print("🔴 Market Scout: CACHE MISS. Deploying Live Tavily Scraper...")
    client = get_tavily()
    
    try:
        query = f"{bedrooms} bedroom apartment for sale in {area} Dubai"
        raw_results = client.search(query=query, search_depth="advanced", max_results=3)
        
        listings = []
        for r in raw_results.get('results', []):
            listings.append({
                "title": r.get('title', 'Property Listing'),
                "url": r.get('url', '')
            })
            
        # 3. SAVE TO CACHE FOR NEXT USER (Persists for 24 hours)
        if redis and listings:
            try:
                redis.set(cache_key, json.dumps(listings), ex=ttl_seconds)
            except Exception as e:
                print(f"⚠️ Redis write error: {e}")
                
        return listings
    except Exception as e:
        print(f"⚠️ Tavily Scraper Blocked: {e}")
        return [{"title": "Offline Fallback Data", "url": "https://dubailand.gov.ae"}]