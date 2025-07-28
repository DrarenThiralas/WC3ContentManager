# -*- coding: utf-8 -*-
"""
Created on Sun Jul 27 13:17:42 2025

@author: alivemary
"""

from extra.war3MapParsers.common import bytesreader
from content.war3Types.war3Object import war3Object, war3ObjectField, typeHasExtraFields

class customdata:
    
    def __init__(self, path, tp):
        self.path = path
        self.type = tp
        self.size = 0
        self.data = None
        
    def read(self):
        file = open(self.path, 'rb')
        self.b = file.read()
        file.close()
        
    def parse(self):
        reader = bytesreader(self.b)
        print("parsing custom "+self.type+" data")
        version = reader.readInt()
        print("format version: "+str(version))
        self.data = []
        
        def parsefield(obj):
            code = reader.readChars(4)
            print("parsing field "+code)
            tp = reader.readInt()
            print("type: "+str(tp))
            level = 0
            pointer = 0
            if typeHasExtraFields(self.type):
                level = reader.readInt()
                pointer = reader.readInt()
            value = 0
            if tp == 0:
                value = reader.readInt()
            elif tp == 3:
                value = reader.readStr()
            else:
                value = reader.readFloat()
            print("value is "+str(value))
            signature = reader.readInt()
            field = war3ObjectField(code, tp, value, level, pointer)
            obj.syncField(field)
            
        def parseobject(isBase):
            proto = reader.readChars(4)
            code = reader.readChars(4)
            print("edited object: "+proto+":"+code)
            size = reader.readInt()
            print("fields: "+str(size))
            obj = war3Object(self.type, proto) if isBase else war3Object(self.type, proto, code)
            for j in range(size):
               parsefield(obj)
            return obj
        
        size0 = reader.readInt()
        print("edits to base objects: "+str(size0))
        self.data = self.data + [parseobject(True) for i in range(size0)]
        size1 = reader.readInt()
        print("custom objects: "+str(size1))
        self.data = self.data + [parseobject(False) for i in range(size1)]
            
    def getData(self):
        if self.data == None:
            self.read()
            self.parse()
        return self.data