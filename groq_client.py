import os
import json
from groq import Groq
from tenacity import retry, wait_exponential, stop_after_attempt, retry_if_exception_type, before_sleep_log
import logging
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)

def get_groq_client():
    """Initializes the Groq client once and stores it in cache."""
    return Groq(api_key=os.getenv("GROQ_API_KEY"))

# The Tenacity Decorator: Retries up to 4 times, backing off exponentially (2s, 4s, 8s...)
@retry(
    wait=wait_exponential(multiplier=1, min=2, max=30),
    stop=stop_after_attempt(4),
    retry=retry_if_exception_type(Exception),
    before_sleep=before_sleep_log(logger, logging.WARNING)
)
def call_groq_with_retry(prompt: str, system: str) -> dict:
    """Centralized LLM caller with automatic rate-limit deflection."""
    client = get_groq_client()
    
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": prompt}
        ],
        max_tokens=800,
        temperature=0.1,
        response_format={"type": "json_object"}
    )
    
    raw = response.choices[0].message.content.strip()
    return json.loads(raw)