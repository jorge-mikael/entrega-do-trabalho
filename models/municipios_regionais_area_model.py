from sqlalchemy import Integer, Text
from sqlalchemy.orm import Mapped, mapped_column
from config.base import Base


class MunicipiosRegionaisArea(Base):
    __tablename__ = "municipios_regionais_area"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    nome: Mapped[str] = mapped_column(Text)

    modelo: Mapped[str] = mapped_column(Text)

    regional: Mapped[str] = mapped_column(Text)

    area: Mapped[str] = mapped_column(Text)