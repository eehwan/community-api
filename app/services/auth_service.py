from datetime import timedelta
from typing import Optional
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from lib.auth import verify_password, create_access_token, create_refresh_token, ACCESS_TOKEN_EXPIRE_MINUTES
from repositories.user_repository import user_repository
from repositories.session_repository import session_repository

class AuthService:
    def signup(self, db: Session, fullname: str, email: str, password: str):
        existing_user = user_repository.get_user_by_email(db, email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        user = user_repository.create_user(db, fullname, email, password)
        return {"message": "User created successfully", "user_id": user.id}
    
    def login(self, db: Session, email: str, password: str, device_name: str = None, ip_address: str = ""):
        user = user_repository.get_user_by_email(db, email)
        if not user or not verify_password(password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password"
            )
        
        # Refresh Token 생성 및 기기 세션 저장
        refresh_token = create_refresh_token()
        session_repository.create_device_session(user.id, refresh_token, device_name, ip_address)
        
        # Access Token 생성 (session_id 포함)
        access_token = create_access_token(data={"sub": str(user.id)}, refresh_token=refresh_token)
        
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "user_id": user.id,
            "expires_in": ACCESS_TOKEN_EXPIRE_MINUTES * 60
        }
    
    def refresh_access_token(self, refresh_token: str):
        """Refresh Token으로 새 Access Token 발급"""
        session_data = session_repository.get_device_session(refresh_token)
        if not session_data:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired refresh token"
            )
        
        # 마지막 활동 시간 업데이트
        session_repository.update_last_activity(refresh_token)
        
        # 새 Access Token 생성 (refresh_token 포함)
        access_token = create_access_token(data={"sub": str(session_data["user_id"])}, refresh_token=refresh_token)
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "expires_in": ACCESS_TOKEN_EXPIRE_MINUTES * 60
        }
    
    def logout_session(self, user_id: int, refresh_token: str):
        """특정 세션 로그아웃 (현재 세션 또는 다른 세션)"""
        session_repository.revoke_device_session(user_id, refresh_token)
        return True
    
    def logout_all_sessions(self, user_id: int):
        """모든 세션 로그아웃"""
        session_repository.revoke_all_user_sessions(user_id)
        return True
    
    def get_user_sessions(self, user_id: int):
        """사용자의 모든 활성 세션 조회"""
        sessions = []
        device_sessions = session_repository.get_user_devices(user_id)
        
        for session_data in device_sessions:
            sessions.append({
                "device_name": session_data["device_name"],
                "last_active": session_data["last_active"],
                "ip_address": session_data["ip_address"]
            })
        
        return {"sessions": sessions}

auth_service = AuthService()