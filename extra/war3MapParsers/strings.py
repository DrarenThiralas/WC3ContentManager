# -*- coding: utf-8 -*-
"""
Created on Sun Jul 27 13:19:25 2025

@author: alivemary
"""

class strings:
    
    def __init__(self):
        self.size = 0
        self.data = None
        
    def read(self, path):
        self.path = path
        with open(self.path, 'r') as file:
            self.file = file.read()
            file.close()
        return self
    
    def write(self, path, data=None):
        if data != None:
            self.data = data
        with open(path, 'w') as file:
            
            for i in len(self.data):
                file.write("STRING "+str(i+1)+"\n{\n"+self.data[i]+"\n}\n\n")
            
            file.close()
            
        return self
        
    def parse(self):
        self.data = [s[:s.find('}')] for s in self.file.split('{')]
        self.data = [s[1:-1] for s in self.data]
        self.data = self.data[1:]
        self.size = len(self.data)
        
    def getData(self):
        if self.data == None:
            self.parse()
        return self.data