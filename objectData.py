# -*- coding: utf-8 -*-
"""
Created on Sat Apr 13 03:00:22 2024

@author: maxer
"""

import configparser, os

from mapData import war3Map
from sharedObjects import addIdentations, objectData
    
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
        
        sourcePath = self.path+"\\"+dataType+".ini"
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