#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 10 21:45:02 2026

@author: drarenthiralas
"""

import os
from extra.common import constants
from extra.war3MapParsers.imports import imports

class importData:
    
    def __init__(self):
        self.data = dict()
        
    def setData(self, data):
        self.data = data
        return self
    
    def getData(self):
        return self.data
    
    def read(self, path, isYml = True):
        if isYml:
            
            f = path+"\\import"
            if not os.path.exists(f):
                return None
            for subdir, dirs, files in os.walk(f):
                for fl in files:
                    with open(subdir+'\\'+fl, 'rb') as file:
                        cleanpath = (subdir+'\\'+fl)[len(f)+1:]
                        self.data[cleanpath] = file.read()
                        print('Reading import file: '+subdir+'\\'+fl)
                        file.close()
                    
        else:
            
            f = path+'\\'+constants.mapImports
            if not os.path.exists(f):
                return None
            filelist = imports().read(f).getData()
            for fl in filelist:
                if os.path.exists(path+'\\'+fl):
                    with open(path+'\\'+fl, 'rb') as file:
                        self.data[fl] = file.read()
                        print('Reading import file: '+path+'\\'+fl)
                        file.close()
                else:
                    print("Cannot find import: "+fl)
            
        return self
    
    def write(self, path, isYml = True):
        
        f = path
        
        if isYml:
            f = f+"\\import"
        else:
            imports().write(f, list(self.data.keys()))
            
        for fl, b in self.data.items():
            if not os.path.exists(os.path.dirname(f+'\\'+fl)):
                os.makedirs(os.path.dirname(f+'\\'+fl))
            with open(f+'\\'+fl, 'wb') as file:
                file.write(b)
                file.close()
            
        return self
    
    
    
    