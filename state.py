from pydantic import BaseModel, Field
from typing import List, Optional

class AgentState(BaseModel):
    query: str = ""
    image_bytes: Optional[bytes] = None 
    
    area: str = "Dubai"
    bedrooms: int = 1
    budget_aed: float = 0.0
    is_offplan: bool = False
    
    ml_price: float = 0.0
    cv_multiplier: float = 1.0
    listings: List[dict] = Field(default_factory=list)
    legal_flags: List[str] = Field(default_factory=list)
    debate_log: List[str] = Field(default_factory=list)
    final_verdict: str = ""
    
    out_of_market: bool = False
    market_warning: str = ""