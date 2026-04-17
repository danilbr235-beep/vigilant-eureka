from datetime import datetime, timedelta, timezone

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.encryption import code_encryption
from app.models import CodeItem, CodeStatus, Order, OrderFulfillment, OrderStatus
from app.schemas.orders import OrderCreateRequest
from app.services.audit_service import AuditService


class OrdersService:
    def __init__(self, db: Session):
        self.db = db
        self.audit = AuditService(db)

    def create_order(self, payload: OrderCreateRequest, actor_user_id: int) -> Order:
        order = Order(
            external_order_id=payload.external_order_id,
            sell_nominal_id=payload.sell_nominal_id,
            status=OrderStatus.new,
            customer_currency=payload.customer_currency,
            customer_nominal=payload.customer_nominal,
            manual_review=False,
        )
        self.db.add(order)
        self.audit.log(actor_user_id=actor_user_id, action="orders.created", entity_type="order", entity_id="new")
        self.db.commit()
        self.db.refresh(order)
        return order

    def reserve_codes(self, *, order_id: int, code_item_ids: list[int], actor_user_id: int) -> Order:
        order = self.db.get(Order, order_id)
        if not order:
            raise ValueError("Order not found")

        now = datetime.now(timezone.utc)
        ttl = now + timedelta(minutes=settings.reservation_ttl_minutes)

        stmt = select(CodeItem).where(CodeItem.id.in_(code_item_ids))
        items = list(self.db.scalars(stmt).all())
        if len(items) != len(code_item_ids):
            raise ValueError("Some codes not found")

        for item in items:
            if item.status != CodeStatus.new:
                raise ValueError(f"Code {item.id} is not available")
            item.status = CodeStatus.reserved
            item.current_order_id = order_id
            item.reserved_until = ttl

        order.status = OrderStatus.reserved
        self.audit.log(
            actor_user_id=actor_user_id,
            action="orders.codes_reserved",
            entity_type="order",
            entity_id=str(order_id),
            payload={"code_item_ids": code_item_ids, "reserved_until": ttl.isoformat()},
        )
        self.db.commit()
        self.db.refresh(order)
        return order

    def fulfill(self, *, order_id: int, actor_user_id: int) -> list[str]:
        order = self.db.get(Order, order_id)
        if not order:
            raise ValueError("Order not found")

        stmt = select(CodeItem).where(CodeItem.current_order_id == order_id, CodeItem.status == CodeStatus.reserved)
        items = list(self.db.scalars(stmt).all())
        if not items:
            raise ValueError("No reserved codes for this order")

        revealed_codes: list[str] = []
        for item in items:
            revealed_codes.append(code_encryption.decrypt(item.encrypted_code))
            item.status = CodeStatus.sent
            item.reserved_until = None

        order.status = OrderStatus.fulfilled
        self.db.add(
            OrderFulfillment(
                order_id=order_id,
                operator_user_id=actor_user_id,
                delivered_payload={"code_item_ids": [i.id for i in items], "count": len(items)},
            )
        )
        self.audit.log(
            actor_user_id=actor_user_id,
            action="orders.fulfilled",
            entity_type="order",
            entity_id=str(order_id),
            payload={"code_item_ids": [i.id for i in items]},
        )
        self.db.commit()
        return revealed_codes

    def mark_problem(self, *, order_id: int, actor_user_id: int, reason: str | None = None) -> Order:
        order = self.db.get(Order, order_id)
        if not order:
            raise ValueError("Order not found")
        order.status = OrderStatus.problem
        order.manual_review = True
        self.audit.log(
            actor_user_id=actor_user_id,
            action="orders.problem",
            entity_type="order",
            entity_id=str(order_id),
            payload={"reason": reason},
        )
        self.db.commit()
        self.db.refresh(order)
        return order

    def complete(self, *, order_id: int, actor_user_id: int) -> Order:
        order = self.db.get(Order, order_id)
        if not order:
            raise ValueError("Order not found")
        if order.status not in {OrderStatus.fulfilled, OrderStatus.problem}:
            raise ValueError("Only fulfilled or problem order can be completed")
        order.status = OrderStatus.completed
        self.audit.log(
            actor_user_id=actor_user_id,
            action="orders.completed",
            entity_type="order",
            entity_id=str(order_id),
        )
        self.db.commit()
        self.db.refresh(order)
        return order
