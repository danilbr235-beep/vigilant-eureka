from datetime import datetime, timedelta, timezone

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.db.base import Base
from app.models import CodeItem, CodeStatus, Order, OrderStatus, PurchaseBatch, SellNominal, SupplierCodeType, User, UserRole
from app.services.inventory_service import InventoryService
from app.services.reservation_service import ReservationService
from app.core.security import hash_password


def make_session() -> Session:
    engine = create_engine("sqlite+pysqlite:///:memory:", future=True)
    Base.metadata.create_all(engine)
    return Session(engine)


def setup_data(db: Session):
    user = User(email="admin@test.local", password_hash=hash_password("pass"), role=UserRole.admin, is_active=True)
    nominal = SellNominal(currency="EUR", nominal=20, is_active=True)
    db.add_all([user, nominal])
    db.flush()

    order = Order(
        external_order_id="ORD-IDEMP-1",
        sell_nominal_id=nominal.id,
        status=OrderStatus.new,
        customer_currency="EUR",
        customer_nominal=20,
        manual_review=False,
    )
    code_type = SupplierCodeType(currency="SGD", nominal=10, is_active=True)
    batch = PurchaseBatch(supplier_name="demo")
    db.add_all([order, code_type, batch])
    db.commit()
    return user, order, code_type, batch


def test_double_reserve_blocked_by_idempotency():
    db = make_session()
    user, order, code_type, batch = setup_data(db)
    code = InventoryService(db).create_code(
        supplier_code_type_id=code_type.id,
        purchase_batch_id=batch.id,
        code="AAAA-BBBB-CCCC",
        cost_rub=50,
        actor_user_id=user.id,
    )

    service = ReservationService(db)
    service.reserve_with_idempotency(
        order_id=order.id,
        code_item_ids=[code.id],
        actor_user_id=user.id,
        idempotency_key="dup-key",
    )

    try:
        service.reserve_with_idempotency(
            order_id=order.id,
            code_item_ids=[code.id],
            actor_user_id=user.id,
            idempotency_key="dup-key",
        )
        assert False, "expected duplicate reserve to fail"
    except ValueError as exc:
        assert "Duplicate" in str(exc)


def test_clear_expired_reservations_releases_codes():
    db = make_session()
    user, order, code_type, batch = setup_data(db)
    code = InventoryService(db).create_code(
        supplier_code_type_id=code_type.id,
        purchase_batch_id=batch.id,
        code="ZZZZ-YYYY-XXXX",
        cost_rub=60,
        actor_user_id=user.id,
    )

    service = ReservationService(db)
    service.reserve_with_idempotency(
        order_id=order.id,
        code_item_ids=[code.id],
        actor_user_id=user.id,
        idempotency_key="ttl-key",
    )

    row = db.get(CodeItem, code.id)
    row.reserved_until = datetime.now(timezone.utc) - timedelta(minutes=1)
    db.commit()

    cleared = service.clear_expired_reservations()
    row = db.get(CodeItem, code.id)
    assert cleared >= 1
    assert row.status == CodeStatus.new
    assert row.current_order_id is None
