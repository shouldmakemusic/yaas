from __future__ import with_statement

import sys
import time
import os

# RemixNet
from ..LiveOSC.OSCClient import OSCClient
from ..LiveOSC.OSCServer import OSCServer
from ..LiveOSC.UDPClient import UDPClient
from ..LiveOSC.UDPServer import UDPServer
    
class Logger:
    """
    Logs to osc receiver on port 9050
    and to ableton live log
    """
    def __init__(self):
        
        self._yaas_set = 0
        
        # setting up the YAAS OSC Server
        self.basicAPI = 0    
        self.oscServer = OSCServer('localhost', 9050, None, 9089)
        
        filename = os.path.dirname(__file__)[:-4] + os.path.basename("stderr.txt")
        self.oscServer.sendOSC("/yaas/log/errorfile", filename)
           
        self.debug("Logger started")
        
    def set_yaas(self, yaas):
        self.yaas = yaas
        self._yaas_set = 1
        
    def log_to_yaas(self, msg):
        if self._yaas_set == 1:
            self.yaas.log_message(msg)
        
    def error(self,msg):
        self.log_to_yaas(msg)
        self.oscServer.sendOSC("/yaas/log/error", msg)
    
    def debug(self,msg):
        self.log_to_yaas(msg)
        self.oscServer.sendOSC("/yaas/log/debug", msg)
        
    def verbose(self,msg):
        self.log_to_yaas(msg)
        self.oscServer.sendOSC("/yaas/log/verbose", msg)
        
    def info(self,msg):
        self.log_to_yaas(msg)
        self.oscServer.sendOSC("/yaas/log/info", msg)
        
    def write(self, data):
        if self.oscServer is not None:
            self.oscServer.sendOSC("/yaas/log/error", data)
    