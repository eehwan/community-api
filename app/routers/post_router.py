from typing import List, Optional
from datetime import datetime
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from infra.database import get_db
from services.post_service import post_service
from lib.dependencies import get_current_user
from entities.user import User
from schemas.post import PostCreateRequest, PostUpdateRequest, PostResponse, PostListResponse

router = APIRouter(tags=["posts"])

@router.post("/boards/{board_id}/posts", response_model=PostResponse)
async def create_post(
    board_id: int,
    request: PostCreateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return post_service.create_post(db, request.title, request.content, board_id, current_user.id)

@router.get("/posts/{post_id}", response_model=PostResponse)
async def get_post(
    post_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return post_service.get_post(db, post_id, current_user.id)

@router.get("/boards/{board_id}/posts", response_model=PostListResponse)
async def list_posts(
    board_id: int,
    limit: int = Query(20, ge=1, le=100),
    cursor_time: Optional[datetime] = Query(None),
    cursor_id: Optional[int] = Query(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return post_service.list_posts(db, board_id, current_user.id, cursor_time, cursor_id, limit)

@router.put("/posts/{post_id}", response_model=PostResponse)
async def update_post(
    post_id: int,
    request: PostUpdateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return post_service.update_post(db, post_id, current_user.id, request.title, request.content)

@router.delete("/posts/{post_id}", status_code=204)
async def delete_post(
    post_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return post_service.delete_post(db, post_id, current_user.id)