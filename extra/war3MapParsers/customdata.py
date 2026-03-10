# -*- coding: utf-8 -*-
"""
Created on Sun Jul 27 13:17:42 2025

@author: alivemary
"""

from extra.war3MapParsers.bytesreader import bytesreader
from extra.war3MapParsers.byteswriter import byteswriter
from extra.common import constants
from content.war3Types.war3Object import war3Object, war3ObjectField, typeHasExtraFields

class customdata:
    
    def __init__(self, tp):
        self.type = tp
        self.b = None
        self.size = 0
        self.data = None
        
    def read(self, path):
        self.path = path
        f = constants.getObjTypeFile(self.type)
        with open(self.path+'\\'+f, 'rb') as file:
            self.b = file.read()
            file.close()
        return self
        
    def parse(self):
        reader = bytesreader(self.b)
        #print("parsing custom "+self.type+" data")
        version = reader.readInt()
        #print("format version: "+str(version))
        self.data = []
        
        def parsefield(obj):
            code = reader.readChars(4)
            #print("parsing field "+code)
            tp = reader.readInt()
            #print("type: "+str(tp))
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
            #print("value is "+str(value))
            signature = reader.readInt()
            field = war3ObjectField(code, tp, value, level, pointer)
            obj.syncField(field)
            
        def parseobject(isBase):
            proto = reader.readChars(4)
            code = reader.readChars(4)
            #print("edited object: "+proto+":"+code)
            size = reader.readInt()
            #print("fields: "+str(size))
            obj = war3Object(self.type, proto) if isBase else war3Object(self.type, proto, code)
            for j in range(size):
               parsefield(obj)
            return obj
        
        size0 = reader.readInt()
        #print("edits to base objects: "+str(size0))
        self.data = self.data + [parseobject(True) for i in range(size0)]
        size1 = reader.readInt()
        #print("custom objects: "+str(size1))
        self.data = self.data + [parseobject(False) for i in range(size1)]
        
        return self
            
    def getData(self):
        if self.data == None:
            self.parse()
        return self.data
    
    def setData(self, data):
        self.data = data
        return self

    def write(self, path, data = None):
        
        if data != None:
            self.setData(data)
            
        self.path = path
        f = constants.getObjTypeFile(self.type)
        with open(self.path+'\\'+f, 'wb') as file:
            writer = byteswriter(file)
            
            #Write version
            writer.writeInt(2)
            
            def writetable(objs, isOrig = False):
                #Table size
                writer.writeInt(len(objs))
                for obj in objs:
                    objEntries = obj.getTableOrder()
                    #Write object ID
                    writer.writeChars(objEntries[0])
                    if isOrig:
                        writer.writeInt(0)
                    else:
                        writer.writeChars(objEntries[1])
                    #Write field count
                    writer.writeInt(objEntries[2])
                    #Write fields
                    for f in objEntries[3:]:
                        #Field ID
                        writer.writeChars(f[0])
                        #Field type
                        writer.writeInt(f[1])                    
                        #Level and pointer
                        i = 2
                        if len(f) > 4:
                            writer.writeInt(f[2])
                            writer.writeInt(f[3])
                            i = 4
                        #Field value
                        if f[1] == 0:
                            writer.writeInt(f[i])
                        elif f[1] == 3:
                            writer.writeString(f[i])
                        else:
                            writer.writeFloat(f[i])
                        #Field end
                        writer.writeChars(f[i+1])
                        
            #Write original object table
            orig = [obj for obj in self.data if obj.isOriginal()]
            writetable(orig, True)
            #Write custom object table
            custom = [obj for obj in self.data if not obj.isOriginal()]
            writetable(custom)
            
            file.close()
        
        return self
    
    
    
    
    
    
    
    
    