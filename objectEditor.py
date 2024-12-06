# -*- coding: utf-8 -*-
"""
Created on Fri Dec  6 15:19:20 2024

@author: Common
"""

from PyQt6.QtWidgets import QWidget, QTreeWidget, QTreeWidgetItem, QLabel, QLineEdit, QPushButton, QDialog, QHBoxLayout
from sharedObjects import objTypes, objectData

class objectEditorHelper:
    
    def __init__(self, editor):
        self.editor = editor
        
    def populateObjects(self):
        self.editor.widget.clear()
        objItems = [QTreeWidgetItem(self.editor.widget) for objType in objTypes]
        for i in range(len(objItems)):
            objItem = objItems[i]
            objType = objTypes[i]
            objItem.setText(0, objType)
            config = self.editor.objectData.getConfig(objType)
            if not config == None:
                objectIDs = config.sections()
                objectNames = [config[obj]["Name"] if config.has_option(obj, "Name") else "" for obj in objectIDs]
                objects = [QTreeWidgetItem(objItem) for obj in objectIDs]
                for j in range(len(objects)):
                    objects[j].setText(0, objectIDs[j])
                    objects[j].setText(1, objectNames[j])
                    objectFields = config.options(objectIDs[j])
                    fields = [QTreeWidgetItem(objects[j]) for obj in objectFields]
                    for k in range(len(objectFields)):
                        fields[k].setText(0, objectFields[k])
                        fields[k].setText(2, config[objectIDs[j]][objectFields[k]])

class objectEditor:
    
    def __init__(self, parent):
        self.helper = objectEditorHelper(self)
        self.objectData = None
        self.initWidget(parent)
        
    def setObjectData(self, objectData):
        self.objectData = objectData
        self.helper.populateObjects()
        
    def initWidget(self, parent):
        self.widget = QTreeWidget(parent=parent)
        self.widget.setGeometry(20, 80, 1100-40, 780-120-40)
        self.widget.setColumnCount(3)
        self.widget.setHeaderLabels(["ID", "Name", "Value"])
            
        