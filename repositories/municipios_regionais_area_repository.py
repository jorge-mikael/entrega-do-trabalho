from models.municipios_regionais_area_model import MunicipiosRegionaisArea
from sqlalchemy.orm import Session
from sqlalchemy import select

class MunicipiosRegionaisAreaRepository():
    def __init__(self, session: Session):
        self.session = session

    def listar(self, offset=None, limite=None, regionais: list[str]=None):
            query = self.session.query(MunicipiosRegionaisArea).order_by(MunicipiosRegionaisArea.nome)

            if regionais:
                query = query.filter(MunicipiosRegionaisArea.regional.in_(regionais))
    
            if offset is not None:
                query = query.offset(offset)
    
            if limite is not None:
                query = query.limit(limite)
            
    
            return query.all()


    def listar_regionais(self):
        stmt = (
            select(MunicipiosRegionaisArea.regional)
            .distinct()
            .order_by(MunicipiosRegionaisArea.regional)
        )

        return self.session.scalars(stmt).all()


    def buscar_modelo(self, municipio: str):
        registro = self.session.query(MunicipiosRegionaisArea).filter(MunicipiosRegionaisArea.nome == municipio).first()

        return registro.modelo


    def existe_municipio(self, municipio: str) -> bool:
        stmt = select(MunicipiosRegionaisArea.nome).where(MunicipiosRegionaisArea.nome == municipio)

        return self.session.scalar(stmt) is not None