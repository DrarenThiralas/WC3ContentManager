#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 11 20:27:12 2026

@author: drarenthiralas
"""

import os
from extra.common import constants
from extra.war3MapParsers.bytesreader import bytesreader
from extra.war3MapParsers.byteswriter import byteswriter

class mapinfo:
    
    def __init__(self):
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
        
        saves = reader.readInt()
        edversion = reader.readInt()
        
        name = reader.readStr()
        author = reader.readStr()
        desc = reader.readStr()
        playersrec = reader.readStr()
        
        # Basic map data (0-5)
        self.data = [saves, edversion, name, author, desc, playersrec]
        
        # Map bounds data + flags at the end (6-20)
        for i in range(8):
            self.data.append(reader.readFloat())
        for i in range(7):
            self.data.append(reader.readInt())
        
        # Main ground type (21)
        self.data.append(reader.readChars(1))
        # Loading screen ID (22)
        self.data.append(reader.readInt())
        # Loading screen data (23-26)
        for i in range(4):
            self.data.append(reader.readStr())
            
        # Game data set ID (27)
        self.data.append(reader.readInt())
        # Prologue screen data (usually empty strings) (28-31)
        for i in range(4):
            self.data.append(reader.readStr())
            
        # Fog ID (32)
        self.data.append(reader.readInt())
        # Fog data (33-39)
        for i in range(3):
            self.data.append(reader.readFloat())
        for i in range(4):
            self.data.append(reader.readByte())
        
        # Weather ID (40)
        self.data.append(reader.readInt())
        
        # Sound environment (41)
        self.data.append(reader.readStr())
        
        # Light ID (42)
        self.data.append(reader.readChar())
        
        # Water tint data (43-46)
        for i in range(4):
            self.data.append(reader.readByte())
            
        # Number of players (47)
        n = reader.readInt()
        self.data.append(n)
        
        #TODO: finish parsing the file
            
            
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
        