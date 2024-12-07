# -*- coding: utf-8 -*-
"""
Created on Sat Dec  7 15:39:13 2024

@author: Common
"""

from PyQt6.QtWidgets import QWidget, QTreeWidget, QTreeWidgetItem, QLabel, QLineEdit, QPushButton, QDialog, QHBoxLayout
import configparser
from sharedObjects import constants, objectData

class objectEditorHelper:

    def __init__(self, editor):
        self.editor = editor
        self.workData = objectData("Work\\ObjectEditor\\")
        self.clearObjectData()

    def clearObjectData(self):
        self.workData.clear()
        self.workData.mergeData(constants.getBaseObjectData())

    def addObjectData(self, objData):
        self.workData.mergeData(objData)

    def populateObjects(self):
        self.editor.widget.clear()
        objItems = [QTreeWidgetItem(self.editor.widget) for objType in constants.objTypes]
        for i in range(len(objItems)):
            objItem = objItems[i]
            objType = constants.objTypes[i]
            objItem.setText(0, objType)
            config = self.workData.getConfig(objType)
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
            self.workData.setConfig(dataType.text(0), config)
        self.workData.subtractData(constants.getBaseObjectData())
        self.editor.objectData.setData(self.workData)
