from ui.municipio_ui import MunicipioUI
from config.db import Session
from repositories.municipios_repository import MunicipiosRepository
from repositories.modelos_repository import ModelosRepository
from repositories.regionais_repository import RegionaisRepository
from models.municipios_model import Municipio

class MunicipioController():
    def __init__(self, ui: MunicipioUI, id: int = None):
        self.ui  = ui
        self.id = id
        self.modelos = []
        self.regionais = []


    def carregar(self):
        self.ui.setWindowTitle("Editar Municipio" if self.id else "Adicionar Municipio")
        self.ui.save.clicked.connect(self._salvar)
        self.ui.fechar.clicked.connect(self.ui.close)
        self._carregar_combo_modelo()
        self._carregar_combo_regionais()
        if self.id:
            self._carregar_dados()


    def _carregar_combo_modelo(self):
        with Session() as session:
            repo = ModelosRepository(session)

            modelos = repo.listar()

            self.modelos = [(modelo.id, modelo.nome) for modelo in modelos]

        for id, nome in self.modelos:
            self.ui.input_modelo.addItem(nome, id)


    def _atual_combo_modelo(self, modelo_id):
        for i, (id, _) in enumerate(self.modelos):
            if id == modelo_id:
                self.ui.input_modelo.setCurrentIndex(i)
                break


    def _carregar_combo_regionais(self):
            with Session() as session:
                repo = RegionaisRepository(session)
    
                regionais = repo.listar()
    
                self.regionais = [(regional.id, regional.nome) for regional in regionais]
    
            for id, nome in self.regionais:
                self.ui.input_regional.addItem(nome, id)
    
    
    def _atual_combo_regionais(self, regionais_id):
        for i, (id, _) in enumerate(self.regionais):
            if id == regionais_id:
                self.ui.input_regional.setCurrentIndex(i)
                break
        

    def _carregar_dados(self):
        with Session() as session:
            repo = MunicipiosRepository(session)
            municipio = repo.buscar_por_id(self.id)

            self.ui.input_nome.setText(municipio.nome or "")
            self._atual_combo_modelo(municipio.modelo)
            self._atual_combo_regionais(municipio.regionais_id)


    def _salvar(self):
        nome = self.ui.input_nome.text().strip() or None
        modelo = self.ui.input_modelo.currentData() or None
        regional = self.ui.input_regional.currentData() or None
        
        with Session() as session:
            repo = MunicipiosRepository(session)

            if self.id is not None:
                empresa = repo.buscar_por_id(self.id)

                empresa.nome = nome
                empresa.modelo = modelo
                empresa.regionais_id = regional

                self.ui.informar('Sucesso!', 'Empresa foi atualizada com sucesso!')

            else:
                municipio = Municipio(
                    nome = nome,
                    modelo = modelo,
                    regionais_id = regional
                )

                repo.inserir(municipio)

                self.ui.informar('Sucesso!', 'Empresa foi adicionada com sucesso!')

            session.commit()

        self.ui.accept()
