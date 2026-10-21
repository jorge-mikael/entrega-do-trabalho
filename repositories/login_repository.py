from models.usuarios_model import Usuario
from sqlalchemy.orm import Session

class LoginRepository():
    def __init__(self, session: Session):
        self.session = session

    def listar(self):
        return self.session.query(Usuario).all()

