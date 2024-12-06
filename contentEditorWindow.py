# -*- coding: utf-8 -*-
"""
Created on Fri Dec  6 14:30:16 2024

@author: Common
"""

from PyQt6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QDialog, QHBoxLayout
from PyQt6.QtGui import QIcon
from contentEditorHelper import contentEditorHelper
from objectEditor import objectEditor

class contentEditorWindow:
    
    def __init__(self, parent):
        self.helper = contentEditorHelper(self)
        self.contentContainer = None
        self.initWindow(parent)
        self.initMainLayout()
        self.initObjectEditor()
        
    def setContent(self, contentContainer):
        self.contentContainer = contentContainer
        self.objectEditor.setObjectData(contentContainer.objData)
        
    def initWindow(self, parent):   
        self.window = QDialog(parent=parent)
        self.window.setWindowTitle("Content Editor")
        self.window.setGeometry(200, 40, 1100, 780)
        self.windowOkButton = QPushButton(text = 'Apply', parent=self.window)
        self.windowOkButton.setGeometry(1100-80-40, 780-60, 80, 40)
        self.windowOkButton.clicked.connect(self.window.accept)
        self.window.accepted.connect(self.helper.finalizeContentPack)
        
    def initMainLayout(self):
        self.tabLayout = QHBoxLayout()
        self.tabSpace = QWidget(parent=self.window)
        self.tabSpace.setGeometry(20, 20, 1100-40, 40)
        self.tabNames = ['Objects', 'Triggers', 'Resources']
        for name in self.tabNames:
            button = QPushButton(text = name)
            self.tabLayout.addWidget(button)
        self.tabSpace.setLayout(self.tabLayout)
        self.activeTabId = 0
        
    def initObjectEditor(self):
        self.objectEditor = objectEditor(self.window)
