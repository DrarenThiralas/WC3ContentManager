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
