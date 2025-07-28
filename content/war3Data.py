# -*- coding: utf-8 -*-
"""
Created on Sat Apr 13 03:09:20 2024

@author: maxer
"""

import subprocess, shutil, os
from extra.sharedObjects import triggerData, objectData, resourceData, contentContainer, constants

class war3Data:

    def __init__(self, path):
        """
        Initializes a new war3Data object.

        Parameters
        ----------
        path : string
            Path to the data files.
            
        Returns
        -------
        None.

        """
        self.path = path
        self.name = path.split('/')[-1][:-4]

    def __str__(self):
        return self.name

    def backup(self):
        """
        Makes a backup of the map in the Backup subfolder.

        Returns
        -------
        self

        """
        shutil.copy(self.path, "Backup\\"+self.path.split('/')[-1])
        return self

    def initData(self):

        if self.lnipath != None:
            self.data = contentContainer(self.lnipath)
            self.data.triggerData = triggerData(self.lnipath+'\\trigger')
            self.data.objData = objectData(self.lnipath)
            self.data.resourceData = resourceData(self.lnipath)


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

        if self.path != None and os.path.exists(self.path):
            shutil.rmtree(self.path)
        self.path = None
        self.data = None
        
class war3DataRaw(war3Data):
    
    def __init__(self, path):
        war3Data.init(self, path)
        
    def __str__(self):
        return self.name
    
    def backup(self):
        war3Data.backup(self)
        
    def close(self):
        war3Data.close(self)
        
    def unpack(self, lnipath, debug = False):
        
        message = "Unpacking data: "+self.name
        if debug:
            print(message)

        self.backup()
    
    def toLni(self, debug = False):
        lnipath = self.path[:-4]+"_lni"
        self.unpack(lnipath, debug)
        return war3DataLni(lnipath)
        
class war3DataLni(war3Data):
    
    def __init__(self, path):
        war3Data.init(self, path)
        self.data = self.initData()
