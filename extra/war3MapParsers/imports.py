# -*- coding: utf-8 -*-
"""
Created on Sun Jul 27 13:16:43 2025

@author: alivemary
"""

import os
from extra.common import constants
from extra.war3MapParsers.bytesreader import bytesreader
from extra.war3MapParsers.byteswriter import byteswriter

class imports:
    
    def __init__(self):
        self.size = 0
        self.data = None
        
    def read(self, path):
        self.path = path
        with open(self.path, 'rb') as file:
            self.b = file.read()
            file.close()
        return self
        
    def parse(self):
        reader = bytesreader(self.b)
        version = reader.readInt()
        self.size = reader.readInt()
        self.data = []
        for i in range(self.size):
            isFull = reader.readByte() > 8
            path = ("war3mapImported\\" if not isFull else "") + reader.readStr()
            self.data.append(path)
            
    def getData(self):
        if self.data == None:
            self.parse()
        return self.data
    
    def setData(self, data):
        self.data = data
        return self
    
    def write(self, path, data=None):
        if type(data) != type(None):
            self.setData(data)
        self.path = path
        
        if not os.path.exists(path):
            os.makedirs(path)
        f = constants.mapImports
        with open(self.path+'\\'+f, 'wb') as file:
            writer = byteswriter(file)
            
            #Write version
            writer.writeInt(1)
            
            #Write list
            for line in self.data:
                byte, l = None, None
                if line[:16] == "war3mapImported\\":
                    byte, l = 8, line[16:]
                else:
                    byte, l = 13, line
                writer.writeByte(byte)
                writer.writeString(l)
            
            file.close()
        
        return self
        
        
        