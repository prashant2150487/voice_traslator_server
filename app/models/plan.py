import uuid
from decimal import Decimal
from sqlalchemy import Numeric, String, text, true
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import Base, TimestampMixin

class Plan(Base, TimestampMixin):
    __tablename__ = "plans"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    code: Mapped[str] = mapped_column(String(30), unique=True)  # starter, business, enterprise
    name: Mapped[str] = mapped_column(String(80))
    price_monthly: Mapped[Decimal] = mapped_column(Numeric(10, 2), server_default="0")
    price_yearly: Mapped[Decimal] = mapped_column(Numeric(10, 2), server_default="0")
    currency: Mapped[str] = mapped_column(String(3), server_default="USD")
    # max_seats, monthly_minutes, max_concurrent_rooms, max_room_participants, languages,
    # telephony_enabled, transcript_retention_days, allowed_providers
    limits: Mapped[dict] = mapped_column(JSONB, server_default=text("'{}'::jsonb"))
    external_price_id: Mapped[str | None] = mapped_column(String(100))
    is_active: Mapped[bool] = mapped_column(server_default=true())