from ui.modelo_ui import ModeloUI
from config.db import Session
from repositories.modelos_repository import ModelosRepository
from repositories.assinantes_repository import AssinantesRepository
from models.modelos_model import Modelo

class ModeloController():
    def __init__(self, ui: ModeloUI, id: int = None):
        self.ui  = ui
        self.id = id
        self.assinantes = []


    def carregar(self):
        self.ui.setWindowTitle("Editar modelo" if self.id else "Adicionar modelo")
        self.ui.save.clicked.connect(self._salvar)
        self.ui.fechar.clicked.connect(self.ui.close)
        self._carregar_combo_elaborador()
        self._carregar_combo_aprovador()
        if self.id:
            self._carregar_dados()


    def _carregar_combo_elaborador(self):
        with Session() as session:
            repo = AssinantesRepository(session)

            assinantes = repo.listar()

            self.assinantes = [(assinante.id, assinante.nome) for assinante in assinantes]

        for id, nome in self.assinantes:
            self.ui.input_elaborador.addItem(nome, id)


    def _atual_combo_elaborador(self, elaborador_id):
        for i, (id, _) in enumerate(self.assinantes):
            if id == elaborador_id:
                self.ui.input_elaborador.setCurrentIndex(i)
                break


    def _carregar_combo_aprovador(self):
            with Session() as session:
                repo = AssinantesRepository(session)
    
                assinantes = repo.listar()
    
                self.assinantes = [(assinante.id, assinante.nome) for assinante in assinantes]
    
            for id, nome in self.assinantes:
                self.ui.input_aprovador.addItem(nome, id)
    
    
    def _atual_combo_aprovador(self, aprovador_id):
        for i, (id, _) in enumerate(self.assinantes):
            if id == aprovador_id:
                self.ui.input_aprovador.setCurrentIndex(i)
                break
        

    def _carregar_dados(self):
        with Session() as session:
            repo = ModelosRepository(session)
            modelo = repo.buscar_por_id(self.id)

            self.ui.input_nome.setText(modelo.nome or "")
            self._atual_combo_elaborador(modelo.elaborador_id)
            self._atual_combo_aprovador(modelo.aprovador_id)


    def _salvar(self):
        nome = self.ui.input_nome.text().strip() or None
        elaborador = self.ui.input_elaborador.currentData() or None
        aprovador = self.ui.input_aprovador.currentData() or None
        
        with Session() as session:
            repo = ModelosRepository(session)

            if self.id is not None:
                modelo = repo.buscar_por_id(self.id)

                modelo.nome = nome
                modelo.elaborador_id = elaborador
                modelo.aprovador_id = aprovador

                self.ui.informar('Sucesso!', 'Modelo foi atualizado com sucesso!')

            else:
                modelo = Modelo(
                    nome = nome,
                    elaborador_id = elaborador,
                    aprovador_id = aprovador
                )

                repo.inserir(modelo)

                self.ui.informar('Sucesso!', 'Modelo foi adicionado com sucesso!')

            session.commit()

        self.ui.accept()
