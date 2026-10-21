from models.municipios_model import Municipio
from sqlalchemy.orm import Session

class MunicipiosRepository():
    def __init__(self, session: Session):
        self.session = session


    def listar(self):
        return self.session.query(Municipio).all()


    def buscar_por_id(self, municipio_id: int):
        return self.session.get(Municipio, municipio_id)


    def inserir(self, municipio: Municipio):
        self.session.add(municipio)


    def excluir(self, municipio: Municipio):
        self.session.delete(municipio)
        self.session.flush()
