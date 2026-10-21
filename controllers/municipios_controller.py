from ui.municipios_ui import MunicipiosUI
from ui.municipio_ui import MunicipioUI
from controllers.municipio_controller import MunicipioController
from repositories.municipios_regionais_area_repository import MunicipiosRegionaisAreaRepository
from repositories.municipios_repository import MunicipiosRepository
from config.db import Session

LINHAS_POR_PAGINA = 10

class MunicipiosController():
    def __init__(self, ui: MunicipiosUI):
        self.ui = ui
        self.pagina = 0


    def carregar(self):
        self._carregar_dados()
        self.ui.btn_prev.clicked.connect(self._anterior)
        self.ui.btn_next.clicked.connect(self._proxima)
        self.ui.regionais_grupo.buttonToggled.connect(self._carregar_dados)
        self.ui.editar_municipio.connect(self._editar_municipio)
        self.ui.excluir_municipio.connect(self._excluir_municipio)
        self.ui.btn_new.clicked.connect(self._adicionar_municipio)


        with Session() as session:
            repo = MunicipiosRegionaisAreaRepository(session)
            regionais = repo.listar_regionais()
            self.ui.criar_botoes_filtro(regionais)


    def _carregar_dados(self):
        total = self._count_total()
        max_pag = max(0, (total - 1)//LINHAS_POR_PAGINA)
        self.ui.lbl_pagina.setText(f"Página {self.pagina+1} / {max_pag+1} de {total} registros")
        offset = self.pagina * LINHAS_POR_PAGINA
        regionais_filtro = self._filtro_regionais()

        with Session() as session:
            repo = MunicipiosRegionaisAreaRepository(session)

            municipios = repo.listar(offset=offset, limite=LINHAS_POR_PAGINA, regionais=regionais_filtro)
            
        self.ui.preencher_tabela(municipios)
        


    def _filtro_regionais(self):
        regionais = [checkbox.text() for checkbox in self.ui.regionais_grupo.buttons() if checkbox.isChecked()]

        return regionais

            
    def _count_total(self):
        regionais = self._filtro_regionais()
        with Session() as session:
            repo = MunicipiosRegionaisAreaRepository(session)

            municipios = repo.listar(regionais=regionais)

            return len(municipios)


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


    def _adicionar_municipio(self):
        dialog = MunicipioUI(parent=self.ui)
        controller = MunicipioController(dialog)
        controller.carregar()
        if dialog.exec():
            self._carregar_dados()


    def _editar_municipio(self, id):
        dialog = MunicipioUI(parent=self.ui)
        controller = MunicipioController(dialog, id)
        controller.carregar()
        if dialog.exec():
            self._carregar_dados()


    def _excluir_municipio(self, id):
        resposta = self.ui.questionar("Excluir", "Deseja excluir esta empresa?")
        if resposta.name != "Yes":
            return

        with Session() as session:
            repo = MunicipiosRepository(session)

            municipio = repo.buscar_por_id(id)

            if municipio is None:
                return

            repo.excluir(municipio)

            session.commit()

        self._carregar_dados()
