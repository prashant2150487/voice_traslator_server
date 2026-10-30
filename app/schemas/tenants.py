import datetime
import uuid
from typing import Any , Annotated

from pydantic import BaseModel , StringConstraints , EmailStr, Field , field_validator

from app.schemas.subscription import SubscriptionBrief

Slug = Annotated[str, StringConstraints(pattern=r"^[a-z0-9]([a-z0-9-]{0,61}[a-z0-9])?$")]
class TenantsListItem(BaseModel):
    id: uuid.UUID
    name: str
    slug: str
    status: str
    owner_user_id: uuid.UUID | None
    default_language: str | None
    user_count: int
    subscription: SubscriptionBrief | None


class TenantDetail(TenantsListItem):
    data_region: str | None
    settings: dict[str,Any] | None
    updated_at : datetime.datetime | None

class TenantAdminCreate(BaseModel):
    email: EmailStr
    display_name: str = Field(min_length=1, max_length=100)
    password: str = Field(min_length=12, max_length=128)

    @field_validator("email")
    @classmethod
    def lower_email(cls, v: str) -> str:
        return v.lower()

# class TenantsCreate(BaseModel):
#     name: str
#     slug: Slug
#     default_language: str | None = Field(default= None , max_length = 150)
#     plan_id = uuid.UUID
#     admin: TenantAdminCreate | None = None













