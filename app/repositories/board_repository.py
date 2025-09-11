from typing import List, Optional, Dict
from sqlalchemy.orm import Session
from sqlalchemy import func, desc, and_
from entities.board import Board
from entities.post import Post
from infra.redis_client import redis_client

class BoardRepository:
    POST_COUNT_PREFIX = "board:post_count:"
    
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
        public_q = db.query(Board).filter(and_(Board.public.is_(True), Board.owner_id != user_id))
        mine_q = db.query(Board).filter(Board.owner_id == user_id)
        
        return public_q.union_all(mine_q)\
            .order_by(desc(Board.post_count), Board.id)\
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
    
    def increment_post_count_delta(self, board_id: int) -> None:
        """Redis에 게시글 수 증가 기록"""
        redis_client.hincrby("board:post_count", str(board_id), 1)
    
    def decrement_post_count_delta(self, board_id: int) -> None:
        """Redis에 게시글 수 감소 기록"""
        redis_client.hincrby("board:post_count", str(board_id), -1)
    
    def get_all_post_count_deltas(self) -> Dict[int, int]:
        """모든 게시판의 증감량 조회"""
        deltas_str = redis_client.hgetall("board:post_count")
        return {int(board_id): int(delta) for board_id, delta in deltas_str.items() if int(delta) != 0}
    
    def update_board_post_counts(self, db: Session) -> None:
        """Redis 증감량을 읽어서 DB의 post_count 업데이트"""
        deltas = self.get_all_post_count_deltas()
        
        for board_id, delta in deltas.items():
            board = self.get_board_by_id(db, board_id)
            if board:
                board.post_count = max(0, board.post_count + delta)
        
        if deltas:
            redis_client.delete("board:post_count")
            db.commit()

board_repository = BoardRepository()