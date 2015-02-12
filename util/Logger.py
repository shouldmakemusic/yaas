import sys
import time
import os

# RemixNet
from ..LiveOSC.OSCClient import OSCClient
from ..LiveOSC.OSCServer import OSCServer
from ..LiveOSC.UDPClient import UDPClient
from ..LiveOSC.UDPServer import UDPServer

from config_logger import *
    
class Logger:
    """
    Logs to osc receiver on port 9050
    and to ableton live log
    """
    def __init__(self, yaas):
        
        self.yaas = yaas
        
        # setting up the YAAS OSC Server
        unused_incoming_port = PORT_LOGGER
        connected = False
        tries = 0
        
        while not connected and tries < 10:
            try:
                self.log_to_yaas("Init logger with outgoing port " + str(PORT_LIGHTHOUSE) + " and incoming port " + str(unused_incoming_port))
                self.oscServer = OSCServer('localhost', PORT_LIGHTHOUSE, None, unused_incoming_port)
            except Exception, err:
                self.log_to_yaas("ERROR IN LOGGER: " + str(err))
                unused_incoming_port = unused_incoming_port + 1  
                tries = tries + 1     
        
        filename = os.path.join(os.path.dirname(__file__)[:-4], os.path.basename("stderr.txt"))
        self.oscServer.sendOSC("/yaas/config/errorfile", filename)
           
        self.debug("Logger started")
                
    def log_to_yaas(self, msg):
        self.yaas.log_message(msg)
        
    def error(self,msg):
        self.log_to_yaas(msg)
        self.oscServer.sendOSC("/yaas/log/error", msg)
    
    def debug(self,msg):
        self.log_to_yaas(msg)
        self.oscServer.sendOSC("/yaas/log/debug", msg)
        
    def verbose(self,msg):
        self.oscServer.sendOSC("/yaas/log/verbose", msg)
        
    def info(self,msg):
        self.log_to_yaas(msg)
        self.oscServer.sendOSC("/yaas/log/info", msg)
        
    def write(self, data):
        if self.oscServer is not None:
            self.oscServer.sendOSC("/yaas/log/error", data)
            
    def log_object_attributes(self, obj):     
        self.log_object_attributes_extended(obj, False)
        
    def log_object_attributes_extended(self, obj, extended):
        for attr in dir(obj):
            method_desc = getattr(obj, attr)
            if extended:
                if "method" in str(method_desc):
                    self.verbose( "obj.%s = %s" % (attr, method_desc))
                    params = method_desc.func_code.co_varnames
                    for i in range(method_desc.func_code.co_argcount):
                        self.verbose("param: " + params[i])
                else:
                    self.verbose( "obj.%s = %s" % (attr, method_desc))
            else:
                self.verbose( "obj.%s = %s" % (attr, method_desc))
                

