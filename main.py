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
from content.war3Data.war3ObjectData import objectDataType

test = w3x(".\\test2.w3x")
test.op()
test.ex_all('.\\test2_w3x')
test.cl()

test2 = strings().read('.\\test2_w3x\\war3map.wts')
print(test2.getData())

test3 = customdata('unit').read('.\\test2_w3x')

for obj in test3.getData():
    obj.write('.\\test2_yml\\unit')
    
#test4 = w3x(".\\test2_new.w3x")
#test4.pack(".\\test2_w3x")

test5 = objectDataType('item').read('.\\test2_w3x', False)
test5.write('.\\test2_yml')

test5a = objectDataType('item').read('.\\test2_yml')
for obj in test5a.data.values():
    print(str(obj))
    print(str(obj.fields))
test5a.write('.\\test2_yml', False)

test5b = objectDataType('item').read('.\\test2_yml', False)

print("Comparing object data before and after:")
print("Objects before: "+str(len(test5.data)))
print("List: "+str([str(obj) for obj in test5.data.values()]))
print("Objects after: "+str(len(test5b.data.values())))
print("List: "+str([str(obj) for obj in test5b.data.values()]))
mask = [int(obj in test5b) for obj in test5.data.values()]
print("Preserved objects: "+str(sum(mask))+" out of "+str(len(test5.data)))
print("Object preservation mask:")
print(str(mask))

#app = QApplication([])
#mainWin = mainWindow()
#mainWin.run()
#sys.exit(app.exec())
