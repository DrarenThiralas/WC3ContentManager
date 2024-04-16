# -*- coding: utf-8 -*-
"""
Created on Fri Apr 12 18:12:14 2024

@author: maxer
"""

import sys
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
import subprocess, shutil, os

from mapData import war3Map
from contentPack import contentPack

    
def selectMapsFunction():
    """
    The function for the select maps button.
    Opens a map selection dialog.

    Returns
    -------
    None.

    """
    
    file = str(QFileDialog.getOpenFileNames(None, "Select Maps")[0])
    mapPathLine.setText(file)
    
def selectMapFunction():
    
    file = str(QFileDialog.getOpenFileName(None, "Select a map to export content from")[0])
    if file:
        packName = QInputDialog().getText(None, "Enter new pack name", "Name:")[0]
        if os.path.exists("ContentPacks\\"+packName):
            resultMsg.setText("Content pack already exists.")
        else:
            mp = war3Map(file)
            mp.unpack()
            shutil.copytree(mp.lnipath+"\\table", "ContentPacks\\"+packName, dirs_exist_ok = True)
            shutil.copytree(mp.lnipath+"\\resource", "ContentPacks\\"+packName, dirs_exist_ok = True)
            shutil.copytree(mp.lnipath+"\\trigger", "ContentPacks\\"+packName+"\\triggerData", dirs_exist_ok = True)
            newPack = contentPack("ContentPacks\\"+packName)
            populateSettings(newPack)
            settingsDialog.open()
    
def populateSettings(pack):
    
    confDict = pack.getObjConfDict()
    i = 0
    for key, conf in confDict.items():
        headerLabel = QLabel(text=str(key), parent=settingsDialog)
        headerLabel.setGeometry(30+110*i, 20, 40, 20)
        for j in range(len(conf.sections())):
            checkbox = QCheckBox(text=str(conf.sections()[j]), checked=True)
            settingsLayout.addWidget(checkbox, j+1, i)
        i+=1
    settingsListSpace.setGeometry(20, 40, 110*len(confDict), 25*max(list(map(lambda x: len(x[1]), confDict.items()))))
    
    
def finalizeContentPack():
    
    resultMsg.setText("New content pack created!")
    importContentPacks()


    
def executeFunction():
    """
    The function for the Apply Content Packs button.
    Applies the selected content packs to the selected maps.

    Returns
    -------
    None.

    """

    contentPacks = getActivePacks()
    maps = list(str(mapPathLine.text())[:-1].split(','))
    maps = [mp[2:-1] for mp in maps]
    maps = [war3Map(mp) for mp in maps]
    
    progressTotal = 3*len(maps)+2
    progressDialog = QProgressDialog("Importing...", "Cancel", 0, progressTotal)
    progressDialog.setWindowModality(Qt.WindowModality.WindowModal)
    
    shutil.rmtree("Temp\\", ignore_errors=True)
    os.mkdir("Temp\\")
    progressDialog.setValue(1)

    for mp, i in zip(maps, range(len(maps))):       
        maps[i] = mp.unpack(True)
        progressDialog.setValue(i+1)
        
    for pack in contentPacks:
        maps = list(map(pack.apply, maps))
        progressDialog.setValue(i+1+len(maps))
        
    for mp, i in zip(maps, range(len(maps))):       
        maps[i] = mp.pack(True)
        progressDialog.setValue(i+1+len(maps)*2)
        
    progressDialog.setValue(progressTotal)
        
    resultMsg.setText("Content packs imported!")
    
        
def importContentPacks():
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
    packListSpace.setGeometry(40, 140, 820, 40*i)
    
    packListSpace.setLayout(layout)
    
def getActivePacks():
    """
    The function that returns the currently active content packs from the checklist.

    Returns
    -------
    activePacks : list of contentPack objects

    """
    
    activePacks = []
    
    layout = packListSpace.layout()
    
    index = layout.count()-1
    while(index >= 0):
        myWidget = layout.itemAt(index).widget()
        if myWidget.isChecked():
            activePacks.append(contentPack("ContentPacks\\"+myWidget.text()))
        index -=1
        
    return activePacks

    

app = QApplication([])

# Window and title

window = QWidget()
window.setWindowTitle("WCIII Content Manager")
icon = QIcon()
icon.addFile("w3cm.ico")
window.setWindowIcon(icon)
window.setGeometry(100, 100, 900, 800)
helloMsg = QLabel("<h1>Warcraft III Content Manager</h1>", parent=window)
helloMsg.move(60, 15)

# Map selection UI

mapPathLine = QLineEdit(parent=window)
mapPathLine.setGeometry(220, 100, 600, 30)
selectMapButton = QPushButton(text='Select Map Files', parent=window)
selectMapButton.setGeometry(30, 100, 180, 30)
selectMapButton.clicked.connect(selectMapsFunction)

# Content Pack selection UI

packListSpace = QWidget(parent=window)


importContentPacks()



# Feedback message for responsiveness

resultMsg = QLabel("", parent=window)
resultMsg.setGeometry(450-110, 660, 220, 40)

# The main "do stuff" button

executeButton = QPushButton(text='Apply Content Packs', parent=window)
executeButton.setGeometry(340-220, 720, 220, 40)
executeButton.clicked.connect(executeFunction)

exportButton = QPushButton(text='Export Content', parent=window)
exportButton.setGeometry(340+220, 720, 220, 40)
exportButton.clicked.connect(selectMapFunction)

settingsDialog = QDialog()
settingsDialog.setGeometry(100, 100, 700, 600)
settingsListSpace = QWidget(parent=settingsDialog)
settingsLayout = QGridLayout()
settingsListSpace.setLayout(settingsLayout)
settingsDialogOk = QPushButton(text = 'Confirm', parent=settingsDialog)
settingsDialogOk.setGeometry(350-40, 540, 80, 40)
settingsDialogOk.clicked.connect(settingsDialog.accept)
settingsDialog.accepted.connect(finalizeContentPack)

window.show()

sys.exit(app.exec())