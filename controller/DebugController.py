from YaasController import *

class DebugController (YaasController):
    __module__ = __name__
    __doc__ = "Debug methods and tests"
    
    def __init__(self, yaas):

        YaasController.__init__(self, yaas)
        self.log.debug("(DebugController) init")
        
    def send_available_methods_to_lighthouse(self, params, value):
        
        self.yaas.send_available_methods_to_lighthouse()
