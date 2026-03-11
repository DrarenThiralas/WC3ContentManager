#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 11 20:25:53 2026

@author: drarenthiralas
"""

import os
from extra.common import constants

class infoData:
    
    def __init__(self):
        self.data = dict()
        
    def setData(self, data):
        self.data = data
        return self
        
    def getData(self):
        return self.data
        
    def read(self, path, isYml = True):
        
        f = path + ('\\info\\' if isYml else '\\')
        if not os.path.exists(f):
            return None
        files = constants.mapInfoParts
        for file in files:
            if os.path.exists(f+file):
                with open(f+file, 'rb') as b:
                    self.data[file] = b.read()
                    b.close()
                    
        if len(self.data) == 0:
            return None
                    
        return self
    
    def write(self, path, isYml = True):
        
        f = path + ('\\info\\' if isYml else '\\')
        if not os.path.exists(f):
            os.makedirs(f)
        for name, b in self.data.items():
            with open(f+name, 'wb') as file:
                file.write(b)
                file.close()
        
        return self