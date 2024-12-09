# -*- coding: utf-8 -*-
"""
Created on Wed Apr 17 04:50:04 2024

@author: maxer
"""

import os
from extra.expandedConfig import expandedConfig
from extra.lmlParser import lmlParser, lmlLine, lmlEntry

class constants:

    def getGlobalOption(option):
        config = expandedConfig()
        config.read("config.ini")
        value = config["Settings"][option]
        return value

    def getBaseObjectData():
        return objectData("Data\\BaseObjectData")

    objTypes = ['ability', 'buff', 'item','unit', 'misc', 'upgrade', 'doodad', 'destructable']
    triggerTypes = ['trigger', 'customscript', 'vars']
    resourceTypes = ['resource']
    defaultTypes = objTypes + triggerTypes + resourceTypes


def addIdentations(filePath):
    """
    Adds identations to the multiline values in the target .ini file.
    Otherwise ConfigParser can't read it.


    Parameters
    ----------
    filePath : string
        The path to the .ini file.

    Returns
    -------
    None.

    """

    file = open(filePath, "r")
    lines = file.readlines()

    def isHeader(line):
        return (line[0] == '[' and line[5] == ']')

    def isComment(line):
        return (line[0]=='-' and line[1] == '-')

    if lines[0][0] != " ":
        newlines = []
        for line in lines:
            newline = line
            if newline.find("=") == -1 and isHeader(newline) == False and isComment(newline) == False:
                newline = " "+newline
            newlines.append(newline)
        file.close()
        file = open(filePath, "w")
        file.writelines(newlines)

    file.close()

class contentContainer:

    def __init__(self, path):
        """
        Initializes a generic content container object that can be
        used to store object, trigger, and resource data together.
        Used by both maps and content packs.

        Parameters
        ----------
        path : string
            Path to the folder where the content is stored.

        Returns
        -------
        None.

        """
        self.path = path
        self.objData = None
        self.triggerData = None
        self.resourceData = None

class triggerVariable:

    def __init__(self, lml):
        """
        Initializes a triggerVariable object.
        This object represents a trigger variable.

        Parameters
        ----------
        lml : string
            lml entry describing the variable.

        Returns
        -------
        None.

        """

        self.name = lml.name.split(":")[0]
        self.type = lml.name.split(":")[1][1:]
        self.initial = None
        self.array = None
        for child in lml.children:
            if child.name[:3] == "Def":
                self.initial = child.name.split(":")[1][1:]
            if child.name[:5] == "Array":
                self.array = child.name.split(":")[1][1:]

    def toLml(self):

        entry = lmlEntry(self.name+": "+self.type, [])
        if self.initial != None:
            entry.children.append(lmlEntry("Def   : "+self.initial, []))
        if self.array != None:
            entry.children.append(lmlEntry("Array : "+self.array, []))

        return entry

    def __str__(self):
        return self.name+": "+self.type

class trigger:

    def __init__(self, path):
        """
        Initializes a trigger object, which represents a single trigger.

        Parameters
        ----------
        path : string
            Path to the trigger file.

        Returns
        -------
        None.

        """
        self.path = path
        self.name = path.split('\\')[-1][:-4]

    def getUsedVarNames(self):
        """
        Returns returns a list of variable names used in the trigger.

        Returns
        -------
        usedVars : list of strings
            A list of variable names used in the trigger.

        """

        usedVars = []

        file = open(self.path, 'r')
        lines = file.readlines()
        file.close()

        for line in lines:
            ln = lmlLine(line).name
            if ln[:3] == "Var" or ln[:5] == "Array":
                usedVars.append(ln.split(":")[-1][1:])

        #print("used vars for "+self.name+": "+str(usedVars))
        return usedVars


class triggerCategory:

    def __init__(self, path):
        """
        Initializes a trigger category.
        This object is supposed to represent a self-contained group of triggers.

        Parameters
        ----------
        path : string
            Path to the trigger category folder inside the content pack.

        Returns
        -------
        None.

        """
        self.path = path
        self.name = path.split('\\')[-1]
        self.triggers = [trigger(self.path+'\\'+f.name) for f in os.scandir(self.path) if f.name != 'catalog.lml']



class triggerData:

    def __init__(self, path):
        """
        Initializes a trigger data object.
        This object represents trigger data.
        It consists of:
            1. A custom script
            2. A variable list
            3. One or several trigger categories

        Parameters
        ----------
        path : string
            Path to the folder that the trigger data is in.

        Returns
        -------
        None.

        """
        self.path = path
        self.customScript = self.path+'\\code.j'
        self.varFile = self.path+"\\variable.lml"
        self.categories = [triggerCategory(self.path+'\\'+folder.name) for folder in os.scandir(self.path) if folder.is_dir()]

    def getVars(self):

        allVars = []

        if os.path.exists(self.varFile):
            parser = lmlParser()
            variableTarget = parser.read(self.varFile)
            allVars = [triggerVariable(x) for x in variableTarget.children]

        #print ("vars: "+str([str(var) for var in allVars]))
        return allVars

    def setVars(self, trigVars):

        parser = lmlParser()
        variableTarget = lmlEntry("root", [var.toLml() for var in trigVars])
        parser.write(variableTarget, self.varFile)

    def cleanUnusedVars(self):

        variables = self.getVars()

        usedVarNames = []
        for cat in self.categories:
            for trig in cat.triggers:
                trigUsedNames = trig.getUsedVarNames()
                usedVarNames = usedVarNames + trigUsedNames

        trigVars = [var for var in variables if var.name in usedVarNames]
        #print ("clean vars: "+str([str(var) for var in variables]))
        #print("\n")
        #print("lml: "+str(variables[2].toLml()))

        self.setVars(trigVars)



class objectData:

    def __init__(self, path):
        """
        Initializes a new objectData object.
        This object represents object editor data.

        Parameters
        ----------
        path : string
            Path to the object data folder.

        Returns
        -------
        None.

        """
        self.path = path

    def clearType(self, dataType):
        if self.getHasType(dataType):
            os.remove(self.getTypeFile(dataType))

    def clear(self):
        for Type in self.getTypeList():
            self.clearType(Type)

    def getTypeFile(self, dataType):
        return self.path+"\\"+dataType+".ini"

    def getHasType(self, dataType):
        return os.path.exists(self.getTypeFile(dataType))

    def getTypeList(self):
        return [Type for Type in constants.objTypes if self.getHasType(Type)]

    def getConfig(self, dataType):

        sourcePath = self.path+"\\"+dataType+".ini"
        sourceConfig = None
        if os.path.exists(sourcePath):

            sourceConfig = expandedConfig()

            try:
                sourceConfig.read(sourcePath)
            except:
                addIdentations(sourcePath)
                sourceConfig.read(sourcePath)

        return sourceConfig

    def setConfig(self, dataType, targetConfig):

        targetPath = self.path+"\\"+dataType+".ini"
        with open(targetPath, 'w') as configfile:
            targetConfig.write(configfile)
            configfile.close()

    def mergeDataType(self, newData, dataType):

        config = newData.getConfig(dataType).merge(self.getConfig(dataType), isCopy = False)
        self.setConfig(dataType, config)

    def mergeData(self, newData):
        for dataType in newData.getTypeList():
            self.mergeDataType(newData, dataType)

    def subtractDataType(self, dataToRemove, dataType):

        config = [self.getConfig(dataType), dataToRemove.getConfig(dataType)]

        for section in config[1].sections():
            for option in config[1].options(section):
                if config[0].has_option(option):
                    config[0].remove_option(section, option)
                    if len(config[0].options(section)) == 0:
                        config[0].remove_section(section)

        self.setConfig(dataType, config[0])

    def subtractData(self, dataToRemove):

        for dataType in self.getTypeList():
            if dataType in dataToRemove.getTypeList():
                self.subtractDataType(dataToRemove, dataType)

    def setData(self, data):
        self.clear()
        self.mergeData(data)



class resourceData:

    def __init__(self, path):
        """
        Initializes a new resourceData object.
        This object represents imported asset data.

        Parameters
        ----------
        path : string
            Path to the resource data folder.

        Returns
        -------
        None.

        """
        self.path = path
