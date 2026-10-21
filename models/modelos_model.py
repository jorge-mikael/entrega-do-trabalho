from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column
from config.base import Base

class Modelo(Base):
    __tablename__ = "modelos"

    id: Mapped[int] = mapped_column(primary_key=True)

    nome: Mapped[str] = mapped_column(
        String,
        nullable=False
    )

    elaborador_id: Mapped[int] = mapped_column(
        ForeignKey("assinantes.id"),
        nullable=False
    )

    aprovador_id: Mapped[int] = mapped_column(
        ForeignKey("assinantes.id"),
        nullable=False
    )