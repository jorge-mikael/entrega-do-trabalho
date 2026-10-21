from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, Text
from config.base import Base


class Area(Base):
    __tablename__ = "area"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )

    nome: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        unique=True
    )


    def __repr__(self):
        return (
            f"Area("
            f"id={self.id}, "
            f"nome='{self.nome}'"
            f")"
        )