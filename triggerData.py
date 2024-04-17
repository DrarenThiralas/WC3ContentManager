# -*- coding: utf-8 -*-
"""
Created on Sat Apr 13 03:11:08 2024

@author: maxer
"""

import subprocess, shutil, os

from mapData import war3Map
from lmlParser import lmlParser, lmlEntry
from sharedObjects import triggerCategory, triggerData


class triggerPackCategory(triggerCategory):
    
    def __init__(self, path):
        
        triggerCategory.__init__(self, path)
        self.catalog = self.path+'\\catalog.lml'
    
    def findIndex(self, w3map):
        """
        Finds the index of itself when applied to the given map.
        This is needed in order to add triggers to map that already have triggers.

        Parameters
        ----------
        w3map : war3Map
            Map relative to which the index is calculated.

        Returns
        -------
        integer
            Index.

        """
        existingCategories = []
        for obj in os.scandir(w3map.lnipath+"\\trigger\\"):
            if obj.is_dir():
                existingCategories.append(obj.name)
    
        def categoryKey(cat):
            return int(cat.split('-')[0])
        
        existingCategories.sort(key = categoryKey)
        existingCategoryNames = list(map(lambda x: x[len(x.split('-')):], existingCategories))
        
        index = 1
        
        if self.name in existingCategoryNames:
            index = existingCategories[existingCategoryNames.index(self.name)]
            index = categoryKey(index)
        else:
            parser = lmlParser()
            mapCatalogPath = w3map.lnipath+"\\trigger\\catalog.lml"
            mapCatalog = parser.read(mapCatalogPath)
            index = len(mapCatalog.children)+1
                    
        return index
    
    def updateCatalog(self, w3map):
        """
        Updates the given map's trigger catalog.
        Either adds the category to the catalog, or 
        updates the existing catalog entry if one exists.

        Parameters
        ----------
        w3map : war3Map
            Map to update the catalog in.

        Returns
        -------
        None.

        """
        mapCatalogPath = w3map.lnipath+"\\trigger\\catalog.lml"
        parser = lmlParser()
        mapCatalog = parser.read(mapCatalogPath)
        
        categoryCatalog = parser.read(self.catalog)
        
        index = self.findIndex(w3map)
        
        indexStr = '\''+str(index).zfill(2)+'-'
        categoryCatalog.children[0].name = indexStr+categoryCatalog.children[0].name[1:]
        
        if index > len(mapCatalog.children):
            mapCatalog.children.append(categoryCatalog.children[0])
        else:
            mapCatalog.children[index-1] = categoryCatalog.children[0]
            
        parser.write(mapCatalog, mapCatalogPath)
        
    
    def apply(self, w3map):
        """
        Applies the trigger category to the given map.

        Parameters
        ----------
        w3map : war3Map
            Map to apply the category to.

        Returns
        -------
        None.

        """
            
        index = str(self.findIndex(w3map)).zfill(2)
        
        shutil.copytree(self.path, w3map.lnipath+"\\trigger\\"+index+"-"+self.name, dirs_exist_ok = True)
        os.remove(w3map.lnipath+"\\trigger\\"+index+"-"+self.name+"\\catalog.lml")
        
        self.updateCatalog(w3map)

class triggerPack(triggerData):
    
    def __init__(self, path):
        triggerData.__init__(self, path)
        self.categories = [triggerPackCategory(cat.path) for cat in self.categories]
                
    def updateVariables(self, w3map, clearUnused = True):
        """
        Adds the variables from the content pack
        into the map's variable list.

        Parameters
        ----------
        w3map : war3Map
            Map to add the variables into.

        Returns
        -------
        None.

        """
        
        variableTargetPath = w3map.lnipath+"\\trigger\\variable.lml"
        
        if os.path.exists(variableTargetPath):
            
            parser = lmlParser()
            
            variableSource = parser.read(self.varFile)
            variableTarget = parser.read(variableTargetPath)
            
            for entry in variableSource.children:
                targetNames = list(map(lambda x: x.name, variableTarget.children))
                if entry.name in targetNames:
                    variableTarget.children[targetNames.index(entry.name)] = entry
                else:
                    variableTarget.children.append(entry)
                    
            parser.write(variableTarget, variableTargetPath)
            
        else:
            
            shutil.copy(self.varFile, variableTargetPath)
                
        
            
    def apply(self, w3map, dataTypes):
        """
        Applies the trigger data to the given map.

        Parameters
        ----------
        w3map : war3Map
            Map to apply the trigger data to.
        dataTypes: list of string
            List of types of trigger data to apply.

        Returns
        -------
        None.

        """

        
        if "customscript" in dataTypes and os.path.exists(self.customScript):
            shutil.copy(self.customScript, w3map.lnipath+"\\trigger\\code.j")
        
        if "trigger" in dataTypes:
            for category in self.categories:
                category.apply(w3map)
        
        if "vars" in dataTypes and os.path.exists(self.varFile):
           self.updateVariables(w3map)