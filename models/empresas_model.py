from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, Text
from config.base import Base

class Empresa(Base):
    __tablename__ = 'empresas'

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
        )

    razao_social: Mapped[str] = mapped_column(
        Text,
        nullable=False
        )

    cnpj: Mapped[str] = mapped_column(
            Text,
            nullable=False
        )

    contrato: Mapped[str] = mapped_column(
            Text,
            nullable=False
        )

    responsavel: Mapped[str] = mapped_column(
            Text,
            nullable=False
        )

    email: Mapped[str] = mapped_column(
            Text,
            nullable=False
        )

    sigla: Mapped[str] = mapped_column(
            Text,
            nullable=False
        )

    telefone: Mapped[str] = mapped_column(
            Text,
            nullable=False
        )