from sqlalchemy import Boolean, CheckConstraint, Column, ForeignKey, String, Table, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base

role_permissions = Table(
    "role_permissions",
    Base.metadata,
    Column(
        "role_code",
        String(20),
        ForeignKey(
            "roles.code",
            ondelete="CASCADE",
            onupdate="CASCADE",
            name="fk_role_permissions_role_code_roles",
        ),
        primary_key=True,
    ),
    Column("permission_code", String(60), ForeignKey("permissions.code", ondelete="CASCADE"), primary_key=True),
)

class Permission(Base):
    __tablename__ = "permissions"

    code: Mapped[str] = mapped_column(String(60), primary_key=True)
    description: Mapped[str] = mapped_column(String(255))

class Role(Base):
    __tablename__ = "roles"
    __table_args__ = (
        CheckConstraint("scope IN ('platform','tenant','room')", name="ck_roles_scope"),
    )

    code: Mapped[str] = mapped_column(String(20), primary_key=True)  # super_admin | admin | user | guest
    name: Mapped[str] = mapped_column(String(50))
    scope: Mapped[str] = mapped_column(String(20))
    description: Mapped[str] = mapped_column(Text)
    is_system: Mapped[bool] = mapped_column(Boolean, default=True)

    permissions: Mapped[list[Permission]] = relationship(
        secondary=role_permissions, lazy="selectin", order_by=Permission.code
    )
