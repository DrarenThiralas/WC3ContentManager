# -*- coding: utf-8 -*-
"""
Created on Thu Apr 18 06:24:31 2024

@author: maxer
"""

from PyQt6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QDialog, QGridLayout
from PyQt6.QtGui import QIcon
from mainWindowHelper import mainWindowHelper

from contentEditorWindow import contentEditorWindow

class mainWindow:
    
    def __init__(self):
        self.helper = mainWindowHelper(self)
        self.initWindow()
        self.helper.checkConfig()
        self.initMapSelector()
        self.initPackSelector()
        self.initResMsg()
        self.initContentEditor()
        self.initExecuteButton()
        self.initExportButton()
        self.initExportSettings()
        
    def run(self):
        self.window.show()
        
    def initWindow(self):
        self.window = QWidget()
        self.window.setWindowTitle("WCIII Content Manager")
        self.icon = QIcon("w3cm.ico")
        self.window.setWindowIcon(self.icon)
        self.window.setGeometry(200, 40, 900, 800)
        self.header = QLabel("<h1>Warcraft III Content Manager</h1>", parent=self.window)
        self.header.move(60, 15)
        
    def initMapSelector(self):
        
        self.mapsPathInput = QLineEdit(parent=self.window)
        self.mapsPathInput.setGeometry(220, 100, 600, 30)
        self.selectMapsButton = QPushButton(text='Select Map Files', parent=self.window)
        self.selectMapsButton.setGeometry(30, 100, 180, 30)
        self.selectMapsButton.clicked.connect(self.helper.selectMapsFunction)
        
    def initPackSelector(self):
        
        self.packSelectorHeader = QLabel(parent=self.window)
        self.packSelectorHeader.setGeometry(40, 120, 820, 40)
        
        self.packSelectorSpace = QWidget(parent=self.window)
        geometry, layout = self.helper.importContentPacks()
        
        if geometry[3] > 0:
            self.packSelectorHeader.setText("Content Packs:")
        else:
            self.packSelectorHeader.setText("No Content Packs Found!")

        self.packSelectorSpace.setGeometry(*geometry)
        self.packSelectorSpace.setLayout(layout)
        
    def initResMsg(self):
        
        self.resultMsg = QLabel("", parent=self.window)
        self.resultMsg.setGeometry(450-110, 660, 220, 40)
        
    def initExecuteButton(self):
        
        self.executeButton = QPushButton(text='Apply Content Packs', parent=self.window)
        self.executeButton.setGeometry(340-220, 720, 220, 40)
        self.executeButton.clicked.connect(self.helper.executeFunction)
        
    def initContentEditor(self):
        
        self.contentEditor = contentEditorWindow(self.window)
        
    def initExportButton(self):
        
        self.exportButton = QPushButton(text='Export Content', parent=self.window)
        self.exportButton.setGeometry(340+220, 720, 220, 40)
        self.exportButton.clicked.connect(self.helper.selectMapFunction)
        
    def initExportSettings(self):
        
        self.settingsDialog = QDialog()
        self.settingsDialog.setGeometry(100, 100, 700, 880)
        self.settingsLayout = QGridLayout()
        self.settingsListSpace = QWidget(parent=self.settingsDialog)
        self.settingsListSpace.setLayout(self.settingsLayout)
        self.settingsDialogOk = QPushButton(text = 'Confirm', parent=self.settingsDialog)
        self.settingsDialogOk.setGeometry(350-40, 820, 80, 40)
        self.settingsDialogOk.clicked.connect(self.settingsDialog.accept)
        self.settingsDialog.accepted.connect(self.helper.finalizeContentPack)