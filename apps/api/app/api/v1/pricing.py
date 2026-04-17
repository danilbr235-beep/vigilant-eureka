from fastapi import APIRouter, Depends

from app.api.deps import require_roles
from app.models import UserRole
from app.schemas.pricing import ComboEvaluationInput, ComboEvaluationResponse, PricingConfigInput
from app.services.pricing_service import PricingConfigDTO, PricingService

router = APIRouter(prefix="/pricing", tags=["pricing"])


@router.post("/simulate", response_model=ComboEvaluationResponse)
def simulate(payload: ComboEvaluationInput, cfg: PricingConfigInput, _=Depends(require_roles(UserRole.admin, UserRole.operator, UserRole.viewer))):
    result = PricingService.evaluate_combo(
        combo_cost_rub=payload.combo_cost_rub,
        delivered_value=payload.delivered_value,
        target_nominal=payload.target_nominal,
        revenue_rub=payload.revenue_rub,
        ad_cost_rub=payload.ad_cost_rub,
        cfg=PricingConfigDTO(**cfg.model_dump()),
    )
    return ComboEvaluationResponse(**result)


@router.get("/recommendations")
def recommendations(_=Depends(require_roles(UserRole.admin, UserRole.operator, UserRole.viewer))):
    return {"items": [], "message": "Stage 2 foundation: recommendations engine to be connected next"}


@router.post("/recalculate")
def recalculate(_=Depends(require_roles(UserRole.admin))):
    return {"queued": True}


@router.get("/snapshots")
def snapshots(_=Depends(require_roles(UserRole.admin, UserRole.operator, UserRole.viewer))):
    return {"items": []}
