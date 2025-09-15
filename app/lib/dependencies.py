from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from infra.database import get_db
from repositories.user_repository import user_repository
from lib.auth import verify_access_token

security = HTTPBearer()

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """Access Token만으로 사용자 인증 (Redis 조회 없음)"""
    token = credentials.credentials
    payload = verify_access_token(token)
    user_id = payload["user_id"]
    
    user = user_repository.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    
    # refresh_token 정보를 user 객체에 추가
    user.current_refresh_token = payload.get("refresh_token")
    return user