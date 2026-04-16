from __future__ import annotations

from decimal import Decimal

from sqlalchemy import select

from app.core.security import hash_password
from app.db.session import SessionLocal
from app.models import (
    CodeItem,
    CodeStatus,
    FxRate,
    PricingConfig,
    PromotionCostRule,
    PurchaseBatch,
    SellNominal,
    SupplierCodeType,
    User,
    UserRole,
)
from app.core.encryption import code_encryption


USD_EUR_NOMINALS = [1, 2, 5] + list(range(10, 101, 5)) + [200, 300, 400, 500, 1000]
KZT_NOMINALS = [500, 1000, 2500, 5000, 10000, 15000, 25000, 50000, 75000, 100000]
CNY_NOMINALS = [6, 15, 36, 100, 200, 350, 700, 1000]

SGD_CODES = [10, 20, 30, 40, 50, 100]
MYR_CODES = [5, 8, 10, 13, 15, 20]


DEMO_USERS = [
    ("admin@calcsteam.local", "admin123", UserRole.admin),
    ("operator@calcsteam.local", "operator123", UserRole.operator),
    ("viewer@calcsteam.local", "viewer123", UserRole.viewer),
]


def _upsert_user(db, email: str, password: str, role: UserRole) -> None:
    row = db.scalar(select(User).where(User.email == email))
    if row:
        row.password_hash = hash_password(password)
        row.role = role
        row.is_active = True
    else:
        db.add(User(email=email, password_hash=hash_password(password), role=role, is_active=True))


def _ensure_sell_nominals(db) -> None:
    for currency in ("USD", "EUR"):
        for n in USD_EUR_NOMINALS:
            exists = db.scalar(select(SellNominal).where(SellNominal.currency == currency, SellNominal.nominal == n))
            if not exists:
                db.add(SellNominal(currency=currency, nominal=n, is_active=True))

    for n in KZT_NOMINALS:
        exists = db.scalar(select(SellNominal).where(SellNominal.currency == "KZT", SellNominal.nominal == n))
        if not exists:
            db.add(SellNominal(currency="KZT", nominal=n, is_active=True))

    for n in CNY_NOMINALS:
        exists = db.scalar(select(SellNominal).where(SellNominal.currency == "CNY", SellNominal.nominal == n))
        if not exists:
            db.add(SellNominal(currency="CNY", nominal=n, is_active=True))


def _ensure_supplier_code_types(db) -> list[SupplierCodeType]:
    result: list[SupplierCodeType] = []
    for n in SGD_CODES:
        row = db.scalar(select(SupplierCodeType).where(SupplierCodeType.currency == "SGD", SupplierCodeType.nominal == n))
        if not row:
            row = SupplierCodeType(currency="SGD", nominal=n, is_active=True)
            db.add(row)
        result.append(row)

    for n in MYR_CODES:
        row = db.scalar(select(SupplierCodeType).where(SupplierCodeType.currency == "MYR", SupplierCodeType.nominal == n))
        if not row:
            row = SupplierCodeType(currency="MYR", nominal=n, is_active=True)
            db.add(row)
        result.append(row)

    return result


def _ensure_pricing_defaults(db) -> None:
    if not db.scalar(select(PricingConfig).where(PricingConfig.is_active.is_(True))):
        db.add(
            PricingConfig(
                marketplace_fee_percent=Decimal("10.0"),
                risk_reserve_percent=Decimal("3.0"),
                min_profit_rub=Decimal("50.0"),
                target_profit_percent=Decimal("8.0"),
                rounding_rule="ceil_10",
                max_codes_per_order=3,
                underfill_tolerance_percent=Decimal("1.5"),
                overfill_tolerance_percent=Decimal("1.5"),
                ad_allocation_mode="flat",
                default_ad_cost_per_sale=Decimal("30.0"),
                is_active=True,
            )
        )

    if not db.scalar(select(PromotionCostRule).where(PromotionCostRule.name == "default_flat")):
        db.add(
            PromotionCostRule(
                name="default_flat",
                currency=None,
                nominal_min=None,
                nominal_max=None,
                ad_cost_rub=Decimal("30.0"),
                is_active=True,
            )
        )


def _ensure_demo_batch_and_codes(db, code_types: list[SupplierCodeType]) -> None:
    batch = db.scalar(select(PurchaseBatch).where(PurchaseBatch.supplier_name == "demo-supplier"))
    if not batch:
        batch = PurchaseBatch(supplier_name="demo-supplier", notes="seed data")
        db.add(batch)
        db.flush()

    if db.scalar(select(CodeItem.id).limit(1)):
        return

    for idx, ct in enumerate(code_types[:8], start=1):
        raw = f"SEED-{ct.currency}-{int(ct.nominal)}-{idx:04d}"
        db.add(
            CodeItem(
                supplier_code_type_id=ct.id,
                purchase_batch_id=batch.id,
                encrypted_code=code_encryption.encrypt(raw),
                masked_code=f"****{raw[-4:]}",
                cost_rub=Decimal("100.0") + idx,
                status=CodeStatus.new,
            )
        )


def _ensure_demo_rates(db) -> None:
    pairs = [
        ("EUR", "RUB", Decimal("99.5")),
        ("USD", "RUB", Decimal("92.3")),
        ("KZT", "RUB", Decimal("0.19")),
        ("CNY", "RUB", Decimal("12.7")),
        ("SGD", "RUB", Decimal("68.2")),
        ("MYR", "RUB", Decimal("20.1")),
    ]
    for f, t, rate in pairs:
        exists = db.scalar(select(FxRate).where(FxRate.from_currency == f, FxRate.to_currency == t))
        if not exists:
            db.add(FxRate(from_currency=f, to_currency=t, rate=rate, source="seed"))


def seed_all() -> None:
    with SessionLocal() as db:
        for email, pwd, role in DEMO_USERS:
            _upsert_user(db, email, pwd, role)

        _ensure_sell_nominals(db)
        code_types = _ensure_supplier_code_types(db)
        db.flush()
        _ensure_pricing_defaults(db)
        _ensure_demo_batch_and_codes(db, code_types)
        _ensure_demo_rates(db)
        db.commit()


if __name__ == "__main__":
    seed_all()
    print("Seed completed")
