from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import require_roles
from app.db.session import get_db
from app.models import UserRole
from app.schemas.settings import PricingConfigPatch
from app.services.settings_service import SettingsService

router = APIRouter(prefix="/settings", tags=["settings"])


@router.get("")
def get_settings(db: Session = Depends(get_db), _=Depends(require_roles(UserRole.admin, UserRole.operator, UserRole.viewer))):
    obj = SettingsService(db).get_active_pricing()
    return {"pricing_config": None if not obj else {
        "marketplace_fee_percent": float(obj.marketplace_fee_percent),
        "risk_reserve_percent": float(obj.risk_reserve_percent),
        "min_profit_rub": float(obj.min_profit_rub),
        "target_profit_percent": float(obj.target_profit_percent),
        "default_ad_cost_per_sale": float(obj.default_ad_cost_per_sale),
    }}


@router.patch("")
def patch_settings(payload: PricingConfigPatch, db: Session = Depends(get_db), _=Depends(require_roles(UserRole.admin))):
    obj = SettingsService(db).patch_active_pricing(**payload.model_dump())
    return {"updated": True, "id": obj.id}


@router.get("/promotion-rules")
def promotion_rules(_=Depends(require_roles(UserRole.admin, UserRole.operator, UserRole.viewer))):
    return {"items": []}


@router.post("/promotion-rules")
def create_promotion_rule(_=Depends(require_roles(UserRole.admin))):
    return {"created": True, "message": "Stage 2 foundation"}
