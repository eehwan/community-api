from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from pydantic import BaseModel
from infra.database import get_db
from services.post_service import post_service
from lib.dependencies import get_current_user
from entities.user import User

router = APIRouter(prefix="/posts", tags=["posts"])

class PostCreateRequest(BaseModel):
    title: str
    content: str
    board_id: int

class PostUpdateRequest(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None

@router.post("/")
async def create_post(
    request: PostCreateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return post_service.create_post(db, request.title, request.content, request.board_id, current_user.id)

@router.get("/{post_id}")
async def get_post(
    post_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return post_service.get_post(db, post_id, current_user.id)

@router.get("/board/{board_id}")
async def list_posts(
    board_id: int,
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return post_service.list_posts(db, board_id, current_user.id, limit, offset)

@router.put("/{post_id}")
async def update_post(
    post_id: int,
    request: PostUpdateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return post_service.update_post(db, post_id, current_user.id, request.title, request.content)

@router.delete("/{post_id}")
async def delete_post(
    post_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return post_service.delete_post(db, post_id, current_user.id)