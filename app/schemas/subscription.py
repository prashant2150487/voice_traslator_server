import uuid
from datetime import datetime

from pydantic import BaseModel
from app.schemas.plan import PlanBrief

class SubscriptionBrief(BaseModel):
    id: uuid.UUID
    status: str
    seats: int
    current_period_end: datetime | None
    plan: PlanBrief


