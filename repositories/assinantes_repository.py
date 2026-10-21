from sqlalchemy import select
from sqlalchemy.orm import Session
from models.assinantes_model import Assinante


class AssinantesRepository:

    def __init__(self, session: Session):
        self.session = session


    def inserir(self, assinante: Assinante):
        self.session.add(assinante)
        self.session.flush()


    def buscar_por_id(self, assinante_id: int):
        return self.session.get(Assinante, assinante_id)


    def buscar_por_nome(self, nome: str):
        stmt = select(Assinante).where(
            Assinante.nome == nome
        )
        return self.session.scalar(stmt)


    def buscar_por_matricula(self, matricula: str):
        stmt = select(Assinante).where(
            Assinante.matricula == matricula
        )
        return self.session.scalar(stmt)


    def buscar_por_email(self, email: str):
        stmt = select(Assinante).where(
            Assinante.email == email
        )
        return self.session.scalar(stmt)


    def listar(self):
        stmt = select(Assinante).order_by(Assinante.nome)
        return self.session.scalars(stmt).all()


    def excluir(self, assinante: Assinante):
        self.session.delete(assinante)
        self.session.flush()