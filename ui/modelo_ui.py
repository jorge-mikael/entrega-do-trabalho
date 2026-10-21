from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QFormLayout, QLineEdit, QPushButton,
    QHBoxLayout, QMessageBox, QComboBox
)

class ModeloUI(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.resize(360, 160)

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.form = QFormLayout()
        layout.addLayout(self.form)

        self.input_nome = QLineEdit()
        self.form.addRow("Nome:", self.input_nome)

        self.input_elaborador = QComboBox()
        self.input_elaborador.setPlaceholderText('Selecione o elaborador...')
        self.form.addRow("Elaborador:", self.input_elaborador)

        self.input_aprovador = QComboBox()
        self.input_aprovador.setPlaceholderText('Selecione o aprovador...')
        self.form.addRow("Aprovador:", self.input_aprovador)

        btns = QHBoxLayout()
        self.save = QPushButton("Salvar")
        self.fechar = QPushButton("Fechar")
        btns.addWidget(self.save)
        btns.addWidget(self.fechar)
        layout.addLayout(btns)


    def informar(self, titulo, texto):
        QMessageBox.information(self, titulo, texto)