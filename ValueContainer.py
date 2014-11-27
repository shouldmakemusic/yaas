from __future__ import with_statement
import os

class ValueContainer():
    __module__ = __name__
    __doc__ = 'Contains variables that will be loaded at startup'
    
    def __init__(self, parent):
        self._parent = parent
        self.loadValues()
        
    def set_value(self, key, value):
        
        if isinstance(value, list):
            self._values[key] = value
        else:
            self._values[key] = [value]
        self.storeValues()
        
    def get_value(self, key):
        if self.has_value(key):
            return self._values[key]
        
    def get_single_value(self, key):
        
        value = self.get_value(key)[0]
        if isinstance(value, str):
            return float(value)
        return value
        
    def has_value(self, key):
        return self._values.has_key(key)
        
    def values(self):
        return self._values
    
    '''
    #!/usr/local/bin/python

# Python: Retrieve filename of currently-open Ableton Live set
# based on inspecting Live's last Log.txt.

import re
import os
import glob

# Use Log.txt corresponding to latest Live version. eg:
# ~/Library/Preferences/Ableton/Live\ 9.0.6/Log.txt 

root = os.path.expanduser("~/Library/Preferences/Ableton")
logfiles = glob.glob("%s/Live */Log.txt" % root)
regexp = "file://.*\.als$"

if logfiles:
    logfile = list(sorted(logfiles))[-1]
    # print "(using logfile %s)" % logfile
    contents = file(logfile).readlines()
    projects = filter(lambda line: re.search(regexp, line), contents)
    project = projects[-1].strip()
    project = os.path.basename(project)
    print project

'''
        
    def loadValues(self):
        self._values = {}
        if os.path.isfile(__file__ + '_data.pkl'):
            with open(__file__ + '_data.pkl', 'r') as f:
                for line in f:
                    line = line[:-2]
                    keyvalue = line.split("=")
                    key = keyvalue[0]
                    valuearray = keyvalue[1]
                    values = valuearray.split(';')
                    self._values[key] = values    
    
    def storeValues(self):
        storage_file = open(__file__ + '_data.pkl', 'wb')
        for key in self._values.keys():
            value = ''
            if isinstance(self._values[key], list):
                for index in range(len(self._values[key])):
                    value += str(self._values[key][index]) + ';'
            else:
                value = self._values[key]
            storage_file.write(key + '=' + str(value) + "\n")
        storage_file.close()