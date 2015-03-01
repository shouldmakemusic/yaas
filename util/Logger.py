import sys
import time
import os

# RemixNet
from ..LiveOSC.OSCClient import OSCClient
from ..LiveOSC.OSCServer import OSCServer
from ..LiveOSC.UDPClient import UDPClient
from ..LiveOSC.UDPServer import UDPServer

from ..config.Configuration import Configuration
    
class Logger:
    """
    Logs to osc receiver on port [LightHouse]/port (default.cfg)
    and to ableton live log
    """
    def __init__(self, yaas):
        
        self.yaas = yaas
        self.config = Configuration(None)
        
        # setting up the YAAS OSC Client
        connected = False
        tries = 0
        
        while not connected and tries < 10:
            try:
                outgoing_port = self.config.get_lighthouse_port()
                self.log_to_yaas("Init logger with outgoing port " + str(outgoing_port))
                self.oscServer = OSCServer('localhost', outgoing_port, None, None)
                connected = True
            except Exception, err:
                self.log_to_yaas("ERROR IN LOGGER: " + str(err))
                tries = tries + 1     
        
        #filename = os.path.join(os.path.dirname(__file__)[:-4], os.path.basename("stderr.txt"))
        #self.oscServer.sendOSC("/yaas/config/errorfile", filename)
           
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
        self.log_object_attributes_intern(obj, False)
        
    def log_object_attributes_extended(self, obj):
        self.log_object_attributes_intern(obj, True)
    
    def log_object_attributes_intern(self, obj, extended):
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
    