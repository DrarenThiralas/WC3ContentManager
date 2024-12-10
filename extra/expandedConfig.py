# -*- coding: utf-8 -*-
"""
Created on Sun Dec  8 15:17:06 2024

@author: Common
"""

import configparser

class expandedConfig(configparser.ConfigParser):

    def __init__(self, comment_prefixes=('--', '//')):
        configparser.ConfigParser.__init__(self, comment_prefixes=comment_prefixes, strict = False, interpolation = None)

    def copy(self):
        cfgNew = expandedConfig()
        for section in self:
            if not section == 'DEFAULT':
                if not cfgNew.has_section(section):
                    cfgNew.add_section(section)
                for option in self.options(section):
                    cfgNew.set(section, option, self[section][option])
        return cfgNew

    def merge(self, cfg, overrideSections = False, entryToAdd = None, isCopy = True):

        cfgNew = self.copy() if isCopy else self
        if not cfg == None:
            for section in cfg.sections():
                if not cfgNew.has_section(section):
                    cfgNew.add_section(section)
                if entryToAdd != None:
                    cfgNew.set(section, *entryToAdd)
                for option in cfg.options(section):
                    cfgNew.set(section, option, cfg[section][option])
        return cfgNew
    
    def addIdentations(filePath):
        """
        Adds identations to the multiline values in the target .ini file.
        Otherwise ConfigParser can't read it.


        Parameters
        ----------
        filePath : string
            The path to the .ini file.

        Returns
        -------
        None.

        """

        file = open(filePath, "r")
        lines = file.readlines()

        def isHeader(line):
            return (line[0] == '[' and line[5] == ']')

        def isComment(line):
            return (line[0]=='-' and line[1] == '-')

        if lines[0][0] != " ":
            newlines = []
            for line in lines:
                newline = line
                if newline.find("=") == -1 and isHeader(newline) == False and isComment(newline) == False:
                    newline = " "+newline
                newlines.append(newline)
            file.close()
            file = open(filePath, "w")
            file.writelines(newlines)

        file.close()
        
    def read(self, file):
        try:
            configparser.ConfigParser.read(self, file)
        except:
            self.addIdentations(file)
            configparser.ConfigParser.read(self, file)
