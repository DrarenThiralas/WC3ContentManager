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
        self.proto = proto
        self.id = rawcode if rawcode != "" else proto
        self.type = tp
        self.fields = dict()
        
    def __str__(self):
        return self.proto+":"+self.id
        
    def __contains__(self, field):
        if not field['id'] in self.fields:
            return False
        return (self.fields[field['id']] == field)
        
    def __eq__(self, o):
        vals1 = [self.proto, self.id, self.type]
        vals2 = [o.proto, o.id, o.type]
        conds = [vals1[i] == vals2[i] for i in range(len(vals1))]
        if False in conds:
            return False
        fields1 = [field in self for field in o.fields.values()]
        if False in fields1:
            return False
        fields2 = [field in o for field in self.fields.values()]
        if False in fields2:
            return False
        return True
        
    def __ne__(self, o):
        return not self == o
        
    def isOriginal(self):
        return self.proto == self.id
    
    def __len__(self):
        if self.fields == None:
            return 0
        else:
            return len(self.fields)
    
    def __getitem__(self, key):
        return self.fields[key]
        
    def __setitem__(self, key, field):
        if key != 0:
            self.fields[key]=field
        else:
            self.fields[field['id']]=field
            
    def syncFields(self, fields):
        if type(fields) is dict:
            for key, field in fields.items():
                self[key]=field
        elif type(fields) is list:
            for field in fields:
                self[0]=field
    
    def toLni(self):
        lines = [self.type, self.proto, self.id]
        lines = lines + [str(field) for field in self.fields]
        return lines

    def read(self, path):
        if os.path.exists(path):
            with open(path, 'r') as file:
                d = yaml.safe_load(file)
                self.proto = d['proto']
                self.id = d['id']
                self.type = d['type']
                self.fields = dict()
                self.syncFields(d['fields'])
        else:
            print("error loading object from "+path)
        return self
        
    def write(self, path):
        if not os.path.exists(path):
            os.makedirs(path)
        with open(path+'\\'+self.id+'.yml', 'w') as outfile:
            d = dict()
            d['proto'] = self.proto
            d['id'] = self.id
            d['type'] = self.type
            d['fields'] = list(self.fields.values())
            yaml.dump(d, outfile, default_flow_style=False)
            
    def getTableOrder(self):
        """
        Returns a list of object parts in the right order for writing to a table.
        
        Returns
        -------
        None.

        """
        
        base = [self.proto, self.id, len(self)]
        fields = None
        if typeHasExtraFields(self.type):
            fields = [[f['id'], f['type'], f['level'], f['pointer'], f['value'], self.id] for f in self.fields.values()]
        else:
            fields = [[f['id'], f['type'], f['value'], self.id] for f in self.fields.values()]
        return base+fields

        
        
            

