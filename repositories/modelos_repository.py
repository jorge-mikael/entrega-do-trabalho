from sqlalchemy import select
from sqlalchemy.orm import Session
from models.modelos_model import Modelo


class ModelosRepository:

    def __init__(self, session: Session):
        self.session = session


    def inserir(self, modelo: Modelo):
        self.session.add(modelo)


    def buscar_por_id(self, modelo_id: int):
        return self.session.get(Modelo, modelo_id)


    def buscar_por_nome(self, nome: str):
        stmt = (
            select(Modelo)
            .where(Modelo.nome == nome)
        )

        return self.session.scalar(stmt)


    def listar(self):
        stmt = (
            select(Modelo)
            .order_by(Modelo.nome)
        )

        return self.session.scalars(stmt).all()


    def atualizar(self, modelo: Modelo):
        self.session.flush()

        return modelo


    def excluir(self, modelo: Modelo):
        self.session.delete(modelo)
        self.session.flush()