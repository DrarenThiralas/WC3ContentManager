# -*- coding: utf-8 -*-
"""
Created on Fri Apr 12 18:12:14 2024

@author: maxer
"""

import sys
#from PyQt6.QtWidgets import QApplication
#from mainWindow.mainWindowMain import mainWindow
from extra.StormLib.StormLib import w3x
from extra.war3MapParsers.strings import strings
from extra.war3MapParsers.customdata import customdata

test = w3x(".\\test2.w3x")
test.op()
test.ex_all('.\\test2_w3x')
test.cl()

test2 = strings('.\\test2_w3x\\war3map.wts')
print(test2.getData())

test3 = customdata('.\\test2_w3x\\war3map.w3u', 'unit')
for obj in test3.getData():
    obj.toLni('.\\test2_lni\\'+obj.id+'.txt')

#app = QApplication([])
#mainWin = mainWindow()
#mainWin.run()
#sys.exit(app.exec())
