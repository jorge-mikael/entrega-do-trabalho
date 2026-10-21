from ui.empresa_ui import EmpresaUI
from config.db import Session
from repositories.empresas_repository import EmpresasRepository
from models.empresas_model import Empresa

class EmpresaController():
    def __init__(self, ui: EmpresaUI, id: int = None):
        self.ui  = ui
        self.id = id


    def carregar(self):
        self.ui.setWindowTitle("Editar empresa" if self.id else "Adicionar empresa")
        self.ui.save.clicked.connect(self._salvar)
        self.ui.fechar.clicked.connect(self.ui.close)
        if self.id:
            self._carregar_dados()


    def _carregar_dados(self):
        with Session() as session:
            repo = EmpresasRepository(session)
            empresa = repo.buscar_por_id(self.id)

            self.ui.input_razao_social.setText(empresa.razao_social or "")
            self.ui.input_cnpj.setText(empresa.cnpj or "")
            self.ui.input_contrato.setText(empresa.contrato or "")
            self.ui.input_responsavel.setText(empresa.responsavel or "")
            self.ui.input_email.setText(empresa.email or "")
            self.ui.input_telefone.setText(empresa.telefone or "")
            self.ui.input_sigla.setText(empresa.sigla or "")


    def _salvar(self):
        razao_social = self.ui.input_razao_social.text().strip() or None
        cnpj = self.ui.input_cnpj.text().strip() or None
        contrato = self.ui.input_contrato.text().strip() or None
        responsavel = self.ui.input_responsavel.text().strip() or None
        email = self.ui.input_email.text().strip() or None
        telefone = self.ui.input_telefone.text().strip() or None
        sigla = self.ui.input_sigla.text().strip() or None
        
        with Session() as session:
            repo = EmpresasRepository(session)

            if self.id is not None:
                empresa = repo.buscar_por_id(self.id)

                empresa.razao_social = razao_social
                empresa.cnpj = cnpj
                empresa.contrato = contrato
                empresa.responsavel = responsavel
                empresa.email = email
                empresa.telefone = telefone
                empresa.sigla = sigla

                self.ui.informar('Sucesso!', 'Empresa foi atualizada com sucesso!')

            else:
                empresa = Empresa(
                    razao_social = razao_social,
                    cnpj = cnpj,
                    contrato = contrato,
                    responsavel = responsavel,
                    email = email,
                    telefone = telefone,
                    sigla = sigla
                )

                repo.adicionar(empresa)

                self.ui.informar('Sucesso!', 'Empresa foi adicionada com sucesso!')

            session.commit()

        self.ui.accept()


