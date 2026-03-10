# -*- coding: utf-8 -*-
"""
Created on Fri Apr 12 18:12:14 2024

@author: maxer
"""

import sys, os
#from PyQt6.QtWidgets import QApplication
#from mainWindow.mainWindowMain import mainWindow
from extra.StormLib.StormLib import w3x
from content.war3Data.contentData import contentData
from extra.war3MapParsers.imports import imports

test = w3x(".\\test2.w3x")
test.op()
test.ex_all('.\\test2_w3x')
test.cl()

test2 = contentData().read('.\\test2_w3x', False)
test2.write('.\\test3_lni')


#app = QApplication([])
#mainWin = mainWindow()
#mainWin.run()
#sys.exit(app.exec())
