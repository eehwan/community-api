from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field

class BoardCreateRequest(BaseModel):
    name: str = Field(..., min_length=1, strip_whitespace=True)
    public: bool = True

class BoardUpdateRequest(BaseModel):
    name: Optional[str] = Field(None, min_length=1, strip_whitespace=True)
    public: Optional[bool] = None

class BoardResponse(BaseModel):
    id: int
    name: str
    public: bool
    owner_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True