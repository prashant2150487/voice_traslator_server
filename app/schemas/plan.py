
import uuid
from datetime import datetime
from decimal import Decimal
from typing import Any

from pydantic import BaseModel, ConfigDict, Field



class PlanLimits(BaseModel):
    """Keys follow the plan limits in your doc (12.6). Rename here if your names differ."""
    model_config = ConfigDict(extra="forbid")  # a typo in a key is an error, not silently stored
    max_seats: int = Field(ge=1)
    monthly_minutes: int = Field(ge=0)
    max_concurrent_rooms: int = Field(ge=1)
    max_room_participants: int = Field(ge=2)
    languages: list[str] = Field(default_factory=list)  # empty = all active languages
    telephony_enabled: bool = False
    transcript_retention_days: int | None = Field(default=None, ge=1)  # None = keep until deleted
    allowed_providers: list[str] = Field(default_factory=list)

class PlanResponse(BaseModel):
    id: uuid.UUID
    code: str
    name: str
    price_monthly: Decimal
    price_yearly: Decimal
    currency: str
    limits: dict[str, Any]
    external_price_id: str | None
    is_active: bool
    model_config = ConfigDict(from_attributes=True)

class PlanBrief(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    code: str
    name: str

class PlanOut(BaseModel):
    model_config= ConfigDict(from_attributes=True)
    id: uuid.UUID
    code: str
    name: str
    price_monthly: Decimal
    price_yearly: Decimal
    currency: str
    limits: dict[str, Any]
    external_price_id: str | None
    is_active: bool
    created_at: datetime
    updated_at: datetime

_Money = Field(ge=0, max_digits=10, decimal_places=2)

class PlanCreate(BaseModel):
    code: str = Field(pattern=r"^[a-z0-9][a-z0-9_-]{1,29}$")
    name: str = Field(min_length=1, max_length=80)
    price_monthly: Decimal = _Money
    price_yearly: Decimal = _Money
    currency: str = Field(default="USD", pattern=r"^[A-Z]{3}$")
    limits: PlanLimits
    external_price_id: str | None = Field(default=None, max_length=100)
    is_active: bool = True

class PlanUpdate(BaseModel):  # code is immutable
    name: str | None = Field(default=None, min_length=1, max_length=80)
    price_monthly: Decimal | None = Field(default=None, ge=0, max_digits=10, decimal_places=2)
    price_yearly: Decimal | None = Field(default=None, ge=0, max_digits=10, decimal_places=2)
    currency: str | None = Field(default=None, pattern=r"^[A-Z]{3}$")
    limits: PlanLimits | None = None  # replaces the whole limits object
    external_price_id: str | None = Field(default=None, max_length=100)
    is_active: bool | None = None
