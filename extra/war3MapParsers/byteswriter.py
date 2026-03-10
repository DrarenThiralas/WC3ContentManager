#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 10 13:15:52 2026

@author: drarenthiralas
"""

import struct

class byteswriter:
    
    def __init__(self, b):
        self.b = b
        self.i = 0
        
    def writeInt(self, w):
        ans = int.to_bytes(w, 4, 'little')
        self.i += 4
        self.b.write(ans)
        
    def writeShort(self, w):
        ans = int.to_bytes(w, 2, 'little')
        self.i += 2
        self.b.write(ans)
        
    def writeByte(self, w):
        ans = int.to_bytes(w, 1, 'little')
        self.i += 1
        self.b.write(ans)
        
    def writeFloat(self, w):
        #Note: may have issues compressing precision, must test
        ans = struct.pack('<1f', w)
        self.i += 4
        self.b.write(ans)
        
    def writeChars(self, w):
        #Only UTF-8 is supported due to WC3 limitations
        ans = w.encode('UTF-8')
        self.i += len(ans)
        self.b.write(ans)
        
    def writeString(self, w):
        #Same as writeChars, but adds null terminator
        ans = w.encode('UTF-8')+b'\x00'
        self.i += len(ans)
        self.b.write(ans)