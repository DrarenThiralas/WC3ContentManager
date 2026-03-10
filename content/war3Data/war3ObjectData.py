#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 10 12:17:23 2026

@author: drarenthiralas
"""

import os
from extra.common import constants
from content.war3Types.war3Object import war3Object
from extra.war3MapParsers.customdata import customdata

class objectDataType:
    
    def __init__(self, tp):
        """
        Initializes a new objectDataType object.
        This object represents object editor data of a specific type.
        (i.e. unit or item).

        Parameters
        ----------
        tp : string
            Type of the object data.

        Returns
        -------
        None.

        """
        self.type = tp
        self.data = None
        
    def __contains__(self, o):
        matches = [obj == o for obj in self.data]
        return (True in matches)
        
    def read(self, path, isYml = True):
        """
        Read the object data type from a folder.

        Parameters
        ----------
        path : string
            Path to the object data folder.
        isYml : bool, optional
            Whether the data is stored in yml or w3x format. The default is True (yml).

        Returns
        -------
        self

        """
        if isYml:
            for subdir, dirs, files in os.walk(path+'\\'+self.type):
                self.data = [war3Object().read(subdir+'\\'+f) for f in files]
        else:
            self.data = customdata(self.type).read(path).getData()            
        return self
    
    def write(self, path, isYml = True):
        """
        Write the object data type to a folder (or file).

        Parameters
        ----------
        path : string
            Path to the object data folder.
        isYml : bool, optional
            Whether the data is to be stored in yml or w3x format. The default is True (yml).

        Returns
        -------
        self

        """
        
        if isYml:
            for obj in self.data:
                obj.write(path+'\\'+self.type)
        else:
            customdata(self.type).write(path, self.data)
        
        return self

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
        if not os.path.exists(path):
            os.makedirs(path)

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

            print('getting config for '+sourcePath)
            sourceConfig = expandedConfig()

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