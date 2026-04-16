from fastapi import APIRouter, Depends

from app.api.deps import require_roles
from app.models import UserRole

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/summary")
def summary(_=Depends(require_roles(UserRole.admin, UserRole.operator, UserRole.viewer))):
    return {"profit_today": 0, "avg_margin": 0}


@router.get("/charts")
def charts(_=Depends(require_roles(UserRole.admin, UserRole.operator, UserRole.viewer))):
    return {"series": []}
