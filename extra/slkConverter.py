# -*- coding: utf-8 -*-
"""
Created on Sat Dec  7 16:36:38 2024

@author: Common
"""

from extra.expandedConfig import expandedConfig

class slkConstants:

    unitSlks = ['UnitData', 'UnitBalance', 'UnitUI', 'UnitWeapons', 'UnitAbilities']
    itemSlks = ['ItemData']
    allSlks = unitSlks + itemSlks

class slkReader:

    def __init__(self, file):
        self.file = file

    def lines(self):
        return [slkLine(line) for line in self.file.readlines()]

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

    def toConfig(self, sectionColumn = 0):

        config = expandedConfig()

        matrix = self.getMatrix()
        columns = len(matrix[0])
        header = [entry[1:-1] for entry in matrix[0]]
        matrix = matrix[1:]
        for line in matrix:
            sortedLine = [line[sectionColumn]]+line[:sectionColumn]+line[sectionColumn+1:]
            for i in range(columns):
                if i == 0:
                    config.add_section(sortedLine[i][1:-1])
                else:
                    if len(line)>i:
                        value = sortedLine[i]
                    else:
                        value = ""
                    config.set(sortedLine[0][1:-1], header[i], value)

        return config

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



def getSlkList(config):
    slklist = [config[section]['slk'] for section in config.sections() if config.has_option(section, 'slk')]
    return set(slklist)
