import uuid
from datetime import datetime

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, String, UniqueConstraint, text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import Base, TimestampMixin


class Tenant(Base, TimestampMixin):
    __tablename__ = "tenants"
    __table_args__ = (
        CheckConstraint(
            "status IN ('trial','active','past_due','suspended','cancelled')",
            name="ck_tenants_status",
        ),
        CheckConstraint(
            r"slug ~ '^[a-z0-9]([a-z0-9-]{0,61}[a-z0-9])?$'",
            name="ck_tenants_slug",
        ),
        UniqueConstraint("slug", name="uq_tenants_slug"),
    )
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    slug: Mapped[str] = mapped_column(String(63), nullable=False)
    status: Mapped[str] = mapped_column(
        String(15),
        server_default="active",
        nullable=False,
    )
    owner_user_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey(
            "users.id",
            use_alter=True,
            name="fk_tenants_owner_user",
            ondelete="SET NULL",
        ),
    )
    default_language: Mapped[str | None] = mapped_column(
        ForeignKey("languages.code", name="fk_tenants_default_language_languages"),
    )
    data_region: Mapped[str] = mapped_column(
        String(20),
        server_default="default",
        nullable=False,
    )
    settings: Mapped[dict] = mapped_column(
        JSONB,
        server_default=text("'{}'::jsonb"),
        nullable=False,
    )
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))