from pydantic import BaseModel

from app.models import CodeStatus


class CodeCreateRequest(BaseModel):
    supplier_code_type_id: int
    purchase_batch_id: int
    code: str
    cost_rub: float


class CodeResponse(BaseModel):
    id: int
    masked_code: str
    status: CodeStatus
    cost_rub: float


class CodeRevealResponse(BaseModel):
    id: int
    code: str
