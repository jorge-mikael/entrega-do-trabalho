from PyQt6.QtCore import QThread, pyqtSignal
from services.entregas_do_trabalho import EntregasDoTrabalho
from models.empresas_model import Empresa


class WorkerEntregas(QThread):
    log = pyqtSignal(str)
    progress = pyqtSignal(int)
    finished = pyqtSignal()
    canceled = pyqtSignal()
    erro = pyqtSignal(Exception)


    def __init__(self, obras: list, tecnica: dict, empresa: Empresa, destino: str):
        super().__init__()
        self._running = True
        self.obras = obras
        self.tecnica = tecnica
        self.empresa = empresa
        self.destino = destino


    def run(self):
        try:
            self._fazer_entregas_do_trabalho()
        except Exception as e:
            self.log.emit(str(e))
            self.erro.emit(e)
        finally:
            self.log.emit("✅ Processo finalizado")
            self.finished.emit()


    def stop(self):
        self._running = False


    def _fazer_entregas_do_trabalho(self):
        total = len(self.obras)

        entregas_to_trabalho = EntregasDoTrabalho(self.tecnica, self.empresa, self.destino)

        for i, obra in enumerate(self.obras):
            if not self._running:
                self.log.emit("❌ Processo cancelado")
                self.canceled.emit()
                return

            entregas_to_trabalho.gerar_documento(obra)

            self.log.emit(f'Entrega do trabalho da obra {obra} gerado com sucesso!')
            self.progress.emit(int((i+1)/total * 100))