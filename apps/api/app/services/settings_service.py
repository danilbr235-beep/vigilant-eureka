from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import PricingConfig


class SettingsService:
    def __init__(self, db: Session):
        self.db = db

    def get_active_pricing(self) -> PricingConfig | None:
        return self.db.scalar(select(PricingConfig).where(PricingConfig.is_active.is_(True)).order_by(PricingConfig.id.desc()))

    def patch_active_pricing(self, **fields) -> PricingConfig:
        obj = self.get_active_pricing()
        if obj is None:
            obj = PricingConfig(
                marketplace_fee_percent=10,
                risk_reserve_percent=3,
                min_profit_rub=50,
                target_profit_percent=8,
                rounding_rule="ceil_10",
                max_codes_per_order=3,
                underfill_tolerance_percent=1.5,
                overfill_tolerance_percent=1.5,
                ad_allocation_mode="flat",
                default_ad_cost_per_sale=30,
                is_active=True,
            )
            self.db.add(obj)

        for key, value in fields.items():
            if value is not None and hasattr(obj, key):
                setattr(obj, key, value)

        self.db.commit()
        self.db.refresh(obj)
        return obj
