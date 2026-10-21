from ui.modelos_ui import ModelosUI
from ui.modelo_ui import ModeloUI
from controllers.modelo_controller import ModeloController
from repositories.modelos_view_repository import ModelosViewRepository
from repositories.modelos_repository import ModelosRepository
from config.db import Session

LINHAS_POR_PAGINA = 10

class ModelosController():
    def __init__(self, ui: ModelosUI):
        self.ui = ui
        self.pagina = 0


    def carregar(self):
        self._carregar_dados()
        self.ui.btn_prev.clicked.connect(self._anterior)
        self.ui.btn_next.clicked.connect(self._proxima)
        self.ui.btn_add.clicked.connect(self._adicionar_modelo)
        self.ui.editar_modelo.connect(self._editar_modelo)
        self.ui.excluir_modelo.connect(self._excluir_modelo)


    def _carregar_dados(self):
        total = self._count_total()
        max_pag = max(0, (total - 1)//LINHAS_POR_PAGINA)
        self.ui.lbl_pagina.setText(f"Página {self.pagina+1} / {max_pag+1}")
        offset = self.pagina * LINHAS_POR_PAGINA

        with Session() as session:
            repo = ModelosViewRepository(session)

            modelos = repo.listar(offset=offset, limite=LINHAS_POR_PAGINA)

        self.ui.preencher_tabela(modelos)


    def _editar_modelo(self, id):
        dialog = ModeloUI(parent=self.ui)
        controller = ModeloController(dialog, id)
        controller.carregar()
        if dialog.exec():
            self._carregar_dados()


    def _excluir_modelo(self, id):
        resposta = self.ui.questionar("Excluir", "Deseja excluir esta empresa?")
        if resposta.name != "Yes":
            return

        with Session() as session:
            repo = ModelosRepository(session)

            modelo = repo.buscar_por_id(id)

            if modelo is None:
                return

            repo.excluir(modelo)

            session.commit()

        self._carregar_dados()

            
    def _count_total(self):
        with Session() as session:
            repo = ModelosViewRepository(session)

            modelos = repo.listar()

            return len(modelos)


    def _adicionar_modelo(self):
        dialog = ModeloUI(parent=self.ui)
        controller = ModeloController(dialog)
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