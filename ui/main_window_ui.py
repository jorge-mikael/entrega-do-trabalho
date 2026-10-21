from PyQt6.QtWidgets import QWidget, QMainWindow, QHBoxLayout, QVBoxLayout, QTextEdit, QPushButton, QPlainTextEdit, QProgressBar, QFileDialog, QComboBox, QMessageBox

class MainWindowUI(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Entregas do trabalho")
        self.resize(1000, 560)

        widget_central = QWidget()
        self.setCentralWidget(widget_central)

        layout_principal = QVBoxLayout()
        widget_central.setLayout(layout_principal)

        layout1 = QHBoxLayout()

        # ===== LADO ESQUERDO =====
        layout_esquerda = QVBoxLayout()

        self.input_trabalhos = QTextEdit()
        self.input_trabalhos.setPlaceholderText('Digite os trabalhos das obras aqui...')
        layout_esquerda.addWidget(self.input_trabalhos)

        # Combobox de empresas
        self.empresas_combo = QComboBox()
        self.empresas_combo.setPlaceholderText('Escolha a empresa...')
        layout_esquerda.addWidget(self.empresas_combo)

        # ===== LADO DIREITO =====
        layout_direita = QVBoxLayout()

        self.resultado = QPlainTextEdit()
        self.resultado.setReadOnly(True)
        layout_direita.addWidget(self.resultado)

        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        layout_direita.addWidget(self.progress_bar)

        # ===== ADICIONAR AO PRINCIPAL =====
        layout1.addLayout(layout_esquerda, 1)
        layout1.addLayout(layout_direita, 1)

        layout_principal.addLayout(layout1)

        # Botões
        layout_botoes = QHBoxLayout()

        self.botao_iniciar = QPushButton('▶️ Iniciar')
        layout_botoes.addWidget(self.botao_iniciar)

        self.botao_empresas = QPushButton('Empresas')
        layout_botoes.addWidget(self.botao_empresas)

        self.botao_municipios = QPushButton('Municípios')
        layout_botoes.addWidget(self.botao_municipios)

        self.botao_modelos = QPushButton('Modelos')
        layout_botoes.addWidget(self.botao_modelos)

        self.botao_cancelar = QPushButton('Cancelar')
        self.botao_cancelar.setEnabled(False)
        layout_botoes.addWidget(self.botao_cancelar)

        layout_principal.addLayout(layout_botoes)


      

    def abrir_arquivo(self, parent: QWidget = None) -> str:
        file_filter = "Todos os arquivos (*.*);;Arquivos Excel (*.xlsx *.xls);;CSV (*.csv)"
        arquivo, _ = QFileDialog.getOpenFileName(
            parent,
            "Selecione o arquivo da tecnica em txt",
            "",
            file_filter,
            options=QFileDialog.Option.ReadOnly  # ✅ PyQt6
        )
        return arquivo


    def selecionar_pasta(self):
        path = QFileDialog.getExistingDirectory(self, 'Selecione uma pasta para os documentos')

        return path


    def informar(self, titulo, mensagem):
            QMessageBox.information(self, titulo, mensagem)


