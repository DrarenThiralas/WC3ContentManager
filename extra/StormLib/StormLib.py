# -*- coding: utf-8 -*-
"""
Created on Sat Jul 12 19:49:31 2025

@author: Common
"""

import ctypes, os
from extra.sharedObjects import constants
from extra.war3MapParsers.imports import imports

class mpq:

    def __init__(self, path):
        self.path = path
        self.handle = ctypes.wintypes.HANDLE(None)

    def op(self):
        d0 = ctypes.wintypes.DWORD(0)
        cpath = ctypes.c_wchar_p(self.path)
        return stormLib.lib.SFileOpenArchive(cpath, d0, d0, ctypes.byref(self.handle))

    def cl(self):
        stormLib.lib.SFileCloseArchive(self.handle)

    def ex(self, file, target):
        print("extracting "+file+" as "+target)
        d0 = ctypes.wintypes.DWORD(0)
        cfile = ctypes.c_char_p(file.encode(encoding="ASCII"))
        ctarget = ctypes.c_wchar_p(target)
        stormLib.lib.SFileExtractFile(self.handle, cfile, ctarget, d0)
        return os.path.exists(target)
    
class w3x(mpq):
    def __init__(self, path):
        mpq.__init__(self, path)
    def op(self):
        mpq.op(self)
    def cl(self):
        mpq.cl(self)
    def ex(self, file, target):
        mpq.ex(self, file, target)
        
    def ex_all(self, folder):
        if not os.path.exists(folder):
            os.mkdir(folder)
        # Extract map components
        for f in constants.mapParts:
            self.ex(f, folder+'\\'+f)
        # Get import list from map
        imp = folder+'\\'+constants.mapImports
        if os.path.exists(imp):
            files = imports(imp).getData()
            # Extract imported files
            for f in files:
                self.ex(f, folder+'\\'+f)

        

class stormLib:

    libpath = ".\\extra\\StormLib\\StormLib"
    lib = ctypes.CDLL(libpath)
