from pydantic import BaseModel, Field


class PricingConfigInput(BaseModel):
    marketplace_fee_percent: float
    risk_reserve_percent: float
    min_profit_rub: float
    target_profit_percent: float
    default_ad_cost_per_sale: float


class ComboEvaluationInput(BaseModel):
    combo_cost_rub: float = Field(gt=0)
    delivered_value: float = Field(gt=0)
    target_nominal: float = Field(gt=0)
    revenue_rub: float = Field(gt=0)
    ad_cost_rub: float | None = None


class ComboEvaluationResponse(BaseModel):
    reserve_rub: float
    target_profit_rub: float
    base_required_rub: float
    recommended_price_rub: float
    marketplace_fee_rub: float
    net_profit_rub: float
    margin_percent: float
    deviation_percent: float
    valid: bool
