from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from pydantic import BaseModel
from infra.database import get_db
from services.board_service import board_service
from lib.dependencies import get_current_user
from entities.user import User

router = APIRouter(prefix="/boards", tags=["boards"])

class BoardCreateRequest(BaseModel):
    name: str
    public: bool = True

class BoardUpdateRequest(BaseModel):
    name: Optional[str] = None
    public: Optional[bool] = None

@router.post("/")
async def create_board(
    request: BoardCreateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return board_service.create_board(db, request.name, request.public, current_user.id)

@router.get("/{board_id}")
async def get_board(
    board_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return board_service.get_board(db, board_id, current_user.id)

@router.get("/")
async def list_boards(
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return board_service.list_boards(db, current_user.id, limit, offset)

@router.put("/{board_id}")
async def update_board(
    board_id: int,
    request: BoardUpdateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return board_service.update_board(db, board_id, current_user.id, request.name, request.public)

@router.delete("/{board_id}")
async def delete_board(
    board_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return board_service.delete_board(db, board_id, current_user.id)