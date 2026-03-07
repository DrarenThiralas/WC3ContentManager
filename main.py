# -*- coding: utf-8 -*-
"""
Created on Fri Apr 12 18:12:14 2024

@author: maxer
"""

import sys, os
#from PyQt6.QtWidgets import QApplication
#from mainWindow.mainWindowMain import mainWindow
from extra.StormLib.StormLib import w3x
from extra.war3MapParsers.strings import strings
from extra.war3MapParsers.customdata import customdata
from content.war3Types.war3Object import ymlToObject

test = w3x(".\\test2.w3x")
test.op()
test.ex_all('.\\test2_w3x')
test.cl()

test2 = strings('.\\test2_w3x\\war3map.wts')
print(test2.getData())

test3 = customdata('.\\test2_w3x\\war3map.w3u', 'unit')

for obj in test3.getData():
    obj.toYml('.\\test2_yml\\unit')
    
#test4 = w3x(".\\test2_new.w3x")
#test4.pack(".\\test2_w3x")

test5 = customdata('.\\test2_w3x\\war3map.w3t', 'item')

for obj in test5.getData():
    obj.toYml('.\\test2_yml\\item')

#app = QApplication([])
#mainWin = mainWindow()
#mainWin.run()
#sys.exit(app.exec())
