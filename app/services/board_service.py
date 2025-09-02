from typing import List
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from repositories.board_repository import board_repository

class BoardService:
    def create_board(self, db: Session, name: str, public: bool, user_id: int):
        existing_board = board_repository.get_board_by_name(db, name)
        if existing_board:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Board name already exists"
            )
        
        board = board_repository.create_board(db, name, public, user_id)
        return board
    
    def get_board(self, db: Session, board_id: int, user_id: int):
        board = board_repository.get_board_by_id(db, board_id)
        if not board:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Board not found"
            )
        
        if not board.public and board.owner_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied"
            )
        
        return board
    
    def list_boards(self, db: Session, user_id: int, limit: int = 20, offset: int = 0):
        boards = board_repository.get_accessible_boards(db, user_id, limit, offset)
        return boards
    
    def update_board(self, db: Session, board_id: int, user_id: int, name: str = None, public: bool = None):
        board = board_repository.get_board_by_id(db, board_id)
        if not board:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Board not found"
            )
        
        if board.owner_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only board owner can update"
            )
        
        if name and name != board.name:
            existing_board = board_repository.get_board_by_name(db, name)
            if existing_board:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Board name already exists"
                )
        
        return board_repository.update_board(db, board, name, public)
    
    def delete_board(self, db: Session, board_id: int, user_id: int):
        board = board_repository.get_board_by_id(db, board_id)
        if not board:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Board not found"
            )
        
        if board.owner_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only board owner can delete"
            )
        
        board_repository.delete_board(db, board)

board_service = BoardService()