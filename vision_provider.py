import os
import base64
import json
from openai import AsyncOpenAI
from dotenv import load_dotenv

load_dotenv()

# The ultimate fail-safe baseline
FALLBACK = {
    "premium_multiplier": 1.0,
    "assessment": "Vision unavailable — baseline multiplier applied."
}

# ── GITHUB MODELS CLIENT (GPT-4o via Student Pack)
async def analyze_property_image_github(image_bytes: bytes) -> dict:
    client = AsyncOpenAI(
        base_url="https://models.inference.ai.azure.com",
        api_key=os.getenv("GITHUB_TOKEN"),
    )
    b64_image = base64.b64encode(image_bytes).decode('utf-8')
    
    response = await client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": """You are a UAE luxury property assessor. Evaluate the image and return ONLY valid JSON.
                {"luxury_score": 8.5, "multiplier": 1.25, "assessment": "Premium finishes."}. 
                Multiplier guide: 1.0=basic, 1.1=mid, 1.25=high-end, 1.4=ultra-luxury, 1.5=exceptional.
                Be specific about what you see."""
            },
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Analyze this property interior and assign the financial multiplier."},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64_image}", "detail": "high"}}
                ]
            }
        ],
        response_format={"type": "json_object"},
        temperature=0.1,
        max_tokens=200
    )
    
    result = json.loads(response.choices[0].message.content)
    return {
        "premium_multiplier": result.get("multiplier", 1.0),
        "assessment": result.get("assessment", "Assessment complete.")
    }

# ── THE ABSTRACTION ROUTER
async def analyze_image(image_bytes: bytes) -> dict:
    """Routes the image to the active provider. Protects against rate limits and expiry."""
    if not image_bytes or len(image_bytes) < 100:
        print("👁️ Vision Engine: No image provided. Applying baseline.")
        return FALLBACK
    
    # Reads the active provider from your .env file
    provider = os.getenv("VISION_PROVIDER", "github").lower()
    
    try:
        if provider == "github":
            print("👁️ Vision Engine: Routing to GitHub Models (GPT-4o) [Limit: 150/day]...")
            result = await analyze_property_image_github(image_bytes)
            print(f"👁️ Vision Engine Sees: {result.get('assessment')}")
            return result
            
        elif provider == "groq":
            print("👁️ Vision Engine: Routing to Groq (llama-3.2-11b-vision) [Fallback Mode]...")
            # Logic for Groq Vision will be activated here in May 2026
            return FALLBACK
            
        elif provider == "openai":
            print("👁️ Vision Engine: Routing to Paid OpenAI (gpt-4o-mini)...")
            # Logic for Paid API will be activated here when you have revenue
            return FALLBACK
            
        else:
            return FALLBACK
            
    except Exception as e:
        print(f"⚠️ Vision Engine Failed: {str(e)}")

        return FALLBACK
