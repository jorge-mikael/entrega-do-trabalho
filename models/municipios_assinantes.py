from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Text
from config.base import Base

class MunicipioAssinante(Base):
    __tablename__ = "municipios_assinantes"

    municipio: Mapped[str] = mapped_column(Text, primary_key=True)
    assinatura_elaborador: Mapped[str] = mapped_column(Text)
    aprovador_nome: Mapped[str] = mapped_column(Text)
    aprovador_matricula: Mapped[str] = mapped_column(Text)
    aprovador_email: Mapped[str] = mapped_column(Text)
    aprovador_telefone: Mapped[str] = mapped_column(Text)
    aprovador_assinatura: Mapped[str] = mapped_column(Text)
    regional: Mapped[str] = mapped_column(Text)