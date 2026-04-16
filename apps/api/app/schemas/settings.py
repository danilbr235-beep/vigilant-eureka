from pydantic import BaseModel


class PricingConfigPatch(BaseModel):
    marketplace_fee_percent: float | None = None
    risk_reserve_percent: float | None = None
    min_profit_rub: float | None = None
    target_profit_percent: float | None = None
    default_ad_cost_per_sale: float | None = None
