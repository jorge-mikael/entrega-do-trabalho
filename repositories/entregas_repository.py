from models.entregas_model import Entrega
from sqlalchemy.orm import Session

class EntregasRepository():
    def __init__(self, session: Session):
        self.session = session


    def listar(self):
        return self.session.query(Entrega).order_by(Entrega.id).all()


    def adicionar(self, empresa: Entrega):
        self.session.add(empresa)
