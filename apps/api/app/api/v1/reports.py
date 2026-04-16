from fastapi import APIRouter, Depends

from app.api.deps import require_roles
from app.models import UserRole

router = APIRouter(prefix="/reports", tags=["reports"])


@router.get("/profit")
def profit(_=Depends(require_roles(UserRole.admin, UserRole.viewer, UserRole.operator))):
    return {"items": []}


@router.get("/orders")
def orders(_=Depends(require_roles(UserRole.admin, UserRole.viewer, UserRole.operator))):
    return {"items": []}


@router.get("/problems")
def problems(_=Depends(require_roles(UserRole.admin, UserRole.viewer, UserRole.operator))):
    return {"items": []}


@router.get("/audit")
def audit(_=Depends(require_roles(UserRole.admin, UserRole.viewer))):
    return {"items": []}
