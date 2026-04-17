from pydantic import BaseModel, EmailStr

from app.models import UserRole


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class RefreshRequest(BaseModel):
    refresh_token: str


class Verify2FARequest(BaseModel):
    otp_code: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    role: UserRole


class MeResponse(BaseModel):
    id: int
    email: EmailStr
    role: UserRole
