import uuid
from datetime import datetime
from sqlalchemy import BigInteger, ForeignKey, Index, String, func, text
from sqlalchemy.dialects.postgresql import INET, JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import Base

class AuditLog(Base):
    __tablename__ = "audit_logs"
    __table_args__ = (
        Index("ix_audit_logs_tenant_created", "tenant_id", "created_at"),
        Index("ix_audit_logs_actor", "actor_user_id"),
        # PostgreSQL requires the partition key inside the primary key, hence (id, created_at)
        {"postgresql_partition_by": "RANGE (created_at)"},
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    created_at: Mapped[datetime] = mapped_column(primary_key=True, server_default=func.now())
    tenant_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("tenants.id"))  # null = platform-level action
    actor_user_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"))
    actor_role: Mapped[str | None] = mapped_column(String(20))
    action: Mapped[str] = mapped_column(String(60))
    target_type: Mapped[str | None] = mapped_column(String(40))
    target_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True))
    ip_address: Mapped[str | None] = mapped_column(INET)
    # "metadata" is reserved on declarative classes, so the attribute is meta_data
    meta_data: Mapped[dict] = mapped_column("metadata", JSONB, server_default=text("'{}'::jsonb"))