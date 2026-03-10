# -*- coding: utf-8 -*-
"""
Created on Sat Apr 13 03:09:20 2024

@author: maxer
"""

from content.war3Data.objectData import objectData
from content.war3Data.importData import importData

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
        self.objData = None
        self.importData = None
    
    def read(self, path, isYml = True):
        self.objData = objectData().read(path, isYml)
        self.importData = importData().read(path, isYml)
    
        return self
        
    def write(self, path, isYml = True):
        writeParts = [self.objData, self.importData]
        for part in writeParts:
            if type(part) != type(None):
                part.write(path, isYml)
                
        return self