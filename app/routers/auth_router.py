from fastapi import APIRouter, Depends, Request, Response, Cookie, HTTPException, status
from sqlalchemy.orm import Session
from infra.database import get_db
from services.auth_service import auth_service
from lib.dependencies import get_current_user
from lib.device_parser import parse_device_name
from entities.user import User
from schemas.auth import (
    SignupRequest, LoginRequest, SignupResponse, LoginResponse,
    RefreshResponse, UserSessionsResponse, UserSession
)
from typing import Optional

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/signup", response_model=SignupResponse)
async def signup(request: SignupRequest, db: Session = Depends(get_db)):
    return auth_service.signup(db, request.fullname, request.email, request.password)

@router.post("/login", response_model=LoginResponse)
async def login(
    request: LoginRequest, 
    response: Response,
    fastapi_request: Request, 
    db: Session = Depends(get_db)
):
    ip_address = fastapi_request.client.host if fastapi_request.client else ""
    user_agent = fastapi_request.headers.get("user-agent", "")
    device_name = parse_device_name(user_agent)
    
    result = auth_service.login(db, request.email, request.password, device_name, ip_address)
    
    response.set_cookie(
        key="refresh_token",
        value=result["refresh_token"],
        httponly=True,
        secure=False,  # 개발환경에서는 False, 프로덕션에서는 True
        samesite="lax",
        max_age=30 * 24 * 60 * 60  # 30일
    )
    
    return {
        "access_token": result["access_token"],
        "token_type": result["token_type"],
        "user_id": result["user_id"],
        "expires_in": result["expires_in"]
    }

@router.post("/refresh", response_model=RefreshResponse)
async def refresh_token(refresh_token: Optional[str] = Cookie(None)):
    if not refresh_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token not found"
        )
    return auth_service.refresh_access_token(refresh_token)

@router.post("/logout", status_code=204)
async def logout(
    response: Response,
    current_user: User = Depends(get_current_user)
):
    """현재 세션 로그아웃"""
    refresh_token = getattr(current_user, 'current_refresh_token', None)
    
    response.delete_cookie(key="refresh_token", path="/")
    
    return auth_service.logout_session(current_user.id, refresh_token)

@router.get("/sessions", response_model=UserSessionsResponse)
async def get_user_sessions(current_user: User = Depends(get_current_user)):
    """사용자의 모든 활성 세션 조회"""
    return auth_service.get_user_sessions(current_user.id)

@router.delete("/sessions", status_code=204)
async def delete_all_sessions(
    response: Response,
    current_user: User = Depends(get_current_user)
):
    """모든 세션 삭제"""
    response.delete_cookie(key="refresh_token", path="/")
    
    return auth_service.logout_all_sessions(current_user.id)

@router.delete("/sessions/{refresh_token}", status_code=204)
async def delete_session(refresh_token: str, current_user: User = Depends(get_current_user)):
    """특정 세션 삭제"""
    return auth_service.logout_session(current_user.id, refresh_token)