from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QTableWidget, QLabel, QPushButton, QTableWidgetItem, QCheckBox, QButtonGroup, QMenu,
    QMessageBox, QToolButton
)
from PyQt6.QtGui import QFont
from functools import partial

from models.municipios_regionais_area_model import MunicipiosRegionaisArea

from PyQt6.QtCore import pyqtSignal

class MunicipiosUI(QDialog):

    editar_municipio = pyqtSignal(int)
    excluir_municipio = pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Municípios")
        self.resize(650, 420)

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.regionais = QHBoxLayout()
        
        layout.addLayout(self.regionais)

        self.regionais_grupo =  QButtonGroup(self)
        self.regionais_grupo.setExclusive(False)

        self.tabela = QTableWidget()
        layout.addWidget(self.tabela)

        bottom = QHBoxLayout()
        self.lbl_pagina = QLabel()
        self.btn_prev = QPushButton("Anterior")
        self.btn_next = QPushButton("Próxima")
        self.btn_new  = QPushButton("Adicionar município")
        
        bottom.addWidget(self.btn_prev)
        bottom.addWidget(self.btn_next)
        bottom.addStretch()
        bottom.addWidget(self.lbl_pagina)
        bottom.addStretch()
        bottom.addWidget(self.btn_new)
        layout.addLayout(bottom)


    def criar_botoes_filtro(self, nomes: str):
        for nome in nomes:
            botao = QCheckBox(nome)
            self.regionais.addWidget(botao)
            self.regionais_grupo.addButton(botao)

        self.regionais.addStretch()


    def questionar(self, titulo, texto):
        return QMessageBox.question(self, titulo, texto)


    def _abrir_menu(self, button: QPushButton, id):
        menu = QMenu()
        act_edit = menu.addAction("Editar")
        act_del = menu.addAction("Excluir")
        action = menu.exec(button.mapToGlobal(button.rect().bottomLeft()))
        if action == act_edit:
            self.editar_municipio.emit(id)
        elif action == act_del:
            self.excluir_municipio.emit(id)


    def preencher_tabela(self, municipios: list[MunicipiosRegionaisArea]):
        self.tabela.setRowCount(len(municipios))
        self.tabela.setColumnCount(6)
        self.tabela.setHorizontalHeaderLabels(
            [
                "Ações",
                "ID",
                "Nome", 
                "Regional", 
                "Área", 
                "Modelo", 
            ]
        )

        for r, municipio in enumerate(municipios):
            btn = QToolButton()
            btn.setText("⋮")
            btn.setFont(QFont("Arial", 12))
            btn.clicked.connect(partial(self._abrir_menu, btn, municipio.id))
            self.tabela.setCellWidget(r, 0, btn)
            self.tabela.setItem(r, 1, QTableWidgetItem(str(municipio.id)))
            self.tabela.setItem(r, 2, QTableWidgetItem(municipio.nome or ""))
            self.tabela.setItem(r, 3, QTableWidgetItem(municipio.regional or ""))
            self.tabela.setItem(r, 4, QTableWidgetItem(municipio.area or ""))
            self.tabela.setItem(r, 5, QTableWidgetItem(municipio.modelo or ""))


        