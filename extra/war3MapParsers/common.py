# -*- coding: utf-8 -*-
"""
Created on Mon Jul 28 08:22:43 2025

@author: alivemary
"""

import struct

def btoInt(b):
    return int.from_bytes(b, "little", signed = True)

def btoFloat(b):
    return struct.unpack('<1f', b)[0]

def btoStr(b):
    return b.decode()

class bytesreader:
    
    def __init__(self, b):
        self.b = b
        self.size = len(b)
        self.i = 0
    
    def readInt(self):
        ans = btoInt(self.b[self.i:self.i+4])
        self.i += 4
        return ans
    
    def readShort(self):
        ans = btoInt(self.b[self.i:self.i+2])
        self.i += 2
        return ans
    
    def readByte(self):
        ans = btoInt(self.b[self.i:self.i+1])
        self.i += 1
        return ans
    
    def readFloat(self):
        ans = btoFloat(self.b[self.i:self.i+4])
        self.i += 4
        return ans
    
    def readChars(self, n):
        ans = btoStr(self.b[self.i:self.i+n])
        self.i += n
        return ans
    
    def readStr(self):
        search = self.b[self.i:]
        #print("searching for terminator in bytes: " + str(search))
        term = search.index(0)
        ans = btoStr(self.b[self.i:self.i+term])
        self.i += term+1
        return ans
    
    def isEnd(self):
        return self.i >= self.size