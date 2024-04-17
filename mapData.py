# -*- coding: utf-8 -*-
"""
Created on Sat Apr 13 03:09:20 2024

@author: maxer
"""

import subprocess, shutil, os, configparser
from lmlParser import lmlParser
from sharedObjects import trigger, triggerCategory, triggerData
config = configparser.ConfigParser(interpolation=None)
config.read("config.ini")
w3x2lni = config["Settings"]["w3x2lni"]

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
        self.trigData = None
        
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
        subprocess.run(["cmd", "/c", 'w2l.exe', "lni", self.w3xpath, cwd+"\\"+self.lnipath], cwd = w3x2lni)
        
        self.trigData = triggerData(self.lnipath+'\\trigger')
        
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
            self.trigData.cleanUnusedVars()
        
        cwd = os.getcwd()
        subprocess.run(["cmd", "/c", 'w2l.exe', "obj", cwd+"\\"+self.lnipath, self.w3xpath], cwd = w3x2lni)
        return self