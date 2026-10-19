from sqlalchemy import Boolean, String, false, true
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import Base


class Language(Base):
    __tablename__ = "languages"

    code: Mapped[str] = mapped_column(
        String(10),
        primary_key=True,
    )

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    native_name: Mapped[str] = mapped_column(
        String(80),
        nullable=False,
    )

    translation_support: Mapped[bool] = mapped_column(
        Boolean,
        server_default=false(),
        nullable=False,
    )

    stt_supported: Mapped[bool] = mapped_column(
        Boolean,
        server_default=false(),
        nullable=False,
    )

    tts_supported: Mapped[bool] = mapped_column(
        Boolean,
        server_default=false(),
        nullable=False,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        server_default=true(),
        nullable=False,
    )