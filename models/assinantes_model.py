from sqlalchemy import Integer, Text
from sqlalchemy.orm import Mapped, mapped_column
from config.base import Base


class Assinante(Base):
    __tablename__ = "assinantes"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )

    nome: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    matricula: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    email: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    telefone: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    assinatura: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )