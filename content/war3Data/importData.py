#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 10 21:45:02 2026

@author: drarenthiralas
"""

import os, shutil
from extra.common import constants
from extra.war3MapParsers.imports import imports

class importData:
    
    def __init__(self):
        self.path = None
        self.data = None
        
    def setData(self, data):
        self.data = data
        return self
    
    def getData(self):
        return self.data
    
    def getPath(self):
        return self.path
    
    def setPath(self, path):
        self.path = path
        return self
    
    def read(self, path, isYml = True):
        if isYml:
            self.path = path+"\\import"
            f = self.path+"\\imports.txt"
            with open(f, 'r') as file:
                self.setData(file.readlines())
                file.close()
        else:
            f = path+'\\'+constants.mapImports
            self.path = path
            self.setData(imports().read(f).getData())
        return self
    
    def write(self, path, isYml = True):
        f = path
        if isYml:
            f = f+"\\import"
            if not os.path.exists(f):
                os.makedirs(f)
            with open(f+'\\imports.txt', 'w') as file:
                file.writelines([line+"\n" for line in self.data])
                file.close()
        else:
            imports().write(f, self.data)
            
        if type(self.path) != type(None):
            #TODO: copy the actual import files with shutil
            return 0
            
        return self
    
    
    
    