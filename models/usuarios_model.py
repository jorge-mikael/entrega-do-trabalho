from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, Text
from config.base import Base

class Usuario(Base):
    __tablename__ = "usuarios"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )

    nome: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    email: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    def __repr__(self):
        return (
            f"Usuario(id={self.id}, "
            f"usuario='{self.nome}', "
            f"email='{self.email}')"
        )