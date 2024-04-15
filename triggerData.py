# -*- coding: utf-8 -*-
"""
Created on Sat Apr 13 03:11:08 2024

@author: maxer
"""

import subprocess, shutil, os

from mapData import war3Map
from lmlParser import lmlParser, lmlEntry

class triggerCategory:
    
    def __init__(self, path):
        """
        Initializes a trigger category.
        This object is supposed to represent a self-contained group of triggers.

        Parameters
        ----------
        path : string
            Path to the trigger category folder inside the content pack.

        Returns
        -------
        None.

        """
        self.path = path
        self.name = path.split('\\')[-1]
        
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
        
        categoryCatalog = parser.read(self.path+'\\catalog.lml')
        
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
        
        

class triggerData:
    
    def __init__(self, packPath):
        """
        Initializes a trigger data object.
        This object represents a content pack's trigger data.
        It consists of:
            1. A custom script
            2. A variable list
            3. One or several trigger categories
            
        Parameters
        ----------
        packPath : string
            Path to the content pack that the trigger data is in.

        Returns
        -------
        None.

        """
        self.packPath = packPath
        self.customScript = packPath+'\\triggerData\\code.j'
        self.categories = []
        for folder in os.scandir(packPath+'\\triggerData\\'):
            if folder.is_dir():
                self.categories.append(triggerCategory(packPath+'\\triggerData\\'+folder.name)) 
                
    def updateVariables(self, w3map):
        """
        Adds the variables from the content pack
        into the map's variable list.
        
        TODO: the whole function (needs lml parser)

        Parameters
        ----------
        w3map : war3Map
            Map to add the variables into.

        Returns
        -------
        None.

        """
        variables = self.packPath+"\\variable.lml"
        
            
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
        
        if "customscript" in dataTypes:
            shutil.copy(self.customScript, w3map.lnipath+"\\trigger\\code.j")
        
        if "trigger" in dataTypes:
            triggerCategories = []
            for obj in os.scandir(self.packPath+"\\triggerData\\"):
                if obj.is_dir():
                    triggerCategories.append(triggerCategory(self.packPath+"\\triggerData\\"+obj.name))
                    
            for category in triggerCategories:
                category.apply(w3map)
        
        if "vars" in dataTypes:
           self.updateVariables(w3map)