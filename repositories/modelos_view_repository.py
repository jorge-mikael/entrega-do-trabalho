from sqlalchemy import select
from sqlalchemy.orm import Session
from models.modelos_view import ModeloView

class ModelosViewRepository:

    def __init__(self, session: Session):
        self.session = session

    def buscar_por_id(self, modelo_id: int):
        return self.session.get(ModeloView, modelo_id)

    def listar(self, offset=None, limite=None):
        query = self.session.query(ModeloView).order_by(ModeloView.id)

        if offset is not None:
            query = query.offset(offset)

        if limite is not None:
            query = query.limit(limite)

        return query.all()