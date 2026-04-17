from dataclasses import dataclass


@dataclass(slots=True)
class PricingConfigDTO:
    marketplace_fee_percent: float
    risk_reserve_percent: float
    min_profit_rub: float
    target_profit_percent: float
    default_ad_cost_per_sale: float
    underfill_tolerance_percent: float = 1.0
    overfill_tolerance_percent: float = 1.0


class PricingService:
    @staticmethod
    def evaluate_combo(
        *,
        combo_cost_rub: float,
        delivered_value: float,
        target_nominal: float,
        revenue_rub: float,
        cfg: PricingConfigDTO,
        ad_cost_rub: float | None = None,
    ) -> dict:
        ad_cost = cfg.default_ad_cost_per_sale if ad_cost_rub is None else ad_cost_rub

        reserve_rub = combo_cost_rub * cfg.risk_reserve_percent / 100
        target_profit_rub = max(
            combo_cost_rub * cfg.target_profit_percent / 100,
            cfg.min_profit_rub,
        )
        base_required_rub = combo_cost_rub + ad_cost + reserve_rub + target_profit_rub
        recommended_price_rub = base_required_rub / (1 - cfg.marketplace_fee_percent / 100)

        marketplace_fee_rub = revenue_rub * cfg.marketplace_fee_percent / 100
        net_profit_rub = revenue_rub - marketplace_fee_rub - combo_cost_rub - ad_cost - reserve_rub
        margin_percent = (net_profit_rub / revenue_rub * 100) if revenue_rub else 0.0
        deviation_percent = abs(delivered_value - target_nominal) / target_nominal * 100

        min_allowed = target_nominal * (1 - cfg.underfill_tolerance_percent / 100)
        max_allowed = target_nominal * (1 + cfg.overfill_tolerance_percent / 100)
        valid = min_allowed <= delivered_value <= max_allowed

        return {
            "reserve_rub": reserve_rub,
            "target_profit_rub": target_profit_rub,
            "base_required_rub": base_required_rub,
            "recommended_price_rub": recommended_price_rub,
            "marketplace_fee_rub": marketplace_fee_rub,
            "net_profit_rub": net_profit_rub,
            "margin_percent": margin_percent,
            "deviation_percent": deviation_percent,
            "valid": valid,
        }
