# -*- coding: utf-8 -*-
"""
Created on Mon Dec  9 17:52:57 2024

@author: Common
"""

import os
from PyQt6.QtWidgets import QWidget, QLabel, QCheckBox, QPushButton, QGridLayout
from contentManager.mapData import war3Map


class openMaps:

    def __init__(self):
        self.maps = None
        self.mapFilePath = "Work\\openmaps.txt"
        self.loadMaps()

    def loadMaps(self):
        print('loading maps')
        maps = None
        if os.path.exists(self.mapFilePath):
            print('opening map list')
            with open(self.mapFilePath, 'r') as mapFile:
                lines = mapFile.readlines()
                lines = [line[:-1] for line in lines if len(line)>1]
                for ln in lines:
                    print(ln)
                names = [line.split('/')[-1][:-4] for line in lines]
                lnis = ['Work\\Maps\\'+name+'_w3x' for name in names]
                for ln in lnis:
                    print(ln)
                maps = [war3Map(line, lni) for line, lni in zip(lines, lnis)]
                for mp in maps:
                    print('loading map: '+mp.name)
                mapFile.close()

        self.setMaps(maps)

    def setMaps(self, maps):
        self.maps = maps
        with open(self.mapFilePath, 'w') as mapFile:
            mapFile.writelines([mp.w3xpath+"\n" for mp in maps])
            mapFile.close()

    def closeMap(self, mp):
        self.maps.remove(mp)
        self.setMaps(self.maps)
        mp.close()

class mapListHelper:

    def __init__(self, mapList):
        self.mapList = mapList
        self.openMaps = openMaps()

    def importMaps(self):
        """
        The function that populates the map list.

        Returns
        -------
        None.

        """

        layout = QGridLayout()

        maps = self.openMaps.maps
        i = 0
        if maps != None:
            for mp in maps:
                if os.path.exists(mp.lnipath):
                    checkbox = QCheckBox(str(mp.name))
                    closeButton = QPushButton("Close")
                    #deleteButton = QPushButton("Delete")
                    #mapName = checkbox.text()
                    functionFactory = lambda: lambda: self.openMaps.closeMap(mp)
                    closeButton.clicked.connect(functionFactory())
                    layout.addWidget(checkbox, i, 0)
                    layout.addWidget(closeButton, i, 1)
                    #layout.addWidget(deleteButton, i, 2)
                    i+=1

        geometry = (40, 40, 320, 40*i)

        return geometry, layout

class mapList:

    def __init__(self, window):
        self.window = window
        self.helper = mapListHelper(self)
        self.mapSpace = None
        self.initMapList()

    def initMapList(self):
        parent = self.window.window
        if self.mapSpace != None:
            self.mapSpace.setParent(None)
        self.mapSpace = QWidget(parent = parent)
        self.mapSpace.setGeometry(20, 120, 400, 500)
        self.mapHeader = QLabel(parent = self.mapSpace)
        self.mapHeader.setGeometry(40, 10, 240, 40)
        self.mapSelector = QWidget(parent=self.mapSpace)
        geometry, layout = self.helper.importMaps()

        if geometry[3] > 0:
            self.mapHeader.setText("Maps:")
        else:
            self.mapHeader.setText("No Maps Open.")

        self.mapSelector.setGeometry(*geometry)
        self.mapSelector.setLayout(layout)

    def refresh(self):
        self.initMapList()
        self.mapSpace.show()
