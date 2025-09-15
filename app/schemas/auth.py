from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

class SignupRequest(BaseModel):
    fullname: str = Field(..., min_length=1, strip_whitespace=True)
    email: EmailStr
    password: str = Field(..., min_length=1)

class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=1)

class SignupResponse(BaseModel):
    message: str
    user_id: int

class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: int
    expires_in: int

class RefreshResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int

class UserSession(BaseModel):
    device_name: str
    last_active: datetime
    ip_address: str

class UserSessionsResponse(BaseModel):
    sessions: list[UserSession]