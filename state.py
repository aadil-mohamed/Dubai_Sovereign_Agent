from pydantic import BaseModel, Field
from typing import List, Optional

class AgentState(BaseModel):
    query: str = ""
    image_bytes: Optional[bytes] = None 
    
    area: Optional[str] = "Dubai Marina"
    bedrooms: Optional[int] = 1
    budget_aed: Optional[float] = 0.0
    is_offplan: Optional[bool] = False
    
    ml_price: Optional[float] = 0.0
    cv_multiplier: Optional[float] = 1.0
    listings: List[dict] = Field(default_factory=list)
    legal_flags: List[str] = Field(default_factory=list)
    debate_log: List[str] = Field(default_factory=list)
    final_verdict: Optional[str] = ""
    
    out_of_market: Optional[bool] = False
    market_warning: Optional[str] = ""