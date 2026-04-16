from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, require_roles
from app.db.session import get_db
from app.models import CodeStatus, UserRole
from app.schemas.inventory import CodeCreateRequest, CodeResponse, CodeRevealResponse
from app.services.inventory_service import InventoryService

router = APIRouter(prefix="/inventory", tags=["inventory"])


@router.get("/batches")
def batches(_=Depends(require_roles(UserRole.admin, UserRole.operator, UserRole.viewer))):
    return {"items": []}


@router.post("/import")
def import_codes(_=Depends(require_roles(UserRole.admin, UserRole.operator))):
    return {"imported": 0}


@router.post("/codes", response_model=CodeResponse)
def add_code(payload: CodeCreateRequest, db: Session = Depends(get_db), user=Depends(get_current_user)):
    item = InventoryService(db).create_code(**payload.model_dump(), actor_user_id=user.id)
    return CodeResponse(id=item.id, masked_code=item.masked_code, status=item.status, cost_rub=float(item.cost_rub))


@router.get("/codes", response_model=list[CodeResponse])
def list_codes(status: CodeStatus | None = None, db: Session = Depends(get_db), _=Depends(require_roles(UserRole.admin, UserRole.operator, UserRole.viewer))):
    rows = InventoryService(db).list_codes(status=status)
    return [CodeResponse(id=r.id, masked_code=r.masked_code, status=r.status, cost_rub=float(r.cost_rub)) for r in rows]


@router.get("/codes/{code_id}/reveal", response_model=CodeRevealResponse)
def reveal_code(code_id: int, db: Session = Depends(get_db), user=Depends(require_roles(UserRole.admin, UserRole.operator))):
    try:
        code = InventoryService(db).reveal_code(code_id=code_id, actor_user_id=user.id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc))
    return CodeRevealResponse(id=code_id, code=code)


@router.patch("/codes/{code_id}/status")
def patch_code_status(code_id: int, _=Depends(require_roles(UserRole.admin, UserRole.operator))):
    return {"id": code_id, "updated": True}


@router.get("/stock-summary")
def stock_summary(_=Depends(require_roles(UserRole.admin, UserRole.operator, UserRole.viewer))):
    return {"items": []}
