#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar  7 14:10:50 2026

@author: drarenthiralas
"""

import yaml, os
from content.war3Types.war3Object import war3Object

class ymlReader:
    
    def __init__(self, path):
        self.path = path
        
    def getData(self):
        print()
        #TODO: scan folder and read all yml files to object list