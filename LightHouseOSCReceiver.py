import Live

from util.RangeUtil import RangeUtil
# OSC
from LiveOSC.OSCMessage import OSCMessage
from LiveOSC.CallbackManager import CallbackManager
from LiveOSC.OSCUtils import *

# RemixNet
import LiveOSC.OSCClient
import LiveOSC.OSCServer
import LiveOSC.UDPClient
import LiveOSC.UDPServer


class LightHouseOSCReceiver:
    
    def __init__(self, oscServer, logger):
        
        self.log = logger
        self.log.debug('(LightHouseOSCReceiver) init')
        if oscServer:
            self.oscServer = oscServer
            self.callbackManager = oscServer.callbackManager
            self.oscClient = oscServer.oscClient
                        
        else:
            self.log.error('(LightHouseOSCReceiver) will not work because no oscServer has been given')
            return
        
        self.callbackManager.add(self.sensorX, "/android/sensor")
        self.callbackManager.add(self.send_controller_info, "/yaas/controller/send/info")
    
    def setMainScript(self, mainScript):
        self._parent = mainScript
        # for now
        #self._parent._device_helper.select_current_then_select_next_hash_device(0)
        #device = self._parent._device_helper.get_hash_device()
        #if device is not None:
        #    self.log.debug('Using device ' + device.name)  
            
    def send_controller_info(self, msg):
        self._parent.send_available_methods_to_lighthouse()

    def sensorX(self, msg):
        """Called when a /android/sensor measurement is received.

        Messages:
        /android/sensor (float tempo)   Set the tempo, replies with /live/tempo (float tempo)
        """
        if len(msg) == 5:
            x = msg[2]
            y = msg[3]
            z = msg[4]
            #print('Received values: ' + str(x) + ", " + str(y) + ", " + str(z))
        
            device = self._parent._device_helper.get_hash_device()
            
            range_util = RangeUtil(-10, 10)
            valueX = range_util.get_value(device.parameters[1], x);
            valueY = range_util.get_value(device.parameters[2], y);
            valueZ = range_util.get_value(device.parameters[3], z);
            #print('Normalized values: ' + str(valueX) + ", " + str(valueY) + ", " + str(valueZ))

            device.parameters[1].value = valueX
            device.parameters[2].value = valueY
            device.parameters[3].value = valueZ
            
