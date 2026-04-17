from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import require_roles
from app.db.session import get_db
from app.models import Order, UserRole
from app.schemas.orders import OrderCreateRequest, OrderFulfillResponse, OrderReserveRequest
from app.services.orders_service import OrdersService
from app.services.reservation_service import ReservationService

router = APIRouter(prefix="/orders", tags=["orders"])


@router.get("")
def list_orders(db: Session = Depends(get_db), _=Depends(require_roles(UserRole.admin, UserRole.operator, UserRole.viewer))):
    rows = db.query(Order).order_by(Order.id.desc()).all()
    return {"items": [{"id": x.id, "status": x.status, "external_order_id": x.external_order_id} for x in rows]}


@router.post("")
def create_order(payload: OrderCreateRequest, db: Session = Depends(get_db), user=Depends(require_roles(UserRole.admin, UserRole.operator))):
    row = OrdersService(db).create_order(payload, actor_user_id=user.id)
    return {"created": True, "id": row.id}


@router.get("/{order_id}")
def get_order(order_id: int, db: Session = Depends(get_db), _=Depends(require_roles(UserRole.admin, UserRole.operator, UserRole.viewer))):
    row = db.get(Order, order_id)
    if not row:
        raise HTTPException(status_code=404, detail="Order not found")
    return {"id": row.id, "status": row.status, "external_order_id": row.external_order_id}


@router.post("/{order_id}/reserve")
def reserve(
    order_id: int,
    payload: OrderReserveRequest,
    db: Session = Depends(get_db),
    user=Depends(require_roles(UserRole.admin, UserRole.operator)),
    x_idempotency_key: str = Header(default="", alias="X-Idempotency-Key"),
):
    if not x_idempotency_key:
        raise HTTPException(status_code=400, detail="X-Idempotency-Key is required")

    try:
        result = ReservationService(db).reserve_with_idempotency(
            order_id=order_id,
            code_item_ids=payload.code_item_ids,
            actor_user_id=user.id,
            idempotency_key=x_idempotency_key,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    return {"id": result["order_id"], "reserved": True, "reserved_count": result["reserved_count"]}


@router.post("/{order_id}/fulfill", response_model=OrderFulfillResponse)
def fulfill(order_id: int, db: Session = Depends(get_db), user=Depends(require_roles(UserRole.admin, UserRole.operator))):
    try:
        codes = OrdersService(db).fulfill(order_id=order_id, actor_user_id=user.id)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    return OrderFulfillResponse(order_id=order_id, revealed_codes=codes)


@router.post("/{order_id}/problem")
def problem(order_id: int, db: Session = Depends(get_db), user=Depends(require_roles(UserRole.admin, UserRole.operator))):
    try:
        row = OrdersService(db).mark_problem(order_id=order_id, actor_user_id=user.id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc))
    return {"id": row.id, "problem": True, "status": row.status}


@router.post("/{order_id}/complete")
def complete(order_id: int, db: Session = Depends(get_db), user=Depends(require_roles(UserRole.admin, UserRole.operator))):
    try:
        row = OrdersService(db).complete(order_id=order_id, actor_user_id=user.id)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    return {"id": row.id, "completed": True, "status": row.status}


@router.post("/reservations/clear-expired")
def clear_expired(db: Session = Depends(get_db), _=Depends(require_roles(UserRole.admin))):
    cleared = ReservationService(db).clear_expired_reservations()
    return {"cleared": cleared}
