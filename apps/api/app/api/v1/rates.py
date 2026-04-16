from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import require_roles
from app.db.session import get_db
from app.models import UserRole
from app.schemas.rates import RateManualUpsertRequest, RateResponse
from app.services.rates_service import RatesService

router = APIRouter(prefix="/rates", tags=["rates"])


@router.get("", response_model=list[RateResponse])
def list_rates(db: Session = Depends(get_db), _=Depends(require_roles(UserRole.admin, UserRole.operator, UserRole.viewer))):
    rows = RatesService(db).list_latest()
    return [
        RateResponse(
            from_currency=r.from_currency,
            to_currency=r.to_currency,
            rate=float(r.rate),
            source=r.source,
            fetched_at=r.fetched_at,
        )
        for r in rows
    ]


@router.post("/manual", response_model=RateResponse)
def manual_rate(payload: RateManualUpsertRequest, db: Session = Depends(get_db), _=Depends(require_roles(UserRole.admin))):
    row = RatesService(db).upsert_manual(**payload.model_dump())
    return RateResponse(
        from_currency=row.from_currency,
        to_currency=row.to_currency,
        rate=float(row.rate),
        source=row.source,
        fetched_at=row.fetched_at,
    )


@router.post("/fetch")
def fetch_rates(_=Depends(require_roles(UserRole.admin))):
    return {"queued": True, "source": "mock"}


@router.get("/history")
def history(_=Depends(require_roles(UserRole.admin, UserRole.operator, UserRole.viewer))):
    return {"items": []}
