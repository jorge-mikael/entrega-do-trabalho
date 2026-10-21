from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QTableWidget, QLabel, QPushButton, 
    QToolButton, QTableWidgetItem, QMenu, QMessageBox
)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import pyqtSignal
from functools import partial
from models.modelos_view import ModeloView


class ModelosUI(QDialog):

    editar_modelo = pyqtSignal(int)
    excluir_modelo = pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Modelos")
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
        
        self.btn_add = QPushButton("Adicionar modelo")
        
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
            self.editar_modelo.emit(id)
        elif action == act_del:
            self.excluir_modelo.emit(id)


    def preencher_tabela(self, modelos: list[ModeloView]):
        self.tabela.setRowCount(len(modelos))
        self.tabela.setColumnCount(5)
        self.tabela.setHorizontalHeaderLabels(
            [
                "Ações", 
                "ID", 
                "Modelo", 
                "Elaborador", 
                "Aprovador"
            ]
        )

        for r, modelo in enumerate(modelos):
            btn = QToolButton()
            btn.setText("⋮")
            btn.setFont(QFont("Arial", 12))
            btn.clicked.connect(partial(self._abrir_menu, btn, modelo.id))
            self.tabela.setCellWidget(r, 0, btn)
            self.tabela.setItem(r, 1, QTableWidgetItem(str(modelo.id)))
            self.tabela.setItem(r, 2, QTableWidgetItem(modelo.nome or ""))
            self.tabela.setItem(r, 3, QTableWidgetItem(modelo.elaborador or ""))
            self.tabela.setItem(r, 4, QTableWidgetItem(modelo.aprovador or ""))
            

        