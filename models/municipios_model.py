from sqlalchemy import ForeignKey, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column
from config.base import Base


class Municipio(Base):
    __tablename__ = "municipios"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )

    nome: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        unique=True
    )

    modelo: Mapped[int] = mapped_column(
        ForeignKey('modelos.id'),
        nullable=False
    )

    regionais_id: Mapped[int] = mapped_column(
        ForeignKey("regionais.id"),
        nullable=False
    )
