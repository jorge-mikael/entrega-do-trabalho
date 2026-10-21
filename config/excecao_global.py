import traceback
from PyQt6.QtWidgets import QMessageBox

def excecao_global(exc_type, exc_value, exc_traceback):
    resumo = str(exc_value)
    detalhes = "".join(
        traceback.format_exception(exc_type, exc_value, exc_traceback)
    )

    msg = QMessageBox()
    msg.setIcon(QMessageBox.Icon.Critical)
    msg.setWindowTitle("Erro")
    msg.setText("Ocorreu um erro inesperado.")
    msg.setInformativeText(resumo)
    msg.setDetailedText(detalhes)
    msg.exec()
