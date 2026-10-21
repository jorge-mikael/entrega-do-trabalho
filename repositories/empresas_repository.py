from models.empresas_model import Empresa
from sqlalchemy.orm import Session
from sqlalchemy.inspection import inspect

class EmpresasRepository():
    def __init__(self, session: Session):
        self.session = session


    def listar(self, offset=None, limite=None):
        query = self.session.query(Empresa).order_by(Empresa.id)

        if offset is not None:
            query = query.offset(offset)

        if limite is not None:
            query = query.limit(limite)

        return query.all()


    def adicionar(self, empresa: Empresa):
        self.session.add(empresa)


    def buscar_por_id(self, id_empresa):
        return self.session.get(Empresa, id_empresa)


    def excluir(self, empresa: Empresa):
        self.session.delete(empresa)


    def listar_dict(self):
        empresas = self.listar()

        empresas_por_nome = {
            empresa.razao_social: {
                coluna.key: getattr(empresa, coluna.key)
                for coluna in inspect(empresa).mapper.column_attrs
            }
            for empresa in empresas
        }

        return empresas_por_nome   




    