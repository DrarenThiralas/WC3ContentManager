# -*- coding: utf-8 -*-
"""
Created on Fri Dec  6 15:19:20 2024

@author: Common
"""

from PyQt6.QtWidgets import QWidget, QTreeWidget, QTreeWidgetItem, QLabel, QLineEdit, QPushButton, QDialog, QHBoxLayout
from PyQt6.QtCore import Qt
import configparser
from sharedObjects import constants

class objectEditorHelper:
    
    def __init__(self, editor):
        self.editor = editor
        
    def populateObjects(self):
        self.editor.widget.clear()
        objItems = [QTreeWidgetItem(self.editor.widget) for objType in constants.objTypes]
        for i in range(len(objItems)):
            objItem = objItems[i]
            objType = constants.objTypes[i]
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
                        
    def confirmEdit(self):
        selection = self.editor.widget.selectedItems()
        line = self.editor.editLine
        if len(selection) != 1 or selection[0].childCount() != 0:
            line.setText("")
        else:
            value = line.text()
            selection[0].setText(2, value)
        
    def startEdit(self):
        selection = self.editor.widget.selectedItems()
        line = self.editor.editLine
        if len(selection) != 1:
            line.setText("")
        else:
            line.setText(selection[0].text(2))
            
    def applyEdits(self):
        widget = self.editor.widget
        topLevelItems = [widget.topLevelItem(i) for i in range(widget.topLevelItemCount()) if widget.topLevelItem(i).childCount()>0]
        for dataType in topLevelItems: 
            config = configparser.ConfigParser(comment_prefixes=('--'), strict=False, interpolation=None)
            objects = [dataType.child(i) for i in range(dataType.childCount())]
            for obj in objects:
                fields = [obj.child(i) for i in range(obj.childCount())]
                for field in fields:
                    section = obj.text(0)
                    option = field.text(0)
                    if not config.has_section(section):
                        config.add_section(section)
                    config[section][option] = field.text(2)
            self.editor.objectData.setConfig(dataType.text(0), config)
            

class objectEditor:
    
    def __init__(self):
        self.helper = objectEditorHelper(self)
        self.objectData = None
        self.initSpace()
        self.initWidget()
        self.initEditLine()
        
    def setObjectData(self, objectData):
        self.objectData = objectData
        self.helper.populateObjects()
        
    def initSpace(self):
        self.space = QWidget()
        self.space.setGeometry(20, 20, 1100-40, 780-120-40)
        
    def initWidget(self):
        self.widget = QTreeWidget(parent=self.space)
        self.widget.setGeometry(20, 20, 1100-80-40, 780-120-40-80)
        self.widget.setColumnCount(3)
        self.widget.setHeaderLabels(["ID", "Name", "Value"])
        self.widget.itemSelectionChanged.connect(self.helper.startEdit)
        
    def initEditLine(self):
        self.editLine = QLineEdit(parent = self.space)
        self.editLine.setGeometry(20, 780-120-40-40, 1100-120-200, 20)
        self.editButton = QPushButton(parent = self.space)
        self.editButton.setGeometry(1100-120-120, 780-120-40-40, 60, 20)
        self.editButton.setText("Apply")
        self.editButton.clicked.connect(self.helper.confirmEdit)
        self.editButton.setShortcut(Qt.Key.Key_Enter)