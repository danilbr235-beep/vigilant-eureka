from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import FxRate


class RatesService:
    def __init__(self, db: Session):
        self.db = db

    def upsert_manual(self, *, from_currency: str, to_currency: str, rate: float, source: str = "manual") -> FxRate:
        item = FxRate(
            from_currency=from_currency.upper(),
            to_currency=to_currency.upper(),
            rate=rate,
            source=source,
            fetched_at=datetime.now(timezone.utc),
        )
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        return item

    def list_latest(self, limit: int = 100) -> list[FxRate]:
        stmt = select(FxRate).order_by(FxRate.fetched_at.desc()).limit(limit)
        return list(self.db.scalars(stmt).all())
