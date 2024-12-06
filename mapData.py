# -*- coding: utf-8 -*-
"""
Created on Sat Apr 13 03:09:20 2024

@author: maxer
"""

import subprocess, shutil, os, configparser
from lmlParser import lmlParser
from sharedObjects import trigger, triggerCategory, triggerData, objectData, resourceData, contentContainer, constants

class war3Map:
    
    def __init__(self, mapPath):
        """
        Initializes a new war3Map object.

        Parameters
        ----------
        mapPath : string
            Path to the map's .w3x file.

        Returns
        -------
        None.

        """
        self.w3xpath = mapPath
        self.name = mapPath.split('/')[-1][:-4]
        self.lnipath = None
        self.data = None
        
    def backup(self):
        """
        Makes a backup of the map in the Backup subfolder.

        Returns
        -------
        self

        """
        shutil.copy(self.w3xpath, "Backup\\"+self.name+".w3x")
        return self
        
    def unpack(self, debug = False):
        """
        Unpacks the map into a lni object, stored in the Temp subfolder.

        Returns
        -------
        self

        """
        
        message = "Unpacking map: "+self.name
        
        if debug:
            print(message)
        
        self.backup()
        self.lnipath = "Temp\\"+self.name+"_tmp"
        cwd = os.getcwd()
        subprocess.run(["cmd", "/c", 'w2l.exe', "lni", self.w3xpath, cwd+"\\"+self.lnipath], cwd = constants.w3x2lni())
        
        self.data = contentContainer(self.lnipath)
        self.data.triggerData = triggerData(self.lnipath+'\\trigger')
        self.data.objData = objectData(self.lnipath)
        self.data.resourceData = resourceData(self.lnipath)
        
        return self
    
    def pack(self, debug = False, cleanVars = True):
        """
        Packs the map's lni object back into its original .w3x.

        Returns
        -------
        self

        """
        message = "Packing map: "+self.name
        
        if debug:
            print(message)
            
        if cleanVars:
            self.data.trigData = triggerData(self.lnipath+'\\trigger')
            self.data.trigData.cleanUnusedVars()
        
        cwd = os.getcwd()
        subprocess.run(["cmd", "/c", 'w2l.exe', "obj", cwd+"\\"+self.lnipath, self.w3xpath], cwd = constants.w3x2lni())
        return self