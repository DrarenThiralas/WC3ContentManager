# -*- coding: utf-8 -*-
"""
Created on Sun Jul 27 13:16:43 2025

@author: alivemary
"""

from extra.war3MapParsers.common import bytesreader

class imports:
    
    def __init__(self, path):
        self.path = path
        self.size = 0
        self.data = None
        
    def read(self):
        file = open(self.path, 'rb')
        self.b = file.read()
        file.close()
        
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
            self.read()
            self.parse()
        return self.data