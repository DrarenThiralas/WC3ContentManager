# -*- coding: utf-8 -*-
"""
Created on Thu Apr 18 06:25:00 2024

@author: maxer
"""
import os, shutil
from extra.expandedConfig import expandedConfig
from PyQt6.QtWidgets import QFileDialog, QCheckBox, QProgressDialog, QInputDialog, QLabel
from PyQt6.QtCore import Qt
from contentManager.contentPack import contentPack
from contentManager.mapData import war3Map
from sharedObjects import constants
from extra.mpqExtractor import dataConstants, dataMaker

class mainWindowHelper:

    def __init__(self, window):
        """
        Initializes the helper class that contains extra functions for the main window.

        Parameters
        ----------
        window : mainWindow
            The program's main window.

        Returns
        -------
        None.

        """
        self.window = window

    def checkConfig(self):
        """
        Checks that the config exists, and is valid. Promts the user to fix it if not.

        Returns
        -------
        None.

        """
        configExists = True
        war3Exists = True
        w3x2lniExists = True
        MPQEditorExists = True

        configPath = "config.ini"
        if os.path.exists(configPath):
            config = expandedConfig()
            config.read(configPath)

            if config.has_option("Settings", "w3x2lni"):
                w3x2lni = config["Settings"]["w3x2lni"]+"\\w2l.exe"
                if not os.path.exists(w3x2lni):
                    w3x2lniExists = False
            else:
                w3x2lniExists = False

            if config.has_option("Settings", "mpqedit"):
                MPQEdit = config["Settings"]["mpqedit"]+"\\MPQEditor.exe"
                if not os.path.exists(MPQEdit):
                    MPQEditorExists = False
            else:
                MPQEditorExists = False

            if config.has_option("Settings", "war3"):
                war3Path = config["Settings"]["war3"]+"\\war3.exe"
                if not os.path.exists(war3Path):
                    war3Exists = False
            else:
                war3Exists = False

        else:
            configExists = False
            war3Exists = False
            w3x2lniExists = False
            MPQEditorExists = False

        newConfig = expandedConfig()

        if configExists:
            newConfig.read(configPath)
        if not newConfig.has_section("Settings"):
            newConfig.add_section("Settings")

        def folderSelect(tooltip, setting):
            folder = QFileDialog.getExistingDirectory(self.window.window, tooltip)
            newConfig["Settings"][setting] = folder
            with open(configPath, 'w') as configfile:
                newConfig.write(configfile)
                configfile.close()
            self.checkConfig()

        if not war3Exists:
            folderSelect("Warcraft 3 not found. Select your Warcraft 3 folder.", "war3")
        elif not w3x2lniExists:
            folderSelect("w3x2lni not found. Select your w3x2lni folder.", "w3x2lni")
        elif not MPQEditorExists:
            folderSelect("Ladik's MPQ Editor not found. Select your MPQ Editor folder.", "mpqedit")

    def checkData(self):

        dataPath = "Data\\"
        dataExists = os.path.exists(dataPath)

        if not dataExists:
            self.prepareData()

    def prepareData(self):

        os.makedirs('Data')
        self.prepareObjectMetaData()
        self.prepareObjectStringData()
        self.prepareBaseObjectData()


    def prepareObjectMetaData(self):

        extractor = dataMaker('War3x.mpq')
        for entry in dataConstants.metaDataFiles:
            targetName = entry.split('\\')[1][:-4]
            targetPath = 'Data\\'+targetName+'.ini'
            extractor.process(entry, targetPath)

    def prepareObjectStringData(self):

        extractor = dataMaker('War3xlocal.mpq')
        for entry in dataConstants().stringDataFiles:
            extractor.extract(entry, "Data")

    def prepareBaseObjectData(self):

        self.a = 1


    def selectMapsFunction(self):
        """
        The function for the select maps button.
        Opens a map selection dialog.

        Returns
        -------
        None.

        """

        fileList = QFileDialog.getOpenFileNames(None, "Select Maps")[0]
        print('file list: '+str(fileList))
        maps = [war3Map(file) for file in fileList]
        self.clearWork("Maps")
        for openMap in maps:
            openMap.unpack(True)
        self.window.mapList.helper.openMaps.setMaps(maps)
        self.window.mapList.refresh()

    def clearWork(self, name):

        if os.path.exists("Work\\"+name):
            shutil.rmtree("Work\\"+name)

    def executeFunction(self):
        """
        The function for the Apply Content Packs button.
        Applies the selected content packs to the selected maps.

        Returns
        -------
        None.

        """

        contentPacks = self.window.packList.helper.getActivePacks()
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

    def openContentEditor(self, content):

        self.window.contentEditor.window.open()
        self.window.contentEditor.setContent(content)


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
                Type = constants.objTypes[layout.getItemPosition(index)[1]]
                if Type not in activeSettings:
                    activeSettings[Type] = []
                activeSettings[Type].append(contentPack("ContentPacks\\"+myWidget.text()))
            index -=1

        return activeSettings


    def finalizeContentPack(self):

        self.window.resultMsg.setText("New content pack created!")
        self.window.packList.refresh()
