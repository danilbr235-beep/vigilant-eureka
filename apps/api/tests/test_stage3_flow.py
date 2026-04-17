from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.core.encryption import code_encryption
from app.db.base import Base
from app.models import (
    CodeStatus,
    OrderStatus,
    PricingConfig,
    PurchaseBatch,
    SellNominal,
    SupplierCodeType,
    User,
    UserRole,
)
from app.services.inventory_service import InventoryService
from app.services.orders_service import OrdersService
from app.core.security import hash_password
from app.schemas.orders import OrderCreateRequest


def make_session() -> Session:
    engine = create_engine("sqlite+pysqlite:///:memory:", future=True)
    Base.metadata.create_all(engine)
    return Session(engine)


def bootstrap_entities(db: Session):
    user = User(email="op@test.local", password_hash=hash_password("pass"), role=UserRole.operator, is_active=True)
    nominal = SellNominal(currency="EUR", nominal=20, is_active=True)
    code_type = SupplierCodeType(currency="SGD", nominal=10, is_active=True)
    batch = PurchaseBatch(supplier_name="demo")
    pricing = PricingConfig(
        marketplace_fee_percent=10,
        risk_reserve_percent=1,
        min_profit_rub=10,
        target_profit_percent=5,
        rounding_rule="ceil_10",
        max_codes_per_order=3,
        underfill_tolerance_percent=1,
        overfill_tolerance_percent=1,
        ad_allocation_mode="flat",
        default_ad_cost_per_sale=10,
        is_active=True,
    )
    db.add_all([user, nominal, code_type, batch, pricing])
    db.commit()
    return user, nominal, code_type, batch


def test_encryption_roundtrip():
    raw = "ABCD-EFGH-IJKL"
    enc = code_encryption.encrypt(raw)
    assert enc != raw
    assert code_encryption.decrypt(enc) == raw


def test_order_reserve_and_fulfill_flow():
    db = make_session()
    user, nominal, code_type, batch = bootstrap_entities(db)

    inv = InventoryService(db)
    c1 = inv.create_code(
        supplier_code_type_id=code_type.id,
        purchase_batch_id=batch.id,
        code="AAAA-BBBB-CCCC",
        cost_rub=100,
        actor_user_id=user.id,
    )

    order_service = OrdersService(db)
    order = order_service.create_order(
        OrderCreateRequest(
            external_order_id="ORD-1",
            sell_nominal_id=nominal.id,
            customer_currency="EUR",
            customer_nominal=20,
        ),
        actor_user_id=user.id,
    )

    order_service.reserve_codes(order_id=order.id, code_item_ids=[c1.id], actor_user_id=user.id)

    db.refresh(order)
    db.refresh(c1)
    assert order.status == OrderStatus.reserved
    assert c1.status == CodeStatus.reserved

    codes = order_service.fulfill(order_id=order.id, actor_user_id=user.id)
    db.refresh(order)
    db.refresh(c1)
    assert order.status == OrderStatus.fulfilled
    assert c1.status == CodeStatus.sent
    assert codes == ["AAAA-BBBB-CCCC"]
