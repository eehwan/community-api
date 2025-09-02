from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from infra.database import get_db
from services.user_service import user_service
from lib.dependencies import get_current_user
from entities.user import User

router = APIRouter(prefix="/auth", tags=["auth"])

class SignupRequest(BaseModel):
    fullname: str
    email: EmailStr
    password: str

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

@router.post("/signup")
async def signup(request: SignupRequest, db: Session = Depends(get_db)):
    return user_service.signup(db, request.fullname, request.email, request.password)

@router.post("/login")
async def login(request: LoginRequest, db: Session = Depends(get_db)):
    return user_service.login(db, request.email, request.password)

@router.post("/logout")
async def logout(current_user: User = Depends(get_current_user)):
    return user_service.logout(current_user.id)