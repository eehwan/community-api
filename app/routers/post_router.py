from typing import List
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from infra.database import get_db
from services.post_service import post_service
from lib.dependencies import get_current_user
from entities.user import User
from schemas.post import PostCreateRequest, PostUpdateRequest, PostResponse

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

@router.get("/boards/{board_id}/posts", response_model=List[PostResponse])
async def list_posts(
    board_id: int,
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return post_service.list_posts(db, board_id, current_user.id, limit, offset)

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