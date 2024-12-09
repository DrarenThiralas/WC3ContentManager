# -*- coding: utf-8 -*-
"""
Created on Sat Dec  7 15:39:13 2024

@author: Common
"""

from PyQt6.QtWidgets import QWidget, QTreeWidget, QTreeWidgetItem, QLabel, QLineEdit, QPushButton, QDialog, QHBoxLayout, QInputDialog
from expandedConfig import expandedConfig
from sharedObjects import constants, objectData, addIdentations
from contentEditorShared import objectConstants, metaData



class objectEditorHelper:

    def __init__(self, editor):
        self.editor = editor
        self.workData = objectData("Work\\ObjectEditor")
        self.clearObjectData()
        self.metadata = metaData()

    def loadMetaData(self):
        self.metadata.loadMetaData()

    def loadStringData(self):
        self.metadata.loadStringData()

    def clearObjectData(self):
        self.workData.clear()
        #self.workData.mergeData(constants.getBaseObjectData())

    def addObjectData(self, objData):
        self.workData.mergeData(objData)

    def setObjectData(self, objData):
        self.clearObjectData()
        self.addObjectData(objData)

    def applyMetaData(self, field):
        metadata = self.metadata.get(field)
        if metadata != None:
            name = metadata['displayname'][1:-1]
            if name[:8] == "WESTRING":
                name = self.metadata.applyStringLocal(name)
            fieldType = metadata['type'][1:-1]
            category = metadata['category'][1:-1]
            field.setText(self.editor.getColumn('Name'), name)
            field.setText(self.editor.getColumn('Type'), fieldType)
            field.setText(self.editor.getColumn('Category'), category)


    def populateObjects(self):
        self.editor.widget.clear()

        self.loadMetaData()
        self.loadStringData()

        objItems = [QTreeWidgetItem(self.editor.widget) for objType in constants.objTypes]
        for i in range(len(objItems)):
            objItem = objItems[i]
            objType = constants.objTypes[i]
            objItem.setText(self.editor.getColumn('ID'), objType)
            config = self.workData.getConfig(objType)
            if not config == None:
                objectIDs = config.sections()
                objectNames = [config[obj]["Name"] if config.has_option(obj, "Name") else "" for obj in objectIDs]
                objects = [QTreeWidgetItem(objItem) for obj in objectIDs]
                for j in range(len(objects)):
                    objects[j].setText(self.editor.getColumn('ID'), objectIDs[j])
                    objects[j].setText(self.editor.getColumn('Name'), objectNames[j])
                    objectFields = config.options(objectIDs[j])
                    fields = [QTreeWidgetItem(objects[j]) for obj in objectFields]
                    for k in range(len(objectFields)):
                        fields[k].setText(self.editor.getColumn('ID'), objectFields[k])
                        fields[k].setText(self.editor.getColumn('Value'), config[objectIDs[j]][objectFields[k]])
                        self.applyMetaData(fields[k])

    def getSelection(self):
        selection = self.editor.widget.selectedItems()
        selection = selection[0] if len(selection) == 1 else None
        return selection

    def getEntryType(self, entry):
        #print('getting type of '+str(entry))
        if entry == None:
            #print('type is none')
            return entry
        else:
            #print('type is not none')
            i = -1
            while entry != None:
                entry = entry.parent()
                #print('parent is '+str(entry))
                i+=1
            return objectConstants.selectionTypes[i]

    def getSelectedOfType(self, Type):
        selection = self.getSelection()
        selectionType = self.getEntryType(selection)
        return selection if selectionType == Type else None

    def confirmEdit(self):
        line = self.editor.editLine
        selection = self.getSelectedOfType('field')
        if selection == None:
            selection = self.getSelectedOfType('object')
            if selection == None:
                line.setText("")
            else:
                value = line.text()
                selection.setText(self.editor.getColumn('ID'), value)
        else:
            value = line.text()
            selection.setText(self.editor.getColumn('Value'), value)

    def startEdit(self):
        line = self.editor.editLine

        selection = self.getSelectedOfType('field')
        if selection == None:
            selection = self.getSelectedOfType('object')
            if selection == None:
                line.setText("")
            else:
                line.setText(selection.text(self.editor.getColumn('ID')))
        else:
            line.setText(selection.text(self.editor.getColumn('Value')))

    def createNew(self):
        selection = self.getSelection()
        if selection != None:
            Type = self.getEntryType(selection)
            if Type == 'category':
                self.createNewObject()
            else:
                self.createNewField()

    def createNewObject(self):
        selection = self.getSelectedOfType('category')
        if selection != None:
            newObjectID = QInputDialog.getText(self.editor.widget, 'Enter new object ID.', 'ID:')[0]
            newObject = QTreeWidgetItem(selection)
            newObject.setText(self.editor.getColumn('ID'), newObjectID)
            parentField = self.createFieldForObject(newObject, '_parent')
            parentField.setText(self.editor.getColumn('Value'), newObjectID)


    def createFieldForObject(self, obj, name):
        newField = None
        if obj != None and self.getEntryType(obj)=='object':
            newField = QTreeWidgetItem(obj)
            newField.setText(self.editor.getColumn('ID'), name)
            self.applyMetaData(newField)
            newField.setSelected(True)
        return newField


    def createNewField(self):
        selection = self.getSelectedOfType('object')
        selection = (self.getSelectedOfType('field').parent()
                     if selection == None
                     else selection)
        if selection != None:
            newFieldName = QInputDialog.getText(self.editor.widget, "Enter new field name.", "Name:")[0]
            self.createFieldForObject(selection, newFieldName)


    def deleteField(self):
        selection = self.getSelectedOfType('field')
        selection = self.getSelectedOfType('object') if selection == None else selection
        if selection != None:
            selection.setDisabled(True)



    def applyEdits(self):
        widget = self.editor.widget
        topLevelItems = [widget.topLevelItem(i) for i in range(widget.topLevelItemCount()) if widget.topLevelItem(i).childCount()>0]
        for dataType in topLevelItems:
            config = expandedConfig()
            objects = [dataType.child(i) for i in range(dataType.childCount())]
            for obj in objects:
                if obj.isDisabled() == False:
                    fields = [obj.child(i) for i in range(obj.childCount())]
                    for field in fields:
                        if field.isDisabled() == False:
                            section = obj.text(self.editor.getColumn('ID'))
                            option = field.text(self.editor.getColumn('ID'))
                            if not config.has_section(section):
                                config.add_section(section)
                            config[section][option] = field.text(self.editor.getColumn('Value'))
            self.workData.setConfig(dataType.text(self.editor.getColumn('ID')), config)
        #self.workData.subtractData(constants.getBaseObjectData())
        self.editor.objectData.setData(self.workData)
