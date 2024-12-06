# -*- coding: utf-8 -*-
"""
Created on Sat Apr 13 03:34:10 2024

@author: maxer
"""

import subprocess, shutil, os

from mapData import war3Map
from sharedObjects import constants, contentContainer
from contentPackParts import objectPack, triggerPack, resourcePack

class contentPack:
    
    def __init__(self, path):
        """
        Initializes a content pack object.
        This object represents all of a content pack.
        It consists of:
            1. Object Data
            2. Trigger Data
            3. Resource Data

        Parameters
        ----------
        path : string
            Path to the content pack folder.

        Returns
        -------
        None.

        """
        self.path = path
        self.name = path.split('\\')[-1]
        self.data = contentContainer(path)
        self.data.objData = objectPack(path)
        if os.path.exists(path+'\\triggerData'):
            self.data.triggerData = triggerPack(path+'\\triggerData')
        else:
            self.data.triggerData = None
        if os.path.exists(path+'\\imp.ini'):
            self.data.resourceData = resourcePack(path)
        else:
            self.data.resourceData = None    
            
    def getObjConfDict(self):
        """
        Returns the pack's object data as a dictionary.
        This exists solely for UI reasons.

        Returns
        -------
        confDict : dict
            Object data dictionary.

        """
        confDict = dict()
        for Type in constants.objTypes:
            if os.path.exists(self.path+"\\"+Type+".ini"):
                confDict[Type]=self.data.objData.getConfig(Type)
        return confDict
        
    def apply(self, w3map, dataTypes=constants.defaultTypes):
        """
        Applies the specified data types from
        the content pack to the target map.

        Parameters
        ----------
        w3map : war3Map
            Map to apply the pack to.
        dataTypes : list of string, optional
            List of data types to apply. The default is:
            ['ability', 'buff', 'item','unit', 'misc', 'trigger', 'customscript', 'vars', 'resource'].

        Returns
        -------
        war3Map
            The map that the pack was applied to.

        """
        
        objectTypesArg = [Type for Type in dataTypes if Type in constants.objTypes]
        triggerTypesArg = [Type for Type in dataTypes if Type in constants.triggerTypes]
            
        self.data.objData.apply(w3map, objectTypesArg)
        if self.data.triggerData != None:
            self.data.triggerData.apply(w3map, triggerTypesArg)
        if self.data.resourceData != None:
            self.data.resourceData.apply(w3map)
            
        return w3map
        