from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from entities.post import Post
from repositories.board_repository import board_repository

class PostRepository:
    def create_post(self, db: Session, title: str, content: str, board_id: int, author_id: int) -> Post:
        post = Post(
            title=title,
            content=content,
            board_id=board_id,
            author_id=author_id
        )
        db.add(post)
        db.commit()
        db.refresh(post)
        
        board_repository.increment_post_count_delta(board_id)
        return post
    
    def get_post_by_id(self, db: Session, post_id: int) -> Optional[Post]:
        return db.query(Post).filter(Post.id == post_id).first()
    
    def get_posts_by_board(self, db: Session, board_id: int, cursor_time: Optional[datetime] = None, cursor_id: Optional[int] = None, limit: int = 20) -> List[Post]:
        query = db.query(Post).filter(Post.board_id == board_id)
        
        if cursor_time and cursor_id:
            query = query.filter(
                (Post.created_at < cursor_time) | 
                ((Post.created_at == cursor_time) & (Post.id < cursor_id))
            )
        
        return query.order_by(Post.created_at.desc(), Post.id.desc()).limit(limit).all()
    
    def update_post(self, db: Session, post: Post, title: str = None, content: str = None) -> Post:
        if title is not None:
            post.title = title
        if content is not None:
            post.content = content
        db.commit()
        db.refresh(post)
        return post
    
    def delete_post(self, db: Session, post: Post):
        board_id = post.board_id
        db.delete(post)
        db.commit()
        
        board_repository.decrement_post_count_delta(board_id)

post_repository = PostRepository()