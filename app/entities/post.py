from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Index
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .base import Base

class Post(Base):
    __tablename__ = "posts"
    
    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    content = Column(Text, nullable=False)
    board_id = Column(Integer, ForeignKey("boards.id"), nullable=False)
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    board = relationship("Board", back_populates="posts")
    author = relationship("User", back_populates="posts")
    
    __table_args__ = (
        Index('idx_posts_board_created', 'board_id', 'created_at', 'id',
              postgresql_ops={'created_at': 'DESC', 'id': 'DESC'}),
    )