# -*- coding: utf-8 -*-
"""
Created on Sat Apr 13 03:09:20 2024

@author: maxer
"""

import subprocess, shutil, os
from content.war3Data import contentData
from extra.StormLib import StormLib

class war3Map:

    def __init__(self, mapPath, upPath = None, ymlPath = None):
        """
        Initializes a new war3Map object.

        Parameters
        ----------
        mapPath : string
            Path to the map's .w3x file.
        upPath: string, default = None
            Path to the map's unpacked _w3x folder, if the map is unpacked already.
        ymlPath: string, default = None
            Path to the map's yml folder, if the map is processed already.

        Returns
        -------
        None.

        """
        self.w3xpath = mapPath
        self.name = mapPath.split('/')[-1][:-4]
        self.uppath = upPath
        self.ymlpath = ymlPath
        self.data = self.initData()

    def __str__(self):
        return self.name

    def backup(self):
        """
        Makes a backup of the map in the Backup subfolder.

        Returns
        -------
        self

        """
        #print("Backing up map: "+self.w3xpath)
        #print("Lnipath: "+self.lnipath)
        shutil.copy(self.w3xpath, "Backup\\"+self.name+".w3x")
        return self

    def readData(self, isYml = True):

        if isYml and self.ymlpath != None:
            self.data = contentData().read(self.ymlpath)
        elif self.uppath != None:
            self.data = contentData().read(self.uppath, False)
            
    def getHeader(self):
        
        return self.data.getHeader()

    def unpack(self, debug = False):
        """
        Unpacks the map into a folder, stored in the Work subfolder.

        Returns
        -------
        self

        """

        message = "Unpacking map: "+self.name

        if debug:
            print(message)

        self.backup()
        self.uppath = "Work\\Maps\\"+self.name+"_w3x"
        
        w3x = StormLib.w3x(self.w3xpath)
        w3x.ex_all(self.uppath)

        return self
    
    def decode(self, debug = False):
        """
        Decodes the map into a yml content pack, stored in the Work subfolder.

        Returns
        -------
        None.

        """
        
        if self.uppath == None:
            print("Cannot decode packed map: "+str(self))
        else:
            self.readData(False)
            self.ymlpath = "Work\\Maps\\"+self.name+"_yml"
            self.data.write(self.ymlpath)

    def pack(self, debug = False, cleanVars = True):
        """
        Packs the map's yml object back into its original .w3x.

        Returns
        -------
        self

        """
        message = "Packing map: "+self.name

        if debug:
            print(message)
            
        """
        if cleanVars:
            self.data.trigData = triggerData(self.lnipath+'\\trigger')
            self.data.trigData.cleanUnusedVars()
        """
            
        if self.ymlpath != None and os.path.exists(self.ymlpath):
            
            self.readData()
            
            if self.uppath != None and os.path.exists(self.uppath):
                self.data.write(self.uppath, False)
            else:
                print("Can't pack map: "+self.name)
            
            w3x = StormLib.w3x(self.w3xpath)
            w3x.pack(self.uppath, self.getHeader())


        return self

    def close(self):
        """
        Deletes the yml and unpacked map folders, reversing the effect of unpack() and decode().

        Returns
        -------
        self

        """
        
        if self.uppath != None and os.path.exists(self.uppath):
            shutil.rmtree(self.uppath)
        if self.ymlpath != None and os.path.exists(self.ymlpath):
            shutil.rmtree(self.ymlpath)
        self.uppath = None
        self.ymlpath = None
        self.data = None
