from ui.main_window_ui import MainWindowUI
from ui.empresas_ui import Empresas
from ui.municipios_ui import MunicipiosUI
from ui.modelos_ui import ModelosUI
from controllers.empresas_controller import EmpresasController
from controllers.municipios_controller import MunicipiosController
from controllers.modelos_controller import ModelosController
from config.sessao import Sessao
from config.db import Session
from repositories.empresas_repository import EmpresasRepository
from workers.worker_entregas import WorkerEntregas
import csv

class MainWindowController():
    def __init__(self, ui: MainWindowUI):
        self.ui = ui
        self.usuario = Sessao.get_nome()
        self.worker = None


    def carregar(self):
        self.ui.setWindowTitle("Entregas do trabalho - " + self.usuario)
        self.ui.botao_empresas.clicked.connect(self._abrir_empresas)
        self.ui.botao_iniciar.clicked.connect(self._iniciar_processo)
        self.ui.botao_cancelar.clicked.connect(self._cancelar_processo)
        self.ui.botao_municipios.clicked.connect(self._abrir_municipios)
        self.ui.botao_modelos.clicked.connect(self._abrir_modelos)
        self._carregar_combo_empresas()


    def _carregar_combo_empresas(self):
        self.ui.empresas_combo.clear()

        with Session() as session:
            repo = EmpresasRepository(session)

            empresas = repo.listar()
            for empresa in empresas:
                texto = f'{empresa.cnpj} / {empresa.razao_social} / {empresa.responsavel}'
                self.ui.empresas_combo.addItem(texto, empresa.id)


    def _abrir_empresas(self):
        dialog = Empresas(self.ui)
        controller = EmpresasController(dialog)
        controller.carregar()
        dialog.exec()
        self._carregar_combo_empresas()


    def _validar(self):

        if self.ui.input_trabalhos.toPlainText().strip() == '':
            self.ui.informar('Erro', 'Digite pelo menos uma obra')
            return False

        if self.ui.empresas_combo.currentData() is None:
            self.ui.informar('Erro', 'Selecione uma empresa')
            return False

        return True


    def _iniciar_processo(self):

        if not self._validar():
            return
        
        tecnica = self._importar_tecnica()
        if tecnica is None:
            return
        
        texto_obras = self.ui.input_trabalhos.toPlainText().strip()
        obras_lista = texto_obras.split('\n')
        obras_lista_espacos = [obra.strip() for obra in obras_lista]
        obras = [obra for obra in obras_lista_espacos if obra != '']
    
        empresa = self._importar_empresa()

        destino = self._importar_destino()
        if destino is None:
            return

        self.worker = WorkerEntregas(obras, tecnica, empresa, destino)
        
        self.worker.log.connect(self._atualizar_resultado)
        self.worker.progress.connect(self.ui.progress_bar.setValue)
        self.worker.finished.connect(self._processo_finalizado)
        self.worker.canceled.connect(self._processo_cancelado)
        self.worker.erro.connect(self._mostrar_erro)

        self.ui.resultado.clear()
        self.ui.progress_bar.setValue(0)

        self.ui.botao_iniciar.setEnabled(False)
        self.ui.botao_cancelar.setEnabled(True)

        self.worker.start()


    def _mostrar_erro(self, e):
        raise e

    
    def _cancelar_processo(self):
        if self.worker:
            self.worker.stop()


    def _abrir_municipios(self):
        dialog = MunicipiosUI(self.ui)
        controller = MunicipiosController(dialog)
        controller.carregar()
        dialog.exec()


    def _abrir_modelos(self):
        dialog = ModelosUI(self.ui)
        controller = ModelosController(dialog)
        controller.carregar()
        dialog.exec()


    def _atualizar_resultado(self, texto):
        self.ui.resultado.appendPlainText(texto)


    def _processo_finalizado(self):
        self.ui.resultado.appendPlainText("✔️ Concluído!")
        self.ui.botao_iniciar.setEnabled(True)
        self.ui.botao_cancelar.setEnabled(False)

        self.worker = None


    def _processo_cancelado(self):
        self.ui.resultado.appendPlainText("⚠️ Cancelado pelo usuário")
        self.ui.botao_iniciar.setEnabled(True)
        self.ui.botao_cancelar.setEnabled(False)

        self.worker = None


    def _importar_empresa(self):
        
        empresa_id = self.ui.empresas_combo.currentData()
        with Session() as session:
            repo = EmpresasRepository(session)
            empresa = repo.buscar_por_id(empresa_id)

        return empresa


    def _importar_tecnica(self) -> dict:
        """Importa a planilha da técnica."""

        path = self.ui.abrir_arquivo(self.ui)

        if path == '':
            return None

        tecnica = {}

        with open(path, 'r', encoding='latin1') as arquivo:
            leitor = csv.DictReader(arquivo, delimiter='|')

            for linha in leitor:
                tecnica[linha['TRABALHO']] = linha

        return tecnica


    def _importar_destino(self):
        path = self.ui.selecionar_pasta()

        if path == '':
            return None
        else:
            return path

  
        