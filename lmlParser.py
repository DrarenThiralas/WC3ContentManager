# -*- coding: utf-8 -*-
"""
Created on Sat Apr 13 17:56:26 2024

@author: maxer
"""


class lmlLine:
    
    def __init__(self, line):
        """
        Initializes and .lml line object.
        The object is just a string with data about indentation attached.

        Parameters
        ----------
        line : string
            Line from the .lml file.

        Returns
        -------
        None.

        """
        self.indent = self.getIndent(line)//4
        self.name = line[self.indent*4:]
        if self.name[-1] == '\n':
            self.name = self.name[:-1]
        
    def getIndent(self, line):
        indent = 0
        ch = line[0]
        while ch == ' ':
            indent += 1
            ch = line[indent]
            
        self.indent = indent
        return self.indent

class lmlEntry:
    
    def __init__(self, name, children = []):
        """
        Initializes an lmlEntry object.
        This object is an entry in an .lml file that can also contain additional
        lmlEntry objects as children.

        Parameters
        ----------
        name : string
            The .lml entry itself.
        children : list of lmlEntry, optional
            A list containing the entry's children. The default is [].

        Returns
        -------
        None.

        """
        self.name = name
        self.children = children
        
    def toString(self, indent = 0):
        """
        A function that recursively converts an lmlEntry and its children into a string.

        Parameters
        ----------
        indent : integer, optional
            Indentation of the entry, used for recursion. The default is 0.

        Returns
        -------
        string
            lmlEntry's string form.

        """
        string = self.name
        for i in range(indent):
            string = '    '+string
        for child in self.children:
            string += child.toString(indent+1)
        return '\n'+string
        
    def __str__(self):
        return self.toString()

class lmlParser:
    
    def __init__(self):
        """
        Initilizes an .lml parser.
        .lml files include triggers, trigger catalogs, and variable lists.

        Parameters
        ----------
        None.

        Returns
        -------
        None.

        """
        

    def read(self, path):
        """
        Reads the specified .lml file.

        Parameters
        ----------
        path : string
            Path to the .lml file.

        Returns
        -------
        lmlContent : lmlEntry
            An lmlEntry object with the name "root".
            Has all the top-level entries in the .lml file as children.

        """
        
        lmlContent = lmlEntry("root")
        
        file = open(path, 'r')
        lines = file.readlines()
        file.close()

        lmlLines = list(map(lambda x: lmlLine(x), lines))
        lmlLineNames = list(map(lambda x: x.name, lmlLines))
        
        depth = max(list(map(lambda x: x.indent, lmlLines)))+1
        newParents = [lmlContent]
        
        for i in range(depth):
            parents = newParents
            newParents = []
            for j in range(len(parents)):
                entries = []
                if i != 0:
                    sliceStart = lmlLineNames.index(parents[j].name)
                else:
                    sliceStart = 0 
                if j == len(parents)-1:
                    potentialEntries = lmlLines[sliceStart:]
                else:
                    sliceEnd = lmlLineNames.index(parents[j+1].name)
                    potentialEntries = lmlLines[sliceStart:sliceEnd]
                
                for entry in potentialEntries:
                    if entry.indent == i:
                        newEntry = lmlEntry(entry.name)
                        entries.append(newEntry)
                        newParents.append(newEntry)
                parents[j].children = entries
                
        return lmlContent
            
            
            
    def write(self, lmlContent, path):
        """
        Writes the given lmlEntry object into a file.

        Parameters
        ----------
        lmlContent : lmlEntry
            An lmlEntry to be written into the file.
        path : string
            Path to the .lml file.

        Returns
        -------
        None.

        """
        
        file = open(path, 'w')
        entries = lmlContent.children
        for entry in entries:
            file.write(str(entry))
        file.write('\n')
        file.close()
        
        
        
        
            
            
                