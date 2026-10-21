from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QFormLayout, QLineEdit, QPushButton,
    QHBoxLayout, QMessageBox, QComboBox
)

class MunicipioUI(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.resize(360, 160)

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.form = QFormLayout()
        layout.addLayout(self.form)

        self.input_nome = QLineEdit()
        self.form.addRow("Nome:", self.input_nome)

        self.input_modelo = QComboBox()
        self.input_modelo.setPlaceholderText('Selecione o modelo...')
        self.form.addRow("Modelo:", self.input_modelo)

        self.input_regional = QComboBox()
        self.input_regional.setPlaceholderText('Selecione o regional...')
        self.form.addRow("Regional:", self.input_regional)

        btns = QHBoxLayout()
        self.save = QPushButton("Salvar")
        self.fechar = QPushButton("Fechar")
        btns.addWidget(self.save)
        btns.addWidget(self.fechar)
        layout.addLayout(btns)


    def informar(self, titulo, texto):
        QMessageBox.information(self, titulo, texto)