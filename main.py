# -*- coding: utf-8 -*-
"""
Created on Fri Apr 12 18:12:14 2024

@author: maxer
"""

import sys
from PyQt6.QtWidgets import QApplication
from mainWindow import mainWindow  

app = QApplication([])

mainWin = mainWindow()

mainWin.run()

sys.exit(app.exec())