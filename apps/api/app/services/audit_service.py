from sqlalchemy.orm import Session

from app.models import AuditLog


class AuditService:
    def __init__(self, db: Session):
        self.db = db

    def log(self, *, actor_user_id: int | None, action: str, entity_type: str, entity_id: str, payload: dict | None = None) -> None:
        self.db.add(
            AuditLog(
                actor_user_id=actor_user_id,
                action=action,
                entity_type=entity_type,
                entity_id=entity_id,
                payload=payload or {},
            )
        )
