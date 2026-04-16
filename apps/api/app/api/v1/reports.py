from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import require_roles
from app.db.session import get_db
from app.models import UserRole
from app.services.reports_service import ReportsService

router = APIRouter(prefix="/reports", tags=["reports"])


@router.get("/profit")
def profit(db: Session = Depends(get_db), _=Depends(require_roles(UserRole.admin, UserRole.viewer, UserRole.operator))):
    return ReportsService(db).report_profit()


@router.get("/orders")
def orders(db: Session = Depends(get_db), _=Depends(require_roles(UserRole.admin, UserRole.viewer, UserRole.operator))):
    return ReportsService(db).report_orders()


@router.get("/problems")
def problems(db: Session = Depends(get_db), _=Depends(require_roles(UserRole.admin, UserRole.viewer, UserRole.operator))):
    return ReportsService(db).report_problems()


@router.get("/audit")
def audit(db: Session = Depends(get_db), _=Depends(require_roles(UserRole.admin, UserRole.viewer))):
    return ReportsService(db).report_audit()
