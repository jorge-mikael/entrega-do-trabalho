from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QFormLayout, QLineEdit, QPushButton,
    QHBoxLayout, QMessageBox
)

class EmpresaUI(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.resize(360, 160)

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.form = QFormLayout()
        layout.addLayout(self.form)

        self.input_razao_social = QLineEdit()
        self.form.addRow("Razão social:", self.input_razao_social)

        self.input_cnpj = QLineEdit()
        self.form.addRow("CNPJ:", self.input_cnpj)

        self.input_contrato = QLineEdit()
        self.form.addRow("Contrato:", self.input_contrato)

        self.input_responsavel = QLineEdit()
        self.form.addRow("Responsável:", self.input_responsavel)

        self.input_email = QLineEdit()
        self.form.addRow("Email:", self.input_email)

        self.input_telefone = QLineEdit()
        self.form.addRow("Telefone:", self.input_telefone)

        self.input_sigla = QLineEdit()
        self.form.addRow("Sigla:", self.input_sigla)


        btns = QHBoxLayout()
        self.save = QPushButton("Salvar")
        self.fechar = QPushButton("Fechar")
        btns.addWidget(self.save)
        btns.addWidget(self.fechar)
        layout.addLayout(btns)


    def informar(self, titulo, texto):
        QMessageBox.information(self, titulo, texto)