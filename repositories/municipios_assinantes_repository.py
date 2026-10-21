from models.municipios_assinantes import MunicipioAssinante
from sqlalchemy.orm import Session
from sqlalchemy import select

class MunicipioAssinanteRepository():
    def __init__(self, session: Session):
        self.session = session

    def listar(self, offset=None, limite=None, regionais: list[str]=None):
            query = self.session.query(MunicipioAssinante).order_by(MunicipioAssinante.nome)

            if regionais:
                query = query.filter(MunicipioAssinante.regional.in_(regionais))
    
            if offset is not None:
                query = query.offset(offset)
    
            if limite is not None:
                query = query.limit(limite)
            
    
            return query.all()


    def buscar_por_municipio(self, municipio: str):
        return self.session.get(MunicipioAssinante, municipio)


    def listar_regionais(self):
        stmt = (
            select(MunicipioAssinante.regional)
            .distinct()
            .order_by(MunicipioAssinante.regional)
        )

        return self.session.scalars(stmt).all()


    def buscar_elaborador(self, municipio: str):
        registro = self.session.query(MunicipioAssinante).filter(MunicipioAssinante.municipio == municipio).first()

        return registro.assinatura_elaborador


    def buscar_aprovador(self, municipio: str):
        registro = self.session.query(MunicipioAssinante).filter(MunicipioAssinante.municipio == municipio).first()

        return registro.aprovador_assinatura


    def existe_municipio(self, municipio: str) -> bool:
        stmt = select(MunicipioAssinante.municipio).where(MunicipioAssinante.municipio == municipio)

        return self.session.scalar(stmt) is not None