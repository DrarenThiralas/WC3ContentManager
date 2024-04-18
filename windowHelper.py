# -*- coding: utf-8 -*-
"""
Created on Thu Apr 18 06:25:00 2024

@author: maxer
"""
import os, shutil
from PyQt6.QtWidgets import QFileDialog, QGridLayout, QCheckBox, QProgressDialog, QInputDialog, QLabel
from PyQt6.QtCore import Qt
from contentPack import contentPack
from mapData import war3Map
from sharedObjects import objTypes

class windowHelper:
    
    def __init__(self, window):
        self.window = window
        
    def selectMapsFunction(self):
        """
        The function for the select maps button.
        Opens a map selection dialog.

        Returns
        -------
        None.

        """
        
        file = str(QFileDialog.getOpenFileNames(None, "Select Maps")[0])
        self.window.mapsPathInput.setText(file)
        
    def importContentPacks(self):
        """
        The function that populates the content pack checklist.
        Scans the ContentPacks subdirectory.

        Returns
        -------
        None.

        """
        
        layout = QGridLayout()
        
        contentPacks = os.scandir("ContentPacks\\")
        i = 0
        for pack in contentPacks:
            if pack.is_dir():
                checkbox = QCheckBox(str(pack.name))
                layout.addWidget(checkbox, i, 0)
                i+=1
                
        geometry = (40, 140, 820, 40*i)
        
        return geometry, layout
    
    def getActivePacks(self):
        """
        The function that returns the currently active content packs from the checklist.

        Returns
        -------
        activePacks : list of contentPack objects

        """
        
        activePacks = []
        
        layout = self.packSelectorSpace.layout()
        
        index = layout.count()-1
        while(index >= 0):
            myWidget = layout.itemAt(index).widget()
            if myWidget.isChecked():
                activePacks.append(contentPack("ContentPacks\\"+myWidget.text()))
            index -=1
            
        return activePacks
    
    def executeFunction(self):
        """
        The function for the Apply Content Packs button.
        Applies the selected content packs to the selected maps.

        Returns
        -------
        None.

        """

        contentPacks = self.getActivePacks()
        maps = list(str(self.window.mapsPathInput.text())[:-1].split(','))
        maps = [mp[2:-1] for mp in maps]
        maps = [war3Map(mp) for mp in maps]
        
        progressTotal = 3*len(maps)+2
        progressDialog = QProgressDialog("Initializing...", "Cancel", 0, progressTotal)
        progressDialog.setWindowModality(Qt.WindowModality.WindowModal)
        
        shutil.rmtree("Temp\\", ignore_errors=True)
        os.mkdir("Temp\\")
        progressDialog.setValue(1)
        
        

        for mp, i in zip(maps, range(len(maps))):
            progressDialog.setLabelText("Unpacking map: "+maps[i].name)
            maps[i] = mp.unpack()
            progressDialog.setValue(i+1)
            
            
        for pack in contentPacks:
            progressDialog.setLabelText("Applying pack: "+pack.name)
            maps = list(map(pack.apply, maps))
            progressDialog.setValue(i+1+len(maps))
            
            
        for mp, i in zip(maps, range(len(maps))):      
            progressDialog.setLabelText("Repacking map: "+maps[i].name)
            maps[i] = mp.pack()
            progressDialog.setValue(i+1+len(maps)*2)
            
        progressDialog.setValue(progressTotal)
            
        self.window.resultMsg.setText("Content packs applied!")
        
    def selectMapFunction(self):
        
        file = str(QFileDialog.getOpenFileName(None, "Select a map to export content from")[0])
        if file:
            packName = QInputDialog().getText(None, "Enter new pack name", "Name:")[0]
            if os.path.exists("ContentPacks\\"+packName):
                self.window.resultMsg.setText("Content pack already exists.")
            else:
                mp = war3Map(file)
                mp.unpack()
                shutil.copytree(mp.lnipath+"\\table", "ContentPacks\\"+packName, dirs_exist_ok = True)
                shutil.copytree(mp.lnipath+"\\resource", "ContentPacks\\"+packName+"\\resource", dirs_exist_ok = True)
                shutil.copytree(mp.lnipath+"\\trigger", "ContentPacks\\"+packName+"\\triggerData", dirs_exist_ok = True)
                newPack = contentPack("ContentPacks\\"+packName)
                self.populateSettings(newPack)
                self.window.settingsDialog.open()
        
    def populateSettings(self, pack):
        
        confDict = pack.getObjConfDict()
        i = 0
        for key, conf in confDict.items():
            headerLabel = QLabel(text=str(key), parent=self.window.settingsDialog)
            headerLabel.setGeometry(30+110*i, 20, 40, 20)
            for j in range(len(conf.sections())):
                checkbox = QCheckBox(text=str(conf.sections()[j]), checked=True)
                self.window.settingsLayout.addWidget(checkbox, j+1, i)
            i+=1
        self.window.settingsListSpace.setGeometry(20, 40, 110*len(confDict), 25*max(list(map(lambda x: len(x[1]), confDict.items()))))


    def getActiveSettings(self):

        activeSettings = dict()
        
        layout = self.window.settingsListSpace.layout()
        
        index = layout.count()-1
        while(index >= 0):
            myWidget = layout.itemAt(index).widget()
            if myWidget.isChecked():
                Type = objTypes[layout.getItemPosition(index)[1]]
                if Type not in activeSettings:
                    activeSettings[Type] = []
                activeSettings[Type].append(contentPack("ContentPacks\\"+myWidget.text()))
            index -=1
            
        return activeSettings


    def finalizeContentPack(self):
        
        self.window.resultMsg.setText("New content pack created!")
        self.importContentPacks()
        
            