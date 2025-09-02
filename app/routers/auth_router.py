from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from infra.database import get_db
from services.user_service import user_service
from lib.dependencies import get_current_user
from entities.user import User
from schemas.auth import SignupRequest, LoginRequest, SignupResponse, LoginResponse

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/signup", response_model=SignupResponse)
async def signup(request: SignupRequest, db: Session = Depends(get_db)):
    return user_service.signup(db, request.fullname, request.email, request.password)

@router.post("/login", response_model=LoginResponse)
async def login(request: LoginRequest, db: Session = Depends(get_db)):
    return user_service.login(db, request.email, request.password)

@router.post("/logout", status_code=204)
async def logout(current_user: User = Depends(get_current_user)):
    return user_service.logout(current_user.id)