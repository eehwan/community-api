from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func
from entities.board import Board
from entities.post import Post

class BoardRepository:
    def create_board(self, db: Session, name: str, public: bool, owner_id: int) -> Board:
        board = Board(name=name, public=public, owner_id=owner_id)
        db.add(board)
        db.commit()
        db.refresh(board)
        return board
    
    def get_board_by_id(self, db: Session, board_id: int) -> Optional[Board]:
        return db.query(Board).filter(Board.id == board_id).first()
    
    def get_board_by_name(self, db: Session, name: str) -> Optional[Board]:
        return db.query(Board).filter(Board.name == name).first()
    
    def get_accessible_boards(self, db: Session, user_id: int, limit: int = 20, offset: int = 0) -> List[Board]:
        return db.query(Board)\
            .filter((Board.public == True) | (Board.owner_id == user_id))\
            .order_by(func.count(Post.id).desc())\
            .outerjoin(Post)\
            .group_by(Board.id)\
            .limit(limit).offset(offset).all()
    
    def update_board(self, db: Session, board: Board, name: str = None, public: bool = None) -> Board:
        if name is not None:
            board.name = name
        if public is not None:
            board.public = public
        db.commit()
        db.refresh(board)
        return board
    
    def delete_board(self, db: Session, board: Board):
        db.delete(board)
        db.commit()

board_repository = BoardRepository()