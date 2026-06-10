# -*- coding: utf-8 -*-
"""
Created on Sat Apr 13 03:09:20 2024

@author: maxer
"""

from content.war3Data.stringData import stringData
from content.war3Data.objectData import objectData
from content.war3Data.importData import importData
from content.war3Data.mapData import mapData
from content.war3Data.infoData import infoData

class contentData:

    def __init__(self):
        """
        Initializes a new contentData object,
        containing all types of Warcraft 3 data.

        Parameters
        ----------
        None.
            
        Returns
        -------
        None.

        """
        self.stringData = None
        self.objData = None
        self.importData = None
        self.mapData = None
        self.infoData = None
        
    def getHeader(self):
        return self.infoData.getHeader()
    
    def read(self, path, isYml = True):
                
        self.stringData = stringData().read(path, isYml)
        self.objData = objectData().read(path, isYml)
        self.importData = importData().read(path, isYml)
        self.mapData = mapData().read(path, isYml)
        self.infoData = infoData().read(path, isYml)
    
        return self
        
    def write(self, path, isYml = True):
        
        writeParts = [self.stringData, self.objData, self.importData, self.mapData, self.infoData]
        for part in writeParts:
            if type(part) != type(None):
                part.write(path, isYml)
                
        return self