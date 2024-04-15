# -*- coding: utf-8 -*-
"""
Created on Sun Apr 14 18:58:37 2024

@author: maxer
"""

import os, shutil

from mapData import war3Map

class resourceData:
    
    def __init__(self, packPath):
        """
        Initializes a new resourceData object.
        This object represents imported asset data in a content pack.

        Parameters
        ----------
        packPath : string
            Path to the content pack folder.

        Returns
        -------
        None.

        """
        self.packPath = packPath
        
    def updateIni(self, w3map):
        """
        Updates the imp.ini file that list all the imported resources for the map.

        Parameters
        ----------
        w3map : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        """
        
        imppath = w3map.lnipath+"\\table\\imp.ini"
        
        if os.path.exists(imppath):
            
            file = open(self.packPath+"\\imp.ini", "r")
            resourceLines = file.readlines()[1:-1]
            file.close()
        
            file = open(imppath, "r")
            impini = file.readlines()
            file.close()
            
            newLines = []
            
            for line in resourceLines:
                if not line in impini:
                    newLines.append(line)
            
            impini = impini[:-1]+newLines+impini[-1:]
            
            file = open(imppath, "w")
            file.writelines(impini)
            file.close()
            
        else:
            
            shutil.copy(self.packPath+"\\imp.ini", imppath)
    
    def apply(self, w3map):
        """
        Applies the resource data to the given map.

        Parameters
        ----------
        w3map : war3Map object
            The map to apply resource data to.

        Returns
        -------
        None.

        """
        
        shutil.copytree(self.packPath+'\\resource', w3map.lnipath+"\\resource", dirs_exist_ok = True)
        self.updateIni(w3map)
       
        