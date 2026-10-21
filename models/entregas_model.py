from datetime import date, datetime
from sqlalchemy import Date, DateTime, ForeignKey, Integer, Text, func
from sqlalchemy.orm import Mapped, mapped_column
from config.base import Base


class Entrega(Base):
    __tablename__ = "entregas"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )

    trabalho: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    empresa: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    municipio: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    endereco: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    prazo: Mapped[date] = mapped_column(
        Date,
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.current_timestamp(),
        nullable=False
    )

    usuarios_id: Mapped[int] = mapped_column(
        ForeignKey("usuarios.id"),
        nullable=False
    )