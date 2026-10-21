from sqlalchemy import Integer, Text
from sqlalchemy.orm import Mapped, mapped_column
from config.base import Base

class ModeloView(Base):
    __tablename__ = "modelos_view"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )

    nome: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    elaborador: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    aprovador: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )