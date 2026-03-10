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
        self.data = dict()
        
    def __contains__(self, o):
        matches = [obj == o for obj in self.data.values()]
        return (True in matches)
    
    def __eq__(self, o):
        matches = [obj in self for obj in o.data.value()]
        if (False in matches):
            return False
        matches = [obj in o for obj in self.data.values()]
        if (False in matches):
            return False
        return True
        
    def __ne__(self, o):
        return not self == o
    
    def __getitem__(self, key):
        return self.data[key]
    
    def __setitem__(self, key, item):
        if key != 0:
            self.data[key]=item
        else:
            self.data[item['id']]=item
            
    def __iadd__(self, odt):
        for key, value in odt.data:
            if key in self.data:
                self.data[key]+=value
            else:
                self.data[key]=value
                
    def __isub__(self, odt):
        for key, value in odt.data:
            if value in self:
                del self.data[key]
            elif key in self.data:
                self.data[key]-=value
        
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
            f = path+'\\'+self.type
            if not os.path.exists(f):
                return None
            for subdir, dirs, files in os.walk(f):
                data = [war3Object().read(subdir+'\\'+file) for file in files]
                keys = [obj.id for obj in data]
                self.data = dict(zip(keys, data))
        else:
                data = customdata(self.type).read(path).getData()
                if type(data) == type(None):
                    return None
                keys = [obj.id for obj in data]
                self.data = dict(zip(keys, data))
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
            for obj in self.data.values():
                obj.write(path+'\\'+self.type)
        else:
            customdata(self.type).write(path, self.data)
        
        return self

class objectData:

    def __init__(self):
        """
        Initializes a new objectData object.
        This object represents object editor data,
        and consists of a collection of objectDataTypes.

        Parameters
        ----------
        None.

        Returns
        -------
        None.

        """
        
        self.data = dict()
        
    def __contains__(self, o):
        if type(o) == objectDataType:    
            return o.type in self.data
        elif type(o) == str:
            return o in self.data



    def __getitem__(self, dataType):
        if dataType in self:
           return self.data[dataType]
       
    def __setitem__(self, dataType, odt):
        self.data[dataType] = odt
       
    def clearType(self, dataType):
        if dataType in self:
            del self.data[dataType]

    def clear(self):
        self.data = dict()

    def getTypes(self):
        return self.data.keys()

    def mergeDataType(self, dataType, newData):
        if dataType in self:
            self[dataType] += newData
        else:
            self[dataType] = newData

    def __iadd__(self, newData):
        for dataType in newData.getTypes():
            self.mergeDataType(dataType, newData[dataType])

    def subtractDataType(self, dataType, dataToRemove):
        if dataType in self:
            self[dataType] -= dataToRemove

    def __isub__(self, dataToRemove):
        for dataType in self.getTypes():
            if dataType in dataToRemove.getTypes():
                if dataToRemove[dataType] == self[dataType]:
                    del self[dataType]
                else:
                    self.subtractDataType(dataType, dataToRemove[dataType])
                    
    def read(self, path, isYml = True):
        """
        Read the object data from a folder.

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
        
        for dataType in constants.objTypes:
            
            f = "\\data" if isYml else ""
            
            if os.path.exists(path+f):
                odt = objectDataType(dataType).read(path+f, isYml)
                if type(odt) != type(None):
                    self[dataType] = odt
        
        return self
    
    def write(self, path, isYml = True):
        """
        Write the object data to a folder.

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
        
        for value in self.data.values():
        
            f = "\\data" if isYml else ""
            value.write(path+f, isYml)
        
        return self