from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import require_roles
from app.db.session import get_db
from app.models import UserRole
from app.services.reports_service import ReportsService

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/summary")
def summary(db: Session = Depends(get_db), _=Depends(require_roles(UserRole.admin, UserRole.operator, UserRole.viewer))):
    return ReportsService(db).dashboard_summary()


@router.get("/charts")
def charts(db: Session = Depends(get_db), _=Depends(require_roles(UserRole.admin, UserRole.operator, UserRole.viewer))):
    return ReportsService(db).dashboard_charts()
