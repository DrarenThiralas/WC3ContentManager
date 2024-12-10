# -*- coding: utf-8 -*-
"""
Created on Mon Dec  9 14:02:57 2024

@author: Common
"""

import os
from PyQt6.QtWidgets import QWidget, QLabel, QCheckBox, QPushButton, QGridLayout
from contentManager.contentPack import contentPack

class contentPackListHelper:

    def __init__(self, packList):
        self.packList = packList

    def importContentPacks(self):
        """
        The function that populates the content pack checklist.
        Scans the ContentPacks subdirectory.

        Returns
        -------
        None.

        """

        layout = QGridLayout()

        if not os.path.exists("ContentPacks\\"):
            os.makedirs("ContentPacks\\")

        contentPacks = os.scandir("ContentPacks\\")
        i = 0
        for pack in contentPacks:
            if pack.is_dir():
                checkbox = QCheckBox(str(pack.name))
                editButton = QPushButton("Edit")
                deleteButton = QPushButton("Delete")
                packName = checkbox.text()
                functionFactory = lambda x: lambda: self.packList.window.helper.openContentEditor(contentPack("ContentPacks\\"+x).data)
                editButton.clicked.connect(functionFactory(packName))
                layout.addWidget(checkbox, i, 0)
                layout.addWidget(editButton, i, 1)
                layout.addWidget(deleteButton, i, 2)
                i+=1

        geometry = (40, 40, 320, 40*i)

        return geometry, layout

    def getActivePacks(self):
        """
        The function that returns the currently active content packs from the checklist.

        Returns
        -------
        activePacks : list of contentPack objects

        """

        activePacks = []

        layout = self.packList.packSelector.layout()

        index = layout.count()-1
        while(index >= 0):
            myWidget = layout.itemAt(index).widget()
            if myWidget.isChecked():
                activePacks.append(contentPack("ContentPacks\\"+myWidget.text()))
            index -=1

        return activePacks

class contentPackList:

    def __init__(self, window):
        self.window = window
        self.helper = contentPackListHelper(self)
        self.packSelectorSpace = None
        self.initPackList()


    def initPackList(self):
        parent = self.window.window
        if self.packSelectorSpace != None:
            self.packSelectorSpace.setParent(None)
        self.packSelectorSpace = QWidget(parent=parent)
        self.packSelectorSpace.setGeometry(480, 120, 400, 500)
        self.packSelectorHeader = QLabel(parent=self.packSelectorSpace)
        self.packSelectorHeader.setGeometry(40, 10, 240, 40)
        self.packSelector = QWidget(parent=self.packSelectorSpace)
        geometry, layout = self.helper.importContentPacks()

        if geometry[3] > 0:
            self.packSelectorHeader.setText("Content Packs:")
        else:
            self.packSelectorHeader.setText("No Content Packs Found!")

        self.packSelector.setGeometry(*geometry)
        self.packSelector.setLayout(layout)


    def refresh(self):
        self.initPackList()
        self.packSelectorSpace.show()
