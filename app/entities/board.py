from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Index
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .base import Base

class Board(Base):
    __tablename__ = "boards"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, index=True, nullable=False)
    public = Column(Boolean, default=True, nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    post_count = Column(Integer, default=0, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    owner = relationship("User", back_populates="boards")
    posts = relationship("Post", back_populates="board", cascade="all, delete-orphan")
    
    __table_args__ = (
        # 공개 게시판 정렬용 (public = true 필터링 후 정렬)
        Index('idx_boards_public_rank', 'public', 'post_count', 'id', 
              postgresql_ops={'post_count': 'DESC'}),
        # 내 게시판 정렬용 (owner_id 필터링 후 정렬)  
        Index('idx_boards_owner_rank', 'owner_id', 'post_count', 'id',
              postgresql_ops={'post_count': 'DESC'}),
    )