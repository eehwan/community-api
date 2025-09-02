from typing import List, Optional, Dict, Any
from datetime import datetime
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from repositories.post_repository import post_repository
from repositories.board_repository import board_repository

class PostService:
    def create_post(self, db: Session, title: str, content: str, board_id: int, user_id: int):
        board = board_repository.get_board_by_id(db, board_id)
        if not board:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Board not found"
            )
        
        if not board.public and board.owner_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Cannot create post in this board"
            )
        
        post = post_repository.create_post(db, title, content, board_id, user_id)
        return post
    
    def get_post(self, db: Session, post_id: int, user_id: int):
        post = post_repository.get_post_by_id(db, post_id)
        if not post:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Post not found"
            )
        
        board = post.board
        if not board.public and board.owner_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied"
            )
        
        return post
    
    def list_posts(self, db: Session, board_id: int, user_id: int, cursor_time: Optional[datetime] = None, cursor_id: Optional[int] = None, limit: int = 20) -> Dict[str, Any]:
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
        
        posts = post_repository.get_posts_by_board(db, board_id, cursor_time, cursor_id, limit)
        
        next_cursor_time = None
        next_cursor_id = None
        if len(posts) == limit:
            last_post = posts[-1]
            next_cursor_time = last_post.created_at
            next_cursor_id = last_post.id
        
        return {
            "posts": posts,
            "next_cursor_time": next_cursor_time,
            "next_cursor_id": next_cursor_id
        }
    
    def update_post(self, db: Session, post_id: int, user_id: int, title: str, content: str):
        post = post_repository.get_post_by_id(db, post_id)
        if not post:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Post not found"
            )
        
        if post.author_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only post author can update"
            )
        
        return post_repository.update_post(db, post, title, content)
    
    def delete_post(self, db: Session, post_id: int, user_id: int):
        post = post_repository.get_post_by_id(db, post_id)
        if not post:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Post not found"
            )
        
        if post.author_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only post author can delete"
            )
        
        post_repository.delete_post(db, post)

post_service = PostService()