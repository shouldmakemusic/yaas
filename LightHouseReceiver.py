"""
#

"""

import Live
""" Constants and configuration """
from consts import *
from config_lighthouse import *

class LightHouseReceiver:
    __module__ = __name__
    __doc__ = "LightHouseReceiver handles incoming messages from LightHouse"
    
    def __init__(self, parent, c_instance):
        self._LightHouseReceiver__c_instance = c_instance
        self._parent = parent

    def build_midi_map(self, midi_map_handle):

        print('(LightHouseReceiver) build_midi_map() called')
        
        # midi_note_definitions
        for k, v in midi_note_definitions_lighthouse.iteritems():
            #self.log_message('registered ' + str(k))
            Live.MidiMap.forward_midi_note(self.script_handle(), midi_map_handle, CHANNEL_LIGHTHOUSE, k)

        return
    
    def receive_midi(self, midi_bytes):
        print('(LightHouseReceiver) receive_midi() ' + str(midi_bytes))

        assert (midi_bytes != None)
        assert isinstance(midi_bytes, tuple)

        if (len(midi_bytes) is 3):
            
            message_type = midi_bytes[0]
            midi_note = midi_bytes[1]
            value = midi_bytes[2]
            print('found message_type ' + str(message_type)); 
            if (message_type == MESSAGE_TYPE_LIGHTHOUSE_MIDI_NOTE_PRESSED):
                print('found pressed'); 
                if (midi_note in midi_note_definitions_lighthouse):
                    print('found action');                    
                    self._parent.handle_parametered_function(midi_note_definitions_lighthouse, midi_note, value);
                
            elif (message_type == MESSAGE_TYPE_LIGHTHOUSE_MIDI_NOTE_RELEASED):
                #self.log_message("Button released");
                return
        return

    def script_handle(self):
        return self._LightHouseReceiver__c_instance.handle()
    
    def song(self):
        return self._parent.song()
    
    def log_message(self, message):
        self._parent.log_message(message)