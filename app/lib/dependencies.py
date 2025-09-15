from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from types import SimpleNamespace
from lib.auth import verify_access_token

security = HTTPBearer()

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """하이브리드 패턴: AT는 완전 stateless"""
    token = credentials.credentials
    payload = verify_access_token(token)
    user_id = payload["user_id"]
    session_id = payload.get("session_id")
    
    return SimpleNamespace(
        id=user_id,
        current_session_id=session_id
    )