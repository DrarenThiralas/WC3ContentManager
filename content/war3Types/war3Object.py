# -*- coding: utf-8 -*-
"""
Created on Mon Jul 28 11:21:07 2025

@author: alivemary
"""

war3ObjectTypes = ['dood', 'abil', 'upgd', 'unit', 'item', 'dest','buff']

def typeHasExtraFields(tp):
    index = war3ObjectTypes.index(tp)
    return (index <= 2)

class war3ObjectField:
    def __init__(self, rawcode, flag, value, level = 0, pointer = 0):
        self.id = rawcode
        self.type = flag
        # Types:
        # 0 = int
        # 1 = float
        # 2 = float (between 0 and 1)
        # 3 = string
        self.value = value
        self.level = level
        self.pointer = pointer
    def __str__(self):
        return self.id + ' (' + str(self.level) + ', ' + str(self.pointer) + ") = " + str(self.value)

class war3Object:
    
    def __init__(self, tp, proto, rawcode = ""):
        self.proto = proto
        self.id = rawcode if rawcode != "" else proto
        self.type = tp
        self.fields = []
        
    def syncField(self, field):
        fieldNames = [f.id for f in self.fields]
        if field.id in fieldNames:
            index = fieldNames.index(field.id)
            self.fields[index] = field
        else:
            self.fields.append(field)
            
            
    def getField(self, code):
        fieldNames = [f.id for f in self.fields]
        index = fieldNames.index(code)
        return None if index == -1 else self.fields[index]
    
    def toLni(self, path):
        file = open(path, 'w')
        lines = [self.type, self.proto, self.id]
        lines = lines + [str(field) for field in self.fields]
        lines = [line + '\n' for line in lines]
        file.writelines(lines)
        file.close()