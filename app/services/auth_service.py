from datetime import timedelta
from typing import Optional
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from lib.auth import verify_password, create_access_token, create_refresh_token, ACCESS_TOKEN_EXPIRE_SECONDS
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
    
    def login(self, db: Session, email: str, password: str, device_name: str = None, ip_address: str = "", user_agent: str = ""):
        user = user_repository.get_user_by_email(db, email)
        if not user or not verify_password(password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password"
            )
        
        # Refresh Token 생성 및 기기 세션 저장 (DB)
        refresh_token = create_refresh_token()
        session_id = session_repository.create_device_session(
            db, user.id, refresh_token, device_name, ip_address, user_agent
        )
        
        # Access Token 생성 (session_id 포함)
        access_token = create_access_token({
            "sub": str(user.id),
            "sid": session_id
        })
        
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "user_id": user.id,
            "expires_in": ACCESS_TOKEN_EXPIRE_SECONDS
        }
    
    def refresh_access_token(self, db: Session, refresh_token: str):
        """하이브리드 패턴: RT에서만 상태 검사"""
        # 1. RT 검증 및 세션 조회 (DB)
        session = session_repository.get_device_session(db, refresh_token)
        if not session:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired refresh token"
            )
        
        # 2. 세션 상태 검증 (DB 기준)
        if session.revoked_at:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Session revoked"
            )
        
        # 3. 사용자 존재는 세션이 있으면 보장됨 (FK 제약조건)
        
        # 4. 새 RT 생성 및 기존 RT 무효화 (RT rotation)
        new_refresh_token = create_refresh_token()
        session_repository.update_refresh_token(db, str(session.id), new_refresh_token)
        
        # 5. 새 AT 발급 (stateless)
        access_token = create_access_token({
            "sub": str(session.user_id),
            "sid": str(session.id)
        })
        
        return {
            "access_token": access_token,
            "refresh_token": new_refresh_token,
            "token_type": "bearer",
            "expires_in": ACCESS_TOKEN_EXPIRE_SECONDS
        }
    
    def logout_session(self, db: Session, user_id: int, session_id: str):
        """특정 세션 로그아웃"""
        session_repository.revoke_device_session(db, user_id, session_id, "user_logout")
        return True
    
    def logout_all_sessions(self, db: Session, user_id: int):
        """모든 세션 로그아웃 - RT 갱신 시 차단"""
        session_repository.revoke_all_user_sessions(db, user_id, "logout_all")
        return True
    
    def get_user_sessions(self, db: Session, user_id: int):
        """사용자의 모든 활성 세션 조회"""
        sessions = session_repository.get_user_devices(db, user_id)
        return {"sessions": sessions}

auth_service = AuthService()