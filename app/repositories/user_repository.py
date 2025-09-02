from typing import Optional
from sqlalchemy.orm import Session
from entities.user import User
from lib.auth import get_password_hash

class UserRepository:
    def create_user(self, db: Session, fullname: str, email: str, password: str) -> User:
        hashed_password = get_password_hash(password)
        user = User(
            fullname=fullname,
            email=email,
            hashed_password=hashed_password
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    
    def get_user_by_email(self, db: Session, email: str) -> Optional[User]:
        return db.query(User).filter(User.email == email).first()
    
    def get_user_by_id(self, db: Session, user_id: int) -> Optional[User]:
        return db.query(User).filter(User.id == user_id).first()

user_repository = UserRepository()