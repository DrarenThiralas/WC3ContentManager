# -*- coding: utf-8 -*-
"""
Created on Fri Dec  6 14:30:16 2024

@author: Common
"""

from PyQt6.QtWidgets import QPushButton, QDialog, QTabWidget
from contentEditor.objectEditor.objectEditorMain import objectEditor

class contentEditorHelper:

    def __init__(self, editor):
        self.editor = editor

    def applyChanges(self):
        self.editor.objectEditor.helper.applyEdits()

class contentEditorWindow:

    def __init__(self, parent):
        self.helper = contentEditorHelper(self)
        self.contentContainer = None
        self.initWindow(parent)
        self.initMainLayout()
        self.initObjectEditor()
        self.initOkButton()

    def setContent(self, contentContainer):
        self.contentContainer = contentContainer
        self.objectEditor.setObjectData(contentContainer.objData)

    def initWindow(self, parent):
        self.window = QDialog(parent=parent)
        self.window.setWindowTitle("Content Editor")
        self.window.setGeometry(200, 40, 1100, 780)

    def initOkButton(self):
        self.windowOkButton = QPushButton(text = 'OK', parent=self.window)
        self.windowOkButton.setGeometry(1100-80-40, 780-60, 80, 40)
        self.windowOkButton.clicked.connect(self.window.accept)
        self.window.accepted.connect(self.helper.applyChanges)

    def initMainLayout(self):
        self.tabSpace = QTabWidget(parent=self.window)
        self.tabSpace.setGeometry(20, 20, 1100-40, 780-120)

    def initObjectEditor(self):
        self.objectEditor = objectEditor()
        self.tabSpace.addTab(self.objectEditor.space, "Objects")
