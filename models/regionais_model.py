from sqlalchemy import ForeignKey, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column
from config.base import Base


class Regional(Base):
    __tablename__ = "regionais"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )

    nome: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        unique=True
    )

    area_id: Mapped[int] = mapped_column(
        ForeignKey("area.id"),
        nullable=False
    )
