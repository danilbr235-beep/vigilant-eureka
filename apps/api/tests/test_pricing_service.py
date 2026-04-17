from app.services.pricing_service import PricingConfigDTO, PricingService


def test_formula_and_margin_calculation():
    cfg = PricingConfigDTO(
        marketplace_fee_percent=10,
        risk_reserve_percent=5,
        min_profit_rub=50,
        target_profit_percent=20,
        default_ad_cost_per_sale=30,
        underfill_tolerance_percent=2,
        overfill_tolerance_percent=2,
    )

    result = PricingService.evaluate_combo(
        combo_cost_rub=200,
        delivered_value=100,
        target_nominal=100,
        revenue_rub=400,
        cfg=cfg,
    )

    assert round(result["reserve_rub"], 2) == 10.00
    assert round(result["target_profit_rub"], 2) == 50.00
    assert round(result["base_required_rub"], 2) == 290.00
    assert round(result["recommended_price_rub"], 2) == round(290 / 0.9, 2)
    assert result["valid"] is True


def test_tolerance_validation_out_of_bounds():
    cfg = PricingConfigDTO(
        marketplace_fee_percent=10,
        risk_reserve_percent=1,
        min_profit_rub=10,
        target_profit_percent=5,
        default_ad_cost_per_sale=10,
        underfill_tolerance_percent=1,
        overfill_tolerance_percent=1,
    )

    result = PricingService.evaluate_combo(
        combo_cost_rub=100,
        delivered_value=96,
        target_nominal=100,
        revenue_rub=200,
        cfg=cfg,
    )

    assert result["valid"] is False
