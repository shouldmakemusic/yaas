import Live
import os

from consts import *
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
    
    midi_notes_definitions_temporarily = {}   
    midi_cc_definitions_temporarily = {} 
    midi_note_definitions_for_lighthouse = {}

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
        self.callbackManager.add(self.receive_configuration, "/yaas/controller/receive/configuration")
    
    def setMainScript(self, mainScript):
        self.yaas = mainScript
        # for now
        #self.yaas._device_helper.select_current_then_select_next_hash_device(0)
        #device = self.yaas._device_helper.get_hash_device()
        #if device is not None:
        #    self.log.debug('Using device ' + device.name)  
            
    def send_controller_info(self, msg):
        """
            Calls YAAS.send_available_methods_to_lighthouse()
        """
        self.log.debug('sending controller info to lighthouse')

        self.yaas.send_available_methods_to_lighthouse()
        self.oscServer.sendOSC('/yaas/config/port', 9190);
        
        path = os.path.dirname(__file__)
        self.oscServer.sendOSC("/yaas/config/location", path)
        self.log.verbose('sent ' + path)
        
    def receive_configuration(self, msg):
        """
            From LightHouse comes a new configuration to use before the stored one.
        """
        #for i in range(len(msg)):
        #    self.log.debug("Message " + str(i) + ": " + str(msg[i]))
        
    #1  : [DEVICE_CONTROLLER, 'select_current_then_select_next_hash_device', [0]],
        
        if len(msg) == 3:
            if msg[2] == 'start':
                self.log.debug('start receiving')
                self.midi_notes_definitions_temporarily = {}
                self.midi_note_definitions_for_lighthouse = {}
            if msg[2] == 'end':
                self.log.debug('end receiving')
                self.log.verbose('midi from lighthouse: ' + str(self.midi_notes_definitions_temporarily))

                self.yaas.midi_notes_definitions_temporarily = self.midi_notes_definitions_temporarily   
                self.yaas.midi_cc_definitions_temporarily = self.midi_cc_definitions_temporarily
                self.yaas.midi_note_definitions_for_lighthouse = self.midi_note_definitions_for_lighthouse
                self.yaas.request_rebuild_midi_map()
                
        if len(msg) == 9:
            #self.log.debug('entry: ' + str(msg[2]))
            value1 = self.get_value(msg[6])
            value2 = self.get_value(msg[7])
            value3 = self.get_value(msg[8])
            
            if msg[2] == 'Midi Note':
                self.midi_notes_definitions_temporarily[int(msg[3])] = [msg[4], msg[5], [value1, value2, value3]]
                
            elif msg[2] == 'Midi CC':
                self.midi_cc_definitions_temporarily[int(msg[3])] = [msg[4], msg[5], [value1, value2, value3]]

            elif msg[2] == 'Midi Note LightHouse':
                self.midi_note_definitions_for_lighthouse[int(msg[3])] = [msg[4], msg[5], [value1, value2, value3]]

    
    def get_value(self, value):
        
        if value.isdigit():
            return int(value)
        elif value == 'CURRENT':
            return CURRENT
        elif value == 'PREV':
            return PREV
        elif value == 'NEXT':
            return NEXT
        return value
            


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
        
            device = self.yaas._device_helper.get_hash_device()
            
            range_util = RangeUtil(-10, 10)
            valueX = range_util.get_value(device.parameters[1], x);
            valueY = range_util.get_value(device.parameters[2], y);
            valueZ = range_util.get_value(device.parameters[3], z);
            #print('Normalized values: ' + str(valueX) + ", " + str(valueY) + ", " + str(valueZ))

            device.parameters[1].value = valueX
            device.parameters[2].value = valueY
            device.parameters[3].value = valueZ
            
