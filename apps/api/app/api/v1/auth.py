from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.schemas.auth import LoginRequest, MeResponse, RefreshRequest, TokenResponse, Verify2FARequest
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)) -> TokenResponse:
    access_token, refresh_token, user = AuthService(db).login(payload.email, payload.password)
    return TokenResponse(access_token=access_token, refresh_token=refresh_token, role=user.role)


@router.post("/refresh", response_model=TokenResponse)
def refresh(payload: RefreshRequest, db: Session = Depends(get_db)) -> TokenResponse:
    access_token, refresh_token, user = AuthService(db).refresh(payload.refresh_token)
    return TokenResponse(access_token=access_token, refresh_token=refresh_token, role=user.role)


@router.post("/logout")
def logout() -> dict:
    # JWT stateless logout in MVP: client drops tokens
    return {"ok": True}


@router.post("/2fa/verify")
def verify_2fa(payload: Verify2FARequest) -> dict:
    # MVP stub: accept 6-digit shape only, enforce flow in next iteration.
    return {"verified": payload.otp_code.isdigit() and len(payload.otp_code) in {6, 8}}


@router.get("/me", response_model=MeResponse)
def me(user=Depends(get_current_user)) -> MeResponse:
    return MeResponse(id=user.id, email=user.email, role=user.role)
