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
        post_count_sq = db.query(
            Post.board_id.label("board_id"),
            func.count(Post.id).label("post_count")
        ).group_by(Post.board_id).subquery()

        return db.query(Board)\
            .outerjoin(post_count_sq, post_count_sq.c.board_id == Board.id)\
            .filter((Board.public.is_(True)) | (Board.owner_id == user_id))\
            .order_by(func.coalesce(post_count_sq.c.post_count, 0).desc(), Board.id)\
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