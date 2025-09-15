import hashlib
from datetime import datetime, timedelta
from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import and_
from entities.session import Session as SessionModel
from entities.user import User
from lib.auth import REFRESH_TOKEN_EXPIRE_SECONDS

class SessionRepository:
    def create_device_session(self, db: Session, user_id: int, refresh_token: str, device_name: str, ip_address: str, user_agent: str = "") -> str:
        """새 기기 세션 생성 - DB 저장만 (하이브리드 패턴)"""
        # refresh_token 해시화 (보안)
        token_hash = hashlib.sha256(refresh_token.encode()).hexdigest()
        
        # DB에 세션 저장
        expires_at = datetime.now() + timedelta(seconds=REFRESH_TOKEN_EXPIRE_SECONDS)
        session = SessionModel(
            user_id=user_id,
            device_name=device_name or "Unknown Device",
            ip_address=ip_address,
            user_agent=user_agent,
            refresh_token_hash=token_hash,
            expires_at=expires_at
        )
        
        db.add(session)
        db.commit()
        db.refresh(session)
        
        return str(session.id)
    
    def get_device_session(self, db: Session, refresh_token: str) -> Optional[SessionModel]:
        """Refresh Token으로 세션 조회 (기존 이름 유지)"""
        token_hash = hashlib.sha256(refresh_token.encode()).hexdigest()
        return db.query(SessionModel).filter(
            and_(
                SessionModel.refresh_token_hash == token_hash,
                SessionModel.revoked_at.is_(None),
                SessionModel.expires_at > datetime.now()
            )
        ).first()
    
    def get_session_by_id(self, db: Session, session_id: str) -> Optional[SessionModel]:
        """Session ID로 세션 조회"""
        return db.query(SessionModel).filter(
            and_(
                SessionModel.id == session_id,
                SessionModel.revoked_at.is_(None),
                SessionModel.expires_at > datetime.now()
            )
        ).first()
    
    
    def update_last_activity(self, db: Session, session_id: str):
        """마지막 활동 시간 업데이트 (기존 이름 유지)"""
        # DB 업데이트
        db.query(SessionModel).filter(SessionModel.id == session_id).update({
            "last_seen_at": datetime.now()
        })
        db.commit()
    
    def update_refresh_token(self, db: Session, session_id: str, new_refresh_token: str):
        """세션의 refresh token 업데이트 (RT rotation)"""
        token_hash = hashlib.sha256(new_refresh_token.encode()).hexdigest()
        db.query(SessionModel).filter(SessionModel.id == session_id).update({
            "refresh_token_hash": token_hash,
            "last_seen_at": datetime.now()
        })
        db.commit()
    
    def revoke_device_session(self, db: Session, user_id: int, session_id: str, reason: str = "user_logout"):
        """특정 기기 세션 무효화 - RT 단계에서만 처리"""
        # DB에서 revoked_at 설정 (하이브리드 패턴: RT에서만 상태 관리)
        db.query(SessionModel).filter(SessionModel.id == session_id).update({
            "revoked_at": datetime.now(),
            "revocation_reason": reason
        })
        db.commit()
    
    def revoke_all_user_sessions(self, db: Session, user_id: int, reason: str = "logout_all"):
        """사용자의 모든 세션 무효화 - RT 갱신 시에만 차단"""
        # 모든 활성 세션 무효화 (RT 갱신 차단)
        active_sessions = db.query(SessionModel).filter(
            and_(
                SessionModel.user_id == user_id,
                SessionModel.revoked_at.is_(None)
            )
        ).all()
        
        for session in active_sessions:
            session.revoked_at = datetime.now()
            session.revocation_reason = reason
        
        db.commit()
    
    def get_user_devices(self, db: Session, user_id: int) -> List[dict]:
        """사용자의 모든 활성 기기 조회 (기존 이름 유지)"""
        sessions = db.query(SessionModel).filter(
            and_(
                SessionModel.user_id == user_id,
                SessionModel.revoked_at.is_(None),
                SessionModel.expires_at > datetime.now()
            )
        ).order_by(SessionModel.last_seen_at.desc()).all()
        
        devices = []
        for session in sessions:
            devices.append({
                "session_id": str(session.id),
                "device_name": session.device_name,
                "last_active": session.last_seen_at,
                "ip_address": session.ip_address
            })
        
        return devices
    

session_repository = SessionRepository()