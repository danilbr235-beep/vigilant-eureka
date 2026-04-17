from datetime import datetime

from pydantic import BaseModel


class RateManualUpsertRequest(BaseModel):
    from_currency: str
    to_currency: str
    rate: float
    source: str = "manual"


class RateResponse(BaseModel):
    from_currency: str
    to_currency: str
    rate: float
    source: str
    fetched_at: datetime
