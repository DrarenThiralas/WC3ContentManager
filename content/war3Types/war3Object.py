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
        
    def __str__(self):
        return self.d['proto']+":"+self.d['id']
        
    def __contains__(self, field):
        matches = [field == f for f in self.d['fields']]
        return (True in matches)
        
    def __eq__(self, o):
        keys = ['proto', 'id', 'type']
        conds = [self.d[key] == o.d[key] for key in keys]
        if False in conds:
            return False
        fields1 = [field in self.d['fields'] for field in o.d['fields']]
        if False in fields1:
            return False
        fields2 = [field in o.d['fields'] for field in self.d['fields']]
        if False in fields2:
            return False
        return True
        
    def __ne__(self, o):
        return not self == o
        
    def isOriginal(self):
        return self.d['proto'] == self.d['id']
        
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
        
    def read(self, path):
        if os.path.exists(path):
            with open(path, 'r') as file:
                d = yaml.safe_load(file)
                self.d = d
        else:
            print("error loading object from "+path)
        return self
        
    def write(self, path):
        if not os.path.exists(path):
            os.makedirs(path)
        with open(path+'\\'+self.d['id']+'.yml', 'w') as outfile:
            yaml.dump(self.d, outfile, default_flow_style=False)
            
    def getTableOrder(self):
        """
        Returns a list of object parts in the right order for writing to a table.
        
        Returns
        -------
        None.

        """
        
        base = [self.d['proto'], self.d['id'], len(self.d['fields'])]
        fields = None
        if typeHasExtraFields(self.d['type']):
            fields = [[f['id'], f['type'], f['level'], f['pointer'], f['value'], self.d['id']] for f in self.d['fields']]
        else:
            fields = [[f['id'], f['type'], f['value'], self.d['id']] for f in self.d['fields']]
        return base+fields

        
        
            

