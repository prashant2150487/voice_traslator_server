import uuid

from pydantic import BaseModel
from app.schemas.subscription import SubscriptionBrief


class TenantsListItem(BaseModel):
    id: uuid.UUID
    name: str
    slug: str
    status: str
    owner_user_id: uuid.UUID | None
    default_language: str | None
    user_count: int
    subscription: SubscriptionBrief | None



