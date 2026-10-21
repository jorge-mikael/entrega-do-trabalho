from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QTableWidget, QLabel, QPushButton, 
    QToolButton, QTableWidgetItem, QMenu, QMessageBox
)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import pyqtSignal
from functools import partial
from models.empresas_model import Empresa


class Empresas(QDialog):

    editar_empresa = pyqtSignal(int)
    excluir_empresa = pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Empresas")
        self.resize(850, 420)
        self.pagina = 0

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.tabela = QTableWidget()
        layout.addWidget(self.tabela)

        bottom = QHBoxLayout()
        self.lbl_pagina = QLabel()
        self.btn_prev = QPushButton("Anterior")
        
        self.btn_next = QPushButton("Próxima")
        
        self.btn_add = QPushButton("Adicionar empresa")
        
        bottom.addWidget(self.btn_prev)
        bottom.addWidget(self.btn_next)
        bottom.addStretch()
        bottom.addWidget(self.lbl_pagina)
        bottom.addStretch()
        bottom.addWidget(self.btn_add)
        layout.addLayout(bottom)


    def questionar(self, titulo, texto):
        return QMessageBox.question(self, titulo, texto)


    def _abrir_menu(self, button: QPushButton, id):
        menu = QMenu()
        act_edit = menu.addAction("Editar")
        act_del = menu.addAction("Excluir")
        action = menu.exec(button.mapToGlobal(button.rect().bottomLeft()))
        if action == act_edit:
            self.editar_empresa.emit(id)
        elif action == act_del:
            self.excluir_empresa.emit(id)


    def preencher_tabela(self, empresas: list[Empresa]):
        self.tabela.setRowCount(len(empresas))
        self.tabela.setColumnCount(9)
        self.tabela.setHorizontalHeaderLabels(
            [
                "Ações", 
                "ID", 
                "Razão Social", 
                "CNPJ", 
                "Contrato", 
                "Responsável", 
                "Email", 
                "Telefone", 
                "Sigla"
            ]
        )

        for r, empresa in enumerate(empresas):
            btn = QToolButton()
            btn.setText("⋮")
            btn.setFont(QFont("Arial", 12))
            btn.clicked.connect(partial(self._abrir_menu, btn, empresa.id))
            self.tabela.setCellWidget(r, 0, btn)
            self.tabela.setItem(r, 1, QTableWidgetItem(str(empresa.id)))
            self.tabela.setItem(r, 2, QTableWidgetItem(empresa.razao_social or ""))
            self.tabela.setItem(r, 3, QTableWidgetItem(empresa.cnpj or ""))
            self.tabela.setItem(r, 4, QTableWidgetItem(empresa.contrato or ""))
            self.tabela.setItem(r, 5, QTableWidgetItem(empresa.responsavel or ""))
            self.tabela.setItem(r, 6, QTableWidgetItem(empresa.email or ""))
            self.tabela.setItem(r, 7, QTableWidgetItem(empresa.telefone or ""))
            self.tabela.setItem(r, 8, QTableWidgetItem(empresa.sigla or ""))

        