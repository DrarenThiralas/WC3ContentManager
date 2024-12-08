# -*- coding: utf-8 -*-
"""
Created on Fri Dec  6 15:19:20 2024

@author: Common
"""

from PyQt6.QtWidgets import QWidget, QTreeWidget, QLineEdit, QPushButton
from PyQt6.QtCore import Qt
from objectEditorHelper import objectEditorHelper

class objectEditor:

    def __init__(self):
        self.helper = objectEditorHelper(self)
        self.objectData = None
        self.columns = ["ID", "Name", "Value", "Type", "Category"]
        self.initSpace()
        self.initWidget()
        self.initEditLine()

    def getColumn(self, name):
        return self.columns.index(name)

    def setObjectData(self, objectData):
        self.objectData = objectData
        self.helper.setObjectData(self.objectData)
        self.helper.populateObjects()

    def initSpace(self):
        self.space = QWidget()
        self.space.setGeometry(20, 20, 1100-40, 780-120-40)

    def initWidget(self):
        self.widget = QTreeWidget(parent=self.space)
        self.widget.setGeometry(20, 20, 1100-80-40, 780-120-40-80)
        self.widget.setColumnCount(len(self.columns))
        self.widget.setHeaderLabels(self.columns)
        self.widget.itemSelectionChanged.connect(self.helper.startEdit)

    def initEditLine(self):
        self.editLine = QLineEdit(parent = self.space)
        self.editLine.setGeometry(20, 780-120-40-40, 1100-120-200, 20)
        self.editButton = QPushButton(parent = self.space)
        self.editButton.setGeometry(1100-120-120, 780-120-40-40, 60, 20)
        self.editButton.setText("Apply")
        self.editButton.clicked.connect(self.helper.confirmEdit)
        self.editButton.setShortcut(Qt.Key.Key_Enter)
