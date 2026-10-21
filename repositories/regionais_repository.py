from sqlalchemy import select
from sqlalchemy.orm import Session
from models.regionais_model import Regional


class RegionaisRepository:

    def __init__(self, session: Session):
        self.session = session


    def inserir(self, regional: Regional):
        self.session.add(regional)


    def buscar_por_id(self, regional_id: int):
        return self.session.get(Regional, regional_id)


    def buscar_por_nome(self, nome: str):
        stmt = select(Regional).where(Regional.nome == nome)
        return self.session.scalar(stmt)


    def listar(self):
        stmt = select(Regional).order_by(Regional.nome)
        return self.session.scalars(stmt).all()


    def listar_por_area(self, area_id: int):
        stmt = (
            select(Regional)
            .where(Regional.area_id == area_id)
            .order_by(Regional.nome)
        )
        return self.session.scalars(stmt).all()


    def atualizar(self, regional: Regional):
        self.session.flush()
        return regional


    def excluir(self, regional: Regional):
        self.session.delete(regional)
        self.session.flush()