# -*- coding: utf-8 -*-
"""
Created on Sat Jul 12 19:49:31 2025

@author: Common
"""

import ctypes, ctypes.wintypes, os
from extra.common import constants
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
    
    def cr(self, size):
        print("creating archive file "+self.path)
        cpath = ctypes.c_wchar_p(self.path)
        d0 = ctypes.wintypes.DWORD(size)
        dflags = ctypes.wintypes.DWORD(0x00100000 + 0x00200000)
        stormLib.lib.SFileCreateArchive(cpath, dflags, d0, ctypes.byref(self.handle))
        
    def ad(self, file, target):
        print("adding "+file+" as "+target)
        d0 = ctypes.wintypes.DWORD(0x80000200)
        d2 = ctypes.wintypes.DWORD(0x02)
        df = ctypes.wintypes.DWORD(0xFFFFFFFF)
        cfile = ctypes.c_wchar_p(file)
        ctarget = ctypes.c_char_p(target.encode(encoding="ASCII"))
        stormLib.lib.SFileAddFileEx(self.handle, cfile, ctarget, d0, d2, df)
        #centries = (ctypes.c_char_p*1)(*[ctarget])
        #stormLib.lib.SFileAddListFileEntries(self.handle, centries, ctypes.wintypes.DWORD(1))
        
    
class w3x(mpq):
    def __init__(self, path):
        mpq.__init__(self, path)
    def op(self):
        mpq.op(self)
    def cl(self):
        mpq.cl(self)
    def ex(self, file, path):
        # Ensure that target folder exists
        if not os.path.exists(path+"\\"+file[:-len(file.split("\\")[-1])]):
            os.makedirs(path+"\\"+file[:-len(file.split("\\")[-1])])
        mpq.ex(self, file, path+"\\"+file)
        
    def cr(self, size):
        mpq.cr(self, size)
        
    def ad(self, file, path):
        mpq.ad(self, file, path)
        
    def ex_all(self, folder):
        # Extract map components
        for f in constants.mapParts:
            self.ex(f, folder)
        # Get import list from map
        imp = folder+'\\'+constants.mapImports
        if os.path.exists(imp):
            files = imports(imp).getData()
            # Extract imported files
            for f in files:
                self.ex(f, folder)
                
    def ad_all(self, folder):
        for subdir, dirs, files in os.walk(folder):
            for f in files:
                self.ad(subdir+"\\"+f, subdir[len(folder)+1:]+("\\" if subdir!=folder else "")+f)
                
    def pack(self, folder):
        size = 0
        for subdir, dirs, files in os.walk(folder):
            for f in files:
                size += 1
        self.cr(size)
        self.ad_all(folder)
        self.cl()


        

class stormLib:

    libpath = ".\\extra\\StormLib\\StormLib"
    lib = ctypes.CDLL(libpath)
