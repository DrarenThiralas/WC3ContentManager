# -*- coding: utf-8 -*-
"""
Created on Sat Dec  7 16:36:38 2024

@author: Common
"""

from sharedObjects import objectData
import csv, configparser

class slkReader:

    def __init__(self, file):
        self.file = file

    def lines(self):
        return [slkLine(line) for line in file.readlines()]

    def getMatrix(self):
        matrix = []
        currentLine = -1
        for line in self.lines():

            if line.getType()=="C":

                if line.getHasEntry("Y"):
                    matrix.append([])
                    currentLine += 1
                    lastX = 0

                if line.getHasEntry("X"):
                    x = int(line.getEntryValue("X"))
                    diff = x-lastX
                    while diff>1:
                        diff-=1
                        matrix[currentLine].append("")
                    lastX = x

                if line.getHasEntry("K"):
                    matrix[currentLine].append(line.getEntryValue("K"))

        return matrix

    def toObjectData(self, path, dataType):

        objData = objectData(path)
        objData.clear()

        config = configparser.ConfigParser(comment_prefixes=('--'), strict=False, interpolation=None)

        matrix = self.getMatrix()
        print(matrix)
        columns = len(matrix[0])
        header = [entry[1:-1] for entry in matrix[0]]
        matrix = matrix[1:]
        for line in matrix:
            for i in range(columns):
                if i == 0:
                    config.add_section(line[i][1:-1])
                else:
                    config.set(line[0][1:-1], header[i], line[i])

        objData.setConfig(dataType, config)







class slkLine:

    def __init__(self, line):
        self.line = line
        self.entries = line.split(";")

    def getType(self):
        return self.entries[0]

    def isTypeC(self):
        return self.getType()=="C"

    def getHasEntry(self, entryType):
        xEntry = ""
        for entry in self.entries:
            if entry[0]==entryType:
                xEntry = entry
        return len(xEntry)>0

    def getEntryValue(self, entryType):
        xEntry = ""
        for entry in self.entries:
            if entry[0]==entryType:
                xEntry = entry
        if entryType=="K":
            return xEntry[1:-2]
        else:
            return xEntry[1:]




with open("UnitBalance.slk", newline='') as file:
    reader = slkReader(file)
    reader.toObjectData("Data\\BaseObjectDataTest", "unit")
