# -*- coding: utf-8 -*-
"""
Created on Sat Dec  7 15:39:13 2024

@author: Common
"""

from PyQt6.QtWidgets import QWidget, QTreeWidget, QTreeWidgetItem, QLabel, QLineEdit, QPushButton, QDialog, QHBoxLayout
from expandedConfig import expandedConfig
from sharedObjects import constants, objectData, addIdentations

metaDataFiles = ['UnitMetaData.ini',
                 'MiscMetaData.ini',
                 'AbilityMetaData.ini',
                 'UpgradeMetaData.ini',
                 'DestructableMetaData.ini',
                 'DoodadMetaData.ini']
stringDataFiles = ['UI\\WorldEditStrings.txt']

class metaData:

    def __init__(self):

        self.configs = {}
        self.strconfs = {}
        self.cache = {}
        self.strcache = {}

    def loadMetaData(self):
        for file in metaDataFiles:
            self.configs[file] = expandedConfig()
            try:
                self.configs[file].read('Data\\'+file)
            except:
                addIdentations('Data\\'+file)
                self.configs[file].read('Data\\'+file)

    def loadStringData(self):
        for file in stringDataFiles:
            self.strconfs[file] = expandedConfig()
            try:
                self.strconfs[file].read('Data\\'+file)
            except:
                addIdentations('Data\\'+file)
                self.strconfs[file].read('Data\\'+file)

    def get(self, field):

        f = None
        file = None

        name = field.text(0)
        fieldObject = field.parent()
        fieldObjectType = fieldObject.parent()
        fieldObjectTypeName = fieldObjectType.text(0)

        if fieldObjectTypeName == 'item':
            file = 'UnitMetaData.ini'
            f = lambda section: (('useitem' in section)
                                 and (int(section['useitem'])==1))
        elif fieldObjectTypeName == 'unit':
            file = 'UnitMetaData.ini'
            f = lambda section: ((int(section['useunit'])==1)
                                 or (int(section['usehero'])==1)
                                 or (int(section['usebuilding'])==1))
        elif fieldObjectTypeName == 'misc':
            file = 'MiscMetaData.ini'
            f = lambda section: (section['section'][1:-1] == 'Misc')
        elif fieldObjectTypeName == 'ability':
            file = 'AbilityMetaData.ini'
            f = lambda section: True
        elif fieldObjectTypeName == 'upgrade':
            file = 'UpgradeMetaData.ini'
            f = lambda section: True
        elif fieldObjectTypeName == 'destructable':
            file = 'DestructableMetaData.ini'
            f = lambda section: True
        elif fieldObjectTypeName == 'doodad':
            file = 'DoodadMetaData.ini'
            f = lambda section: True


        ans = self.cache[name] if f != None and name in self.cache else self.find(file, name, f)
        self.cache.update([[name, ans]])
        return ans

    def applyStringLocal(self, name):
        if name in self.strcache:
            return self.strcache[name]
        else:
            for key in self.strconfs:
                strconf = self.strconfs[key]
                if strconf.has_section('WorldEditStrings'):
                    for option in strconf.options('WorldEditStrings'):
                        if option.lower() == name.lower():
                            ans = strconf['WorldEditStrings'][option]
                            self.strcache.update([[name, ans]])
                            return ans
        return ''


    def find(self, file, name, validator = None):
        if file != None:
            #print('running find metadata for '+name)
            for section in self.configs[file].sections():
                #print('section '+section)
                fieldName = self.configs[file][section]['field'][1:-1]
                #print('getting data for '+fieldName+', section '+section)
                if fieldName.lower() == name.lower() and validator != None and validator(self.configs[file][section]):
                    return self.configs[file][section]
        return None

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

    def confirmEdit(self):
        selection = self.editor.widget.selectedItems()
        line = self.editor.editLine
        if len(selection) != 1 or selection[0].childCount() != 0:
            line.setText("")
        else:
            value = line.text()
            selection[0].setText(self.editor.getColumn('Value'), value)

    def startEdit(self):
        selection = self.editor.widget.selectedItems()
        line = self.editor.editLine
        if len(selection) != 1:
            line.setText("")
        else:
            line.setText(selection[0].text(self.editor.getColumn('Value')))

    def applyEdits(self):
        widget = self.editor.widget
        topLevelItems = [widget.topLevelItem(i) for i in range(widget.topLevelItemCount()) if widget.topLevelItem(i).childCount()>0]
        for dataType in topLevelItems:
            config = expandedConfig()
            objects = [dataType.child(i) for i in range(dataType.childCount())]
            for obj in objects:
                fields = [obj.child(i) for i in range(obj.childCount())]
                for field in fields:
                    section = obj.text(self.editor.getColumn('ID'))
                    option = field.text(self.editor.getColumn('ID'))
                    if not config.has_section(section):
                        config.add_section(section)
                    config[section][option] = field.text(self.editor.getColumn('Value'))
            self.workData.setConfig(dataType.text(self.editor.getColumn('ID')), config)
        #self.workData.subtractData(constants.getBaseObjectData())
        self.editor.objectData.setData(self.workData)
