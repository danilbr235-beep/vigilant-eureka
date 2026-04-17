from contextlib import contextmanager

from sqlalchemy.orm import Session

from app.core.locks import lock_store
from app.db.session import SessionLocal
from app.services.reservation_service import ReservationService


@contextmanager
def session_scope():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def clear_expired_reservations_job() -> int:
    lock_key = "jobs:clear_expired_reservations"
    if not lock_store.set_nx(lock_key, "1", ttl_seconds=120):
        return 0

    with session_scope() as db:
        return ReservationService(db).clear_expired_reservations()
