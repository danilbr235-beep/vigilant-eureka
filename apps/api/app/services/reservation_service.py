from datetime import datetime, timedelta, timezone

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.locks import lock_store
from app.models import CodeItem, CodeStatus, Order, OrderStatus
from app.services.audit_service import AuditService


class ReservationService:
    def __init__(self, db: Session):
        self.db = db
        self.audit = AuditService(db)

    def reserve_with_idempotency(
        self,
        *,
        order_id: int,
        code_item_ids: list[int],
        actor_user_id: int,
        idempotency_key: str,
    ) -> dict:
        lock_key = f"reserve:{order_id}:{idempotency_key}"
        if not lock_store.set_nx(lock_key, "1", ttl_seconds=settings.reservation_ttl_minutes * 60):
            raise ValueError("Duplicate reserve request")

        order = self.db.get(Order, order_id)
        if not order:
            raise ValueError("Order not found")

        stmt = select(CodeItem).where(CodeItem.id.in_(code_item_ids))
        items = list(self.db.scalars(stmt).all())
        if len(items) != len(code_item_ids):
            raise ValueError("Some codes not found")

        expires_at = (datetime.now(timezone.utc) + timedelta(minutes=settings.reservation_ttl_minutes)).replace(microsecond=0)
        for item in items:
            if item.status != CodeStatus.new:
                raise ValueError(f"Code {item.id} not available")
            item.status = CodeStatus.reserved
            item.current_order_id = order_id
            item.reserved_until = expires_at

        order.status = OrderStatus.reserved
        self.audit.log(
            actor_user_id=actor_user_id,
            action="orders.codes_reserved",
            entity_type="order",
            entity_id=str(order_id),
            payload={"code_item_ids": code_item_ids, "idempotency_key": idempotency_key},
        )
        self.db.commit()
        return {"order_id": order_id, "reserved_count": len(items)}

    def clear_expired_reservations(self) -> int:
        now = datetime.now(timezone.utc)
        stmt = select(CodeItem).where(CodeItem.status == CodeStatus.reserved, CodeItem.reserved_until.is_not(None))
        items = list(self.db.scalars(stmt).all())
        cleared = 0
        for item in items:
            if item.reserved_until and item.reserved_until <= now:
                item.status = CodeStatus.new
                item.current_order_id = None
                item.reserved_until = None
                cleared += 1

        if cleared:
            self.db.commit()
        return cleared
