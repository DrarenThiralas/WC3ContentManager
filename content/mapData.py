# -*- coding: utf-8 -*-
"""
Created on Sat Apr 13 03:09:20 2024

@author: maxer
"""

import subprocess, shutil, os
from extra.sharedObjects import triggerData, objectData, resourceData, contentContainer, constants
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
        self.uppathath = upPath
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

    def initData(self):

        if self.lnipath != None:
            self.data = contentContainer(self.lnipath)
            #TODO: replace these with new yml data classes
            self.data.triggerData = triggerData(self.lnipath+'\\trigger')
            self.data.objData = objectData(self.lnipath)
            self.data.resourceData = resourceData(self.lnipath)

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
            #TODO: decode map
        
            self.initData()

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
        subprocess.run(["cmd", "/c", 'w2l.exe', "obj", cwd+"\\"+self.lnipath, self.w3xpath], cwd = constants.getGlobalOption('w3x2lni'))
        return self

    def close(self):
        """
        Deletes the unpacked map folder, reversing the effect of unpack().

        Returns
        -------
        self

        """

        if self.lnipath != None and os.path.exists(self.lnipath):
            shutil.rmtree(self.lnipath)
        self.lnipath = None
        self.data = None
