import sys
import time

    
class Logger:
    """
    Logs to osc receiver on port 9050
    and to ableton live log
    """
    def __init__(self, parent, oscServer):
        self._parent = parent
        self.oscServer = oscServer
        
    def error(self,msg):
        self._parent.log_message(msg)
        self.oscServer.sendOSC("/yaas/log/error", msg)
    
    def debug(self,msg):
        self._parent.log_message(msg)
        self.oscServer.sendOSC("/yaas/log/debug", msg)
        
    def info(self,msg):
        self._parent.log_message(msg)
        self.oscServer.sendOSC("/yaas/log/info", msg)
