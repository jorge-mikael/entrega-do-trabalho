from ui.login_ui import LoginUI
from config.db import Session
from config.sessao import Sessao
from repositories.login_repository import LoginRepository

class LoginController():
    def __init__(self, ui: LoginUI):
        self.ui = ui


    def carregar(self):
        self._dados_combobox_nome()
        self.ui.entrar_botao.clicked.connect(self._logar)
        

    def _dados_combobox_nome(self):
        with Session() as session:
            repo = LoginRepository(session)

            usuarios = repo.listar()
            for usuario in usuarios:
                self.ui.usuario_nome.addItem(usuario.nome, usuario.id)


    def _logar(self):
       usuario_nome = self.ui.usuario_nome.currentText() or None
       usuario_id = self.ui.usuario_nome.currentData() or None

       if not usuario_nome:
           self.ui.informar('Erro', 'Selecione o usuário!')
           return
           
       Sessao.set_usuario(usuario_id, usuario_nome)
       self.ui.accept()