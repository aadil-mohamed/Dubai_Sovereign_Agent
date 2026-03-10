import json
import os
import logging
from upstash_redis import Redis
from tavily import TavilyClient

logger = logging.getLogger(__name__)

def search_comparables(query: str):
    """Searches Tavily for live property listings with Upstash Redis caching."""
    try:
        # 1. Load keys directly from the cloud environment (No Streamlit)
        tavily_key = os.environ.get("TAVILY_API_KEY")
        redis_url = os.environ.get("UPSTASH_REDIS_REST_URL")
        redis_token = os.environ.get("UPSTASH_REDIS_REST_TOKEN")

        if not tavily_key:
            logger.error("Tavily API key is missing.")
            return {"results": []}

        tavily_client = TavilyClient(api_key=tavily_key)
        
        # 2. Connect to Redis Cache
        redis_client = None
        if redis_url and redis_token:
            redis_client = Redis(url=redis_url, token=redis_token)

        cache_key = f"tavily_comps:{query.replace(' ', '_').lower()}"

        # 3. Check Cache
        if redis_client:
            cached_data = redis_client.get(cache_key)
            if cached_data:
                logger.info("Tavily Cache HIT")
                return json.loads(cached_data) if isinstance(cached_data, str) else cached_data

        # 4. Fetch Live Data
        logger.info("Tavily Cache MISS. Fetching live market data...")
        response = tavily_client.search(
            query=query, 
            search_depth="advanced"
        )

        # 5. Save to Cache
        if redis_client and response:
            redis_client.set(cache_key, json.dumps(response))
            
        return response
        
    except Exception as e:
        logger.error(f"Tavily search failed: {str(e)}")
        return {"results": []}
