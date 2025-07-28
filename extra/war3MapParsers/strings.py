# -*- coding: utf-8 -*-
"""
Created on Sun Jul 27 13:19:25 2025

@author: alivemary
"""

class strings:
    
    def __init__(self, path):
        self.path = path
        self.size = 0
        self.data = None
        
    def read(self):
        file = open(self.path, 'r')
        self.file = file.read()
        file.close()
        
    def parse(self):
        self.data = [s[:s.find('}')] for s in self.file.split('{')]
        self.data = [s[1:-1] for s in self.data]
        self.data = self.data[1:]
        self.size = len(self.data)
        
    def getData(self):
        if self.data == None:
            self.read()
            self.parse()
        return self.data