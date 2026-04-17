from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.db.base import Base
from app.models import CodeStatus, OrderStatus, PurchaseBatch, SupplierCodeType, User, UserRole
from app.schemas.orders import OrderCreateRequest
from app.services.inventory_service import InventoryService
from app.services.orders_service import OrdersService


def make_session() -> Session:
    engine = create_engine("sqlite+pysqlite:///:memory:", future=True)
    Base.metadata.create_all(engine)
    return Session(engine)


def test_inventory_status_update_and_order_problem_complete():
    db = make_session()
    user = User(email="op@x.local", password_hash=hash_password("pass"), role=UserRole.operator, is_active=True)
    batch = PurchaseBatch(supplier_name="demo")
    code_type = SupplierCodeType(currency="SGD", nominal=10, is_active=True)
    db.add_all([user, batch, code_type])
    db.commit()

    inv = InventoryService(db)
    code = inv.create_code(
        supplier_code_type_id=code_type.id,
        purchase_batch_id=batch.id,
        code="ABCD-EFGH-IJKL",
        cost_rub=100,
        actor_user_id=user.id,
    )
    inv.update_status(code_id=code.id, new_status=CodeStatus.problem, actor_user_id=user.id)
    db.refresh(code)
    assert code.status == CodeStatus.problem

    orders = OrdersService(db)
    order = orders.create_order(
        OrderCreateRequest(external_order_id="EXT-1", sell_nominal_id=1, customer_currency="EUR", customer_nominal=20),
        actor_user_id=user.id,
    )
    orders.mark_problem(order_id=order.id, actor_user_id=user.id, reason="manual")
    db.refresh(order)
    assert order.status == OrderStatus.problem

    orders.complete(order_id=order.id, actor_user_id=user.id)
    db.refresh(order)
    assert order.status == OrderStatus.completed
