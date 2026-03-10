# -*- coding: utf-8 -*-
"""
Created on Mon Jul 28 11:21:07 2025

@author: alivemary
"""

import yaml, os
from extra.common import constants

def typeHasExtraFields(tp):
    index = constants.objTypes.index(tp)
    return (index <= 2)

def war3ObjectField(rawcode, flag, value, level = 0, pointer = 0):
        d = dict()
        d['id'] = rawcode
        d['type'] = flag
        # Types:
        # 0 = int
        # 1 = float
        # 2 = float (between 0 and 1)
        # 3 = string
        d['value'] = value
        d['level'] = level
        d['pointer'] = pointer
        return d
    
class war3Object:
    
    def __init__(self, tp = "", proto = "", rawcode = ""):
        self.d = dict()
        self.d['proto'] = proto
        self.d['id'] = rawcode if rawcode != "" else proto
        self.d['type'] = tp
        self.d['fields'] = []
        
    def syncField(self, field):
        fieldNames = [f['id'] for f in self.d['fields']]
        if field['id'] in fieldNames:
            index = fieldNames.index(field['id'])
            self.d['fields'][index] = field
        else:
            self.d['fields'].append(field)
            
            
    def getField(self, code):
        fieldNames = [f['id'] for f in self.d['fields']]
        index = fieldNames.index(code)
        return None if index == -1 else self.d['fields'][index]
    
    def toLni(self, path):
        file = open(path, 'w')
        lines = [self.type, self.proto, self.id]
        lines = lines + [str(field) for field in self.fields]
        lines = [line + '\n' for line in lines]
        file.writelines(lines)
        file.close()
        
    def toYml(self, path):
        if not os.path.exists(path):
            os.makedirs(path)
        with open(path+'\\'+self.d['id']+'.yml', 'w') as outfile:
            yaml.dump(self.d, outfile, default_flow_style=False)
            
    def readYml(self, path):
        if os.path.exists(path):
            with open(path, 'r') as file:
                d = yaml.safe_load(file)
                self.d = d
        else:
            print("error loading object from "+path)
