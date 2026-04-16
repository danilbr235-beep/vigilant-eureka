from pydantic import BaseModel


class OrderCreateRequest(BaseModel):
    external_order_id: str
    sell_nominal_id: int
    customer_currency: str
    customer_nominal: float


class OrderReserveRequest(BaseModel):
    code_item_ids: list[int]


class OrderFulfillResponse(BaseModel):
    order_id: int
    revealed_codes: list[str]
