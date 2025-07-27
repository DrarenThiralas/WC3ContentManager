# -*- coding: utf-8 -*-
"""
Created on Sat Jul 12 19:49:31 2025

@author: Common
"""

import ctypes

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
        d0 = ctypes.wintypes.DWORD(0)
        cfile = ctypes.c_char_p(file.encode(encoding="ASCII"))
        ctarget = ctypes.c_wchar_p(target)
        stormLib.lib.SFileExtractFile(self.handle, cfile, ctarget, d0)

class stormLib:

    libpath = ".\\StormLib"
    lib = ctypes.CDLL(libpath)


test = mpq(".\\test.w3x")
test.op()
test.ex("war3map.j", ".\\war3map.j")
test.cl()
