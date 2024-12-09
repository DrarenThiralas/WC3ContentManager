# -*- coding: utf-8 -*-
"""
Created on Mon Dec  9 13:25:18 2024

@author: Common
"""

from extra.expandedConfig import expandedConfig
from sharedObjects import addIdentations

class objectConstants:
    metaDataFiles = ['UnitMetaData.ini',
                     'MiscMetaData.ini',
                     'AbilityMetaData.ini',
                     'UpgradeMetaData.ini',
                     'DestructableMetaData.ini',
                     'DoodadMetaData.ini']
    stringDataFiles = ['UI\\WorldEditStrings.txt']
    selectionTypes = ['category', 'object', 'field']

    objectMetaDataMapping = {'item': (0,
                                      lambda section: (('useitem' in section)
                                                       and (int(section['useitem'])==1))),
                             'unit': (0,
                                      lambda section: ((int(section['useunit'])==1)
                                                           or (int(section['usehero'])==1)
                                                           or (int(section['usebuilding'])==1))),
                             'misc': (1,
                                      lambda section: (section['section'][1:-1] == 'Misc')),
                             'ability': (2,
                                         lambda section: True),
                             'upgrade': (3,
                                         lambda section: True),
                             'destructable': (4,
                                              lambda section: True),
                             'doodad': (5,
                                        lambda section: True)}

class metaData:

    def __init__(self):

        self.configs = {}
        self.strconfs = {}
        self.cache = {}
        self.strcache = {}

    def loadMetaData(self):
        for file in objectConstants.metaDataFiles:
            self.configs[file] = expandedConfig()
            try:
                self.configs[file].read('Data\\'+file)
            except:
                addIdentations('Data\\'+file)
                self.configs[file].read('Data\\'+file)

    def loadStringData(self):
        for file in objectConstants.stringDataFiles:
            self.strconfs[file] = expandedConfig()
            try:
                self.strconfs[file].read('Data\\'+file)
            except:
                addIdentations('Data\\'+file)
                self.strconfs[file].read('Data\\'+file)

    def get(self, field):

        f = None
        file = None

        name = field.text(0)
        fieldObject = field.parent()
        fieldObjectType = fieldObject.parent()
        fieldObjectTypeName = fieldObjectType.text(0)

        if fieldObjectTypeName in objectConstants.objectMetaDataMapping:
            mapping = objectConstants.objectMetaDataMapping[fieldObjectTypeName]
            file = objectConstants.metaDataFiles[mapping[0]]
            f = mapping[1]

        ans = self.cache[name] if f != None and name in self.cache else self.find(file, name, f)
        self.cache.update([[name, ans]])
        return ans

    def applyStringLocal(self, name):
        if name in self.strcache:
            return self.strcache[name]
        else:
            for key in self.strconfs:
                strconf = self.strconfs[key]
                if strconf.has_section('WorldEditStrings'):
                    for option in strconf.options('WorldEditStrings'):
                        if option.lower() == name.lower():
                            ans = strconf['WorldEditStrings'][option]
                            self.strcache.update([[name, ans]])
                            return ans
        return ''


    def find(self, file, name, validator = None):
        if file != None:
            #print('running find metadata for '+name)
            for section in self.configs[file].sections():
                #print('section '+section)
                fieldName = self.configs[file][section]['field'][1:-1]
                #print('getting data for '+fieldName+', section '+section)
                if fieldName.lower() == name.lower() and validator != None and validator(self.configs[file][section]):
                    return self.configs[file][section]
        return None
