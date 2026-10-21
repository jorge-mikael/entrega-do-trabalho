from ui.empresas_ui import Empresas
from ui.empresa_ui import EmpresaUI
from controllers.empresa_controller import EmpresaController
from repositories.empresas_repository import EmpresasRepository
from config.db import Session

LINHAS_POR_PAGINA = 10

class EmpresasController():
    def __init__(self, ui: Empresas):
        self.ui = ui
        self.pagina = 0


    def carregar(self):
        self._carregar_dados()
        self.ui.btn_prev.clicked.connect(self._anterior)
        self.ui.btn_next.clicked.connect(self._proxima)
        self.ui.btn_add.clicked.connect(self._adicionar_empresa)
        self.ui.editar_empresa.connect(self._editar_empresa)
        self.ui.excluir_empresa.connect(self._excluir_empresa)


    def _carregar_dados(self):
        total = self._count_total()
        max_pag = max(0, (total - 1)//LINHAS_POR_PAGINA)
        self.ui.lbl_pagina.setText(f"Página {self.pagina+1} / {max_pag+1}")
        offset = self.pagina * LINHAS_POR_PAGINA

        with Session() as session:
            repo = EmpresasRepository(session)

            empresas = repo.listar(offset=offset, limite=LINHAS_POR_PAGINA)

        self.ui.preencher_tabela(empresas)


    def _editar_empresa(self, id):
        dialog = EmpresaUI(parent=self.ui)
        controller = EmpresaController(dialog, id)
        controller.carregar()
        if dialog.exec():
            self._carregar_dados()


    def _excluir_empresa(self, id):
        resposta = self.ui.questionar("Excluir", "Deseja excluir esta empresa?")
        if resposta.name != "Yes":
            return

        with Session() as session:
            repo = EmpresasRepository(session)

            empresa = repo.buscar_por_id(id)

            if empresa is None:
                return

            repo.excluir(empresa)

            session.commit()

        self._carregar_dados()

            
    def _count_total(self):
        with Session() as session:
            repo = EmpresasRepository(session)

            empresas = repo.listar()

            return len(empresas)


    def _adicionar_empresa(self):
        dialog = EmpresaUI(parent=self.ui)
        controller = EmpresaController(dialog)
        controller.carregar()
        
        if dialog.exec():
            self._carregar_dados()
        

    def _anterior(self):
        if self.pagina > 0:
            self.pagina -= 1
            self._carregar_dados()


    def _proxima(self):
        total = self._count_total()
        max_pag = max(0, (total - 1)//LINHAS_POR_PAGINA)
        if self.pagina < max_pag:
            self.pagina += 1
            self._carregar_dados()