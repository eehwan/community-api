from pydantic import BaseModel, EmailStr, Field

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
    token_type: str
    user_id: int