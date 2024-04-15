# -*- coding: utf-8 -*-
"""
Created on Sat Apr 13 03:00:22 2024

@author: maxer
"""

import configparser, os

from mapData import war3Map

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

class objectData:
    
    def __init__(self, packPath):
        """
        Initializes a new objectData object.
        This object represents object editor data in a content pack.

        Parameters
        ----------
        packPath : string
            Path to the content pack folder.

        Returns
        -------
        None.

        """
        self.packPath = packPath
        
    def getConfig(self, dataType):
        
        sourcePath = self.packPath+"\\"+dataType+".ini"
        if os.path.exists(sourcePath):
            
            sourceConfig = configparser.ConfigParser(comment_prefixes=('--'), strict=False, interpolation=None)
    
            try:
                sourceConfig.read(sourcePath)
            except:
                addIdentations(sourcePath)
                sourceConfig.read(sourcePath)
                
        return sourceConfig
    
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
                pack = self.packPath.split('\\')[-1]
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
        
        sourcePath = self.packPath+"\\"+dataType+".ini"
        if os.path.exists(sourcePath):
            
            sourceConfig = configparser.ConfigParser(comment_prefixes=('--'), strict=False, interpolation=None)
    
            try:
                sourceConfig.read(sourcePath)
            except:
                addIdentations(sourcePath)
                sourceConfig.read(sourcePath)
            
            
            #print(sourceConfig.sections())
            
            targetConfig = configparser.ConfigParser(comment_prefixes=('--'), strict=False, interpolation=None)
            targetPath = w3map.lnipath+"\\table\\"+dataType+".ini"
            try: 
                targetConfig.read(targetPath)
            except:
                addIdentations(targetPath)
                targetConfig.read(targetPath)
            
            
            dataObjectsSource = sourceConfig.sections()
            
            for obj in dataObjectsSource:
                targetConfig[obj] = sourceConfig[obj]
                
            with open(targetPath, 'w') as configfile:
                targetConfig.write(configfile)
                configfile.close()