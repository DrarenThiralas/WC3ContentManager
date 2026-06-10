#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 10 21:14:45 2026

@author: drarenthiralas
"""

import os
from extra.common import constants
from extra.war3MapParsers.strings import strings

class stringData:
    
    def __init__(self):
        self.data = []
        
    def setData(self, data):
        self.data = data
        return self
    
    def getData(self):
        return self.data
    
    def read(self, path, isYml = True):
        
        f = os.path.join(path, constants.mapStrings)
        if not os.path.exists(f):
            print("Cannot find trigger string file.")
            return None
        else:
            self.data = strings().read(f).getData()
            
        return self
    
    def write(self, path, isYml = True):
        
        f = os.path.join(path, constants.mapStrings)
        strings().write(f, self.data)
            
        return self
    