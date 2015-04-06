# Copyright (C) 2015 Manuel Hirschauer (manuel@hirschauer.net)
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
# For questions regarding this module contact
# Manuel Hirschauer <manuel@hirschauer.net> 
"""
"""
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
    
    midi_note_definitions_temporarily = {}   
    midi_cc_definitions_temporarily = {} 
    midi_note_definitions_for_lighthouse = {}
    midi_note_off_definitions_temporarily = {}
    light_definitions_temporarily = {}

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
                self.midi_note_definitions_temporarily = {}
                self.midi_note_definitions_for_lighthouse = {}
                self.midi_note_off_definitions_temporarily= {}
                self.light_definitions_temporarily = {}
            if msg[2] == 'end':
                self.log.debug('end receiving')
                self.log.verbose('midi from lighthouse: ' + str(self.midi_note_definitions_temporarily))

                follow_up_events = {}
                for k, v in self.midi_note_definitions_temporarily.iteritems():
                    if len(v) == 4:
                        key = v[3][0]
                        if key is not None:
                            follow_up_events[key] = k
                self.yaas.follow_up_events = follow_up_events
                self.log.verbose("Found follow up events " + str(follow_up_events))
                
                for k, v in self.midi_note_definitions_temporarily.iteritems():
                    self.yaas.midi_note_definitions[k] = v  
                for k, v in self.midi_cc_definitions_temporarily.iteritems():
                    self.yaas.midi_cc_definitions[k] = v  
                for k, v in self.midi_note_definitions_for_lighthouse.iteritems():
                    self.yaas.midi_note_definitions_for_lighthouse[k] = v  
                for k, v in self.midi_note_off_definitions_temporarily.iteritems():
                    self.yaas.midi_note_off_definitions[k] = v
                for k, v in self.light_definitions_temporarily.iteritems():
                    self.yaas.light_definitions[k] = v
                    
        elif len(msg) == 5:
            self.log.verbose('(OCSReceiver) got ' + str(msg))
            command = self.get_value(msg[2])
            midi_command = self.get_value(msg[3])
            midi_note = self.get_value(msg[4])
            self.log.verbose('Midi command ' + str(midi_command))
            self.log.verbose('Midi note ' + str(midi_note))
            self.light_definitions_temporarily[command] = [midi_command, midi_note]

        elif len(msg) == 9 or len(msg) == 10:
            #self.log.debug('entry: ' + str(msg[2]))
            value1 = self.get_value(msg[6])
            value2 = self.get_value(msg[7])
            value3 = self.get_value(msg[8])
            follow_up = None
            if len(msg) == 10:
                self.log.verbose("set follow up")
                follow_up = self.get_value(msg[9])
            
            if msg[2] == 'Midi Note' or msg[2] == 'Midi Note On':
                self.midi_note_definitions_temporarily[int(msg[3])] = [msg[4], msg[5], [value1, value2, value3], [follow_up]]
                
            elif msg[2] == 'Midi Note Off':
                self.midi_note_off_definitions_temporarily[int(msg[3])] = [msg[4], msg[5], [value1, value2, value3], [follow_up]]

            elif msg[2] == 'Midi CC':
                self.midi_cc_definitions_temporarily[int(msg[3])] = [msg[4], msg[5], [value1, value2, value3], [follow_up]]

            elif msg[2] == 'Midi Note LightHouse':
                self.midi_note_definitions_for_lighthouse[int(msg[3])] = [msg[4], msg[5], [value1, value2, value3], [follow_up]]
        else:
            self.log.verbose('Unknown message received ' + str(msg))
    
    def get_value(self, value):
        
        if value.isdigit() or (value.startswith('-') and value[1:].isdigit()):
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
            
