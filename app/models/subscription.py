import uuid
from datetime import datetime
from sqlalchemy import CheckConstraint, ForeignKey, String, false, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import Base, TimestampMixin

class Subscription(Base, TimestampMixin):
    __tablename__ = "subscriptions"
    __table_args__ = (
        CheckConstraint("status IN ('trialing','active','past_due','cancelled')", name="ck_subscriptions_status"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("tenants.id", ondelete="CASCADE"), index=True)
    plan_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("plans.id"))
    status: Mapped[str] = mapped_column(String(15), server_default="active")
    billing_provider: Mapped[str | None] = mapped_column(String(20))  # stripe | razorpay
    external_customer_id: Mapped[str | None] = mapped_column(String(100))
    external_subscription_id: Mapped[str | None] = mapped_column(String(100), unique=True)
    seats: Mapped[int] = mapped_column(server_default="1")
    current_period_start: Mapped[datetime | None]
    current_period_end: Mapped[datetime | None]
    cancel_at_period_end: Mapped[bool] = mapped_column(server_default=false())