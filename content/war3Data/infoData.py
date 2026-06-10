#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 11 20:25:53 2026

@author: drarenthiralas
"""

import os
from extra.common import constants
from extra.war3MapParsers.mapinfo import mapinfo

class infoData:
    
    def __init__(self):
        self.data = dict()
        
    def setData(self, data):
        self.data = data
        return self
        
    def getData(self):
        return self.data
    
    def getHeader(self):
        
        info = mapinfo()
        info.b = self.data['war3map.w3i']
        info = info.getData()
        
        # Construct w3x header
        header = bytearray()
        header.append("HM3W".encode("UTF-8"))
        header.append(int.to_bytes(0, 4, 'little'))
        
        header.append(info[2].encode('UTF-8')) # Map Name
        header.append(int.to_bytes(info[20], 4, 'little')) # Map Flags
        header.append(int.to_bytes(info[47], 4, 'little')) # Number of players
        
        # Add padding
        num = 512-len(header)
        header.append(bytes(num))
        
        return header
    
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