from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import require_roles
from app.db.session import get_db
from app.models import PromotionCostRule, UserRole
from app.schemas.settings import PricingConfigPatch
from app.services.audit_service import AuditService
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
def patch_settings(payload: PricingConfigPatch, db: Session = Depends(get_db), user=Depends(require_roles(UserRole.admin))):
    obj = SettingsService(db).patch_active_pricing(**payload.model_dump())
    AuditService(db).log(
        actor_user_id=user.id,
        action="settings.pricing.updated",
        entity_type="pricing_config",
        entity_id=str(obj.id),
        payload=payload.model_dump(exclude_none=True),
    )
    db.commit()
    return {"updated": True, "id": obj.id}


@router.get("/promotion-rules")
def promotion_rules(db: Session = Depends(get_db), _=Depends(require_roles(UserRole.admin, UserRole.operator, UserRole.viewer))):
    rows = db.scalars(select(PromotionCostRule).order_by(PromotionCostRule.id.desc()).limit(200)).all()
    return {
        "items": [
            {
                "id": r.id,
                "name": r.name,
                "currency": r.currency,
                "nominal_min": float(r.nominal_min) if r.nominal_min is not None else None,
                "nominal_max": float(r.nominal_max) if r.nominal_max is not None else None,
                "ad_cost_rub": float(r.ad_cost_rub),
                "is_active": bool(r.is_active),
            }
            for r in rows
        ]
    }


@router.post("/promotion-rules")
def create_promotion_rule(
    payload: dict,
    db: Session = Depends(get_db),
    user=Depends(require_roles(UserRole.admin)),
):
    row = PromotionCostRule(
        name=payload.get("name", "rule"),
        currency=payload.get("currency"),
        nominal_min=payload.get("nominal_min"),
        nominal_max=payload.get("nominal_max"),
        ad_cost_rub=payload.get("ad_cost_rub", 0),
        is_active=payload.get("is_active", True),
    )
    db.add(row)
    db.flush()
    AuditService(db).log(
        actor_user_id=user.id,
        action="settings.promotion_rule.created",
        entity_type="promotion_cost_rule",
        entity_id=str(row.id),
        payload={"name": row.name},
    )
    db.commit()
    return {"created": True, "id": row.id}
