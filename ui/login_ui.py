from PyQt6.QtWidgets import QDialog, QVBoxLayout, QComboBox, QPushButton, QHBoxLayout, QLabel, QSizePolicy, QMessageBox

class LoginUI(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Entre com seu nome")
        self.resize(300, 200)

        layout_principal = QVBoxLayout()
        self.setLayout(layout_principal)

        layout_usuario = QHBoxLayout()

        self.usuario_label = QLabel('Usuário:')
        self.usuario_label.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        layout_usuario.addWidget(self.usuario_label)

        self.usuario_nome = QComboBox()
        self.usuario_nome.setPlaceholderText('Escolha o usuário...')
        self.usuario_nome.setEditable(True)
        layout_usuario.addWidget(self.usuario_nome)

        layout_principal.addLayout(layout_usuario)

        layout_entrar = QHBoxLayout()

        self.entrar_botao = QPushButton('Entrar')
        layout_entrar.addWidget(self.entrar_botao)

        layout_principal.addLayout(layout_entrar)

        self.entrar_botao.setAutoDefault(True)
        self.entrar_botao.setDefault(True)


    def informar(self, titulo, mensagem):
        QMessageBox.information(self, titulo, mensagem)
        