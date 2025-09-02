from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field

class PostCreateRequest(BaseModel):
    title: str = Field(..., min_length=1, strip_whitespace=True)
    content: str = Field(..., min_length=1, strip_whitespace=True)

class PostUpdateRequest(BaseModel):
    title: str = Field(..., min_length=1, strip_whitespace=True)
    content: str = Field(..., min_length=1, strip_whitespace=True)

class PostResponse(BaseModel):
    id: int
    title: str
    content: str
    board_id: int
    author_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class PostListResponse(BaseModel):
    posts: List[PostResponse]
    next_cursor_time: Optional[datetime] = None
    next_cursor_id: Optional[int] = None