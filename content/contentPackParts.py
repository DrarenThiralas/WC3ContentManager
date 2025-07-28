# -*- coding: utf-8 -*-
"""
Created on Thu Apr 18 06:19:35 2024

@author: maxer
"""

import os, shutil
from extra.expandedConfig import expandedConfig
from extra.lmlParser import lmlParser
from extra.sharedObjects import resourceData, triggerCategory, triggerData, objectData

class resourcePack(resourceData):

    def updateIni(self, w3map):
        """
        Updates the imp.ini file that list all the imported resources for the map.

        Parameters
        ----------
        w3map : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        """

        imppath = w3map.lnipath+"\\table\\imp.ini"

        if os.path.exists(imppath):

            file = open(self.path+"\\imp.ini", "r")
            resourceLines = file.readlines()[1:-1]
            file.close()

            file = open(imppath, "r")
            impini = file.readlines()
            file.close()

            newLines = []

            for line in resourceLines:
                if not line in impini:
                    newLines.append(line)

            impini = impini[:-1]+newLines+impini[-1:]

            file = open(imppath, "w")
            file.writelines(impini)
            file.close()

        else:

            shutil.copy(self.path+"\\imp.ini", imppath)

    def apply(self, w3map):
        """
        Applies the resource data to the given map.

        Parameters
        ----------
        w3map : war3Map object
            The map to apply resource data to.

        Returns
        -------
        None.

        """

        shutil.copytree(self.path+'\\resource', w3map.lnipath+"\\resource", dirs_exist_ok = True)
        self.updateIni(w3map)

class objectPack(objectData):

    def apply(self, w3map, dataTypes):
        """
        Applies the given types from the object data to the given map.

        Parameters
        ----------
        w3map : war3Map object
            The map to apply object data to.
        dataTypes : list of string
            List of data types to apply.

        Returns
        -------
        None.

        """
        for dataType in dataTypes:
            try:
                self.applyType(w3map, dataType)
            except:
                pack = self.path.split('\\')[-1]
                print('Failed to apply object data of type '+dataType+' to '+w3map.lnipath+' from '+pack+'. Data may not exist in pack.')

    def applyType(self, w3map, dataType):
        """
        Applies the given type from the object data to the given map.

        Parameters
        ----------
        w3map : war3Map object
            The map to apply object data to.
        dataType : string
            Data type to apply.

        Returns
        -------
        None.

        """

        sourceConfig = self.getConfig(dataType)

        targetConfig = expandedConfig()
        targetPath = w3map.lnipath+"\\table\\"+dataType+".ini"
        targetConfig.read(targetPath)

        sourceSections = sourceConfig.sections()

        for obj in sourceSections:
            targetConfig[obj] = sourceConfig[obj]

        with open(targetPath, 'w') as configfile:
            targetConfig.write(configfile)
            configfile.close()

class triggerPackCategory(triggerCategory):

    def __init__(self, path):

        triggerCategory.__init__(self, path)
        self.catalog = self.path+'\\catalog.lml'

    def findIndex(self, w3map):
        """
        Finds the index of itself when applied to the given map.
        This is needed in order to add triggers to maps that already have triggers.

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
