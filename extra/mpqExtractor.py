# -*- coding: utf-8 -*-
"""
Created on Sun Dec  8 16:49:44 2024

@author: Common
"""

from extra.StormLib.StormLib import mpq
from extra.slkConverter import slkReader
from extra.sharedObjects import constants

class dataConstants:

    metaDataFiles = ['Units\\UnitMetaData.slk',
                     'Units\\AbilityMetaData.slk',
                     'Units\\MiscMetaData.slk',
                     'Units\\UpgradeMetaData.slk',
                     'Units\\UpgradeEffectMetaData.slk',
                     'Units\\DestructableMetaData.slk',
                     'Doodads\\DoodadMetaData.slk']

    stringDataFiles = ['UI\\WorldEditStrings.txt']

class dataMaker:

    def __init__(self, mpqName):
        self.path = constants.getGlobalOption('war3')+'\\'+mpqName
        self.mpq = mpq(self.path)

    def extract(self, file, target = 'Temp'):
        print('extracting '+file)
        self.mpq.ex(file, target+'\\'+file)
        #cwd = os.getcwd()
        #subprocess.run(["cmd", '/c', "MPQEditor.exe", "extract", self.mpq, file, cwd+"\\"+target, '/fp'], cwd = constants.getGlobalOption('mpqedit'))
        #subprocess.run(["cmd", '/c', "MPQEditor.exe", string], cwd = constants.getGlobalOption('mpqedit'))
        return target+"\\"+file

    def process(self, sourcepath, targetpath):
        filepath = self.extract(sourcepath)
        with open(filepath, newline='') as file:
            reader = slkReader(file)
            config = reader.toConfig()
            file.close()
        with open(targetpath, 'w') as targetfile:
            config.write(targetfile)
            targetfile.close()
