from datetime import timedelta
from typing import Optional
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from lib.auth import verify_password, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from repositories.user_repository import user_repository
from repositories.session_repository import session_repository

class UserService:
    def signup(self, db: Session, fullname: str, email: str, password: str):
        existing_user = user_repository.get_user_by_email(db, email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        user = user_repository.create_user(db, fullname, email, password)
        return {"message": "User created successfully", "user_id": user.id}
    
    def login(self, db: Session, email: str, password: str):
        user = user_repository.get_user_by_email(db, email)
        if not user or not verify_password(password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password"
            )
        
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": str(user.id)}, expires_delta=access_token_expires
        )
        
        session_repository.store_session(user.id, access_token)
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user_id": user.id
        }
    
    def logout(self, user_id: int):
        session_repository.delete_session(user_id)
        return True

user_service = UserService()