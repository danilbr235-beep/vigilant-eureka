from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.encryption import code_encryption
from app.models import CodeItem, CodeStatus
from app.services.audit_service import AuditService


def _mask_code(value: str) -> str:
    if len(value) <= 4:
        return "*" * len(value)
    return f"{'*' * (len(value) - 4)}{value[-4:]}"


class InventoryService:
    def __init__(self, db: Session):
        self.db = db
        self.audit = AuditService(db)

    def create_code(self, *, supplier_code_type_id: int, purchase_batch_id: int, code: str, cost_rub: float, actor_user_id: int) -> CodeItem:
        item = CodeItem(
            supplier_code_type_id=supplier_code_type_id,
            purchase_batch_id=purchase_batch_id,
            encrypted_code=code_encryption.encrypt(code),
            masked_code=_mask_code(code),
            cost_rub=cost_rub,
            status=CodeStatus.new,
        )
        self.db.add(item)
        self.audit.log(
            actor_user_id=actor_user_id,
            action="inventory.code_created",
            entity_type="code_item",
            entity_id="new",
            payload={"supplier_code_type_id": supplier_code_type_id, "purchase_batch_id": purchase_batch_id},
        )
        self.db.commit()
        self.db.refresh(item)
        return item

    def list_codes(self, *, status: CodeStatus | None = None) -> list[CodeItem]:
        stmt = select(CodeItem).order_by(CodeItem.id.desc())
        if status:
            stmt = stmt.where(CodeItem.status == status)
        return list(self.db.scalars(stmt).all())

    def reveal_code(self, *, code_id: int, actor_user_id: int) -> str:
        item = self.db.get(CodeItem, code_id)
        if not item:
            raise ValueError("Code not found")
        plain = code_encryption.decrypt(item.encrypted_code)
        self.audit.log(
            actor_user_id=actor_user_id,
            action="inventory.code_revealed",
            entity_type="code_item",
            entity_id=str(code_id),
        )
        self.db.commit()
        return plain

    def update_status(self, *, code_id: int, new_status: CodeStatus, actor_user_id: int) -> CodeItem:
        item = self.db.get(CodeItem, code_id)
        if not item:
            raise ValueError("Code not found")

        item.status = new_status
        if new_status != CodeStatus.reserved:
            item.reserved_until = None
            item.current_order_id = None

        self.audit.log(
            actor_user_id=actor_user_id,
            action="inventory.code_status_updated",
            entity_type="code_item",
            entity_id=str(code_id),
            payload={"status": new_status.value},
        )
        self.db.commit()
        self.db.refresh(item)
        return item
