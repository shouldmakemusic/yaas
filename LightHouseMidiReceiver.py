"""
#

"""

import Live
""" Constants and configuration """
from consts import *
from config_midi_from_lighthouse import *
from util.RangeUtil import RangeUtil

class LightHouseMidiReceiver:
    __module__ = __name__
    __doc__ = "LightHouseMidiReceiver handles incoming messages from LightHouse"
    
    def __init__(self, parent, c_instance):
        self.log = parent.log
        self._LightHouseMidiReceiver__c_instance = c_instance
        self._parent = parent
        self._range_util_android = RangeUtil(0, 100)
        self._currentClipNumber = 0        

    def build_midi_map(self, midi_map_handle):

        self.log.verbose('(LightHouseMidiReceiver) build_midi_map() called')

        Live.MidiMap.forward_midi_note(self.script_handle(), midi_map_handle, CHANNEL_LIGHTHOUSE, 1)
        Live.MidiMap.forward_midi_note(self.script_handle(), midi_map_handle, CHANNEL_LIGHTHOUSE, 2)
        Live.MidiMap.forward_midi_note(self.script_handle(), midi_map_handle, CHANNEL_LIGHTHOUSE, 3)
        Live.MidiMap.forward_midi_note(self.script_handle(), midi_map_handle, CHANNEL_LIGHTHOUSE, 4)
        Live.MidiMap.forward_midi_note(self.script_handle(), midi_map_handle, CHANNEL_LIGHTHOUSE, 12)
        Live.MidiMap.forward_midi_note(self.script_handle(), midi_map_handle, CHANNEL_LIGHTHOUSE, 13)
        Live.MidiMap.forward_midi_note(self.script_handle(), midi_map_handle, CHANNEL_LIGHTHOUSE, 14)
        
        # midi_note_definitions
        for k, v in midi_note_definitions_lighthouse.iteritems():
            #self.log.debug('registered ' + str(k))
            Live.MidiMap.forward_midi_note(self.script_handle(), midi_map_handle, CHANNEL_LIGHTHOUSE, k)

        return
    
    def receive_midi(self, midi_bytes):
        self.log.verbose('(LightHouseMidiReceiver) receive_midi() ' + str(midi_bytes))

        assert (midi_bytes != None)
        assert isinstance(midi_bytes, tuple)

        if (len(midi_bytes) is 3):
            
            message_type = midi_bytes[0]
            midi_note = midi_bytes[1]
            value = midi_bytes[2]
            #print('found message_type ' + str(message_type)); 
            if (message_type == MESSAGE_TYPE_LIGHTHOUSE_MIDI_NOTE_PRESSED):
                #print('found pressed'); 
                if (midi_note in midi_note_definitions_lighthouse):
                    self.log.verbose('found action');                    
                    self._parent.handle_parametered_function(midi_note_definitions_lighthouse, midi_note, value);
                if (midi_note == 1):
                    if (value == 1):                        
                        #print('found start')
                        track_helper = self._parent._song_helper.get_track_for_name("Alto Flute")
                        if (track_helper is not None):
                            #print('track: ' + track_helper.get_track().name)
                            #device = track_helper.get_device("Flute")
                            track_helper.get_track().clip_slots[1].fire()
                    if (value == 2):                        
                        #print('found stop')
                        track_helper = self._parent._song_helper.get_track_for_name("Alto Flute")
                        if (track_helper is not None):
                            #print('track: ' + track_helper.get_track().name)
                            #device = track_helper.get_device("Flute")
                            track_helper.get_track().clip_slots[1].stop()
                if (midi_note == 2):
                    #print('x: ' + str(value))
                    self.handleKnob(1, value)
                if (midi_note == 3):
                    #print('y: ' + str(value))
                    self.handleKnob(2, value)
                if (midi_note == 4):
                    #print('z: ' + str(value))
                    self.handleKnob(3, value)
                if (midi_note == 12):
                   print('x: ' + str(value))
                   self.add_second_track(value)
                if (midi_note == 13):
                    #print('y: ' + str(value))
                    self.startClip(value)
                #if (midi_note == 14):
                #    print('y: ' + str(value))

            elif (message_type == MESSAGE_TYPE_LIGHTHOUSE_MIDI_NOTE_RELEASED):
                #self.log.debug("released");
                return
        return
    def add_second_track(self, value):
        
        track_helper = self._parent._song_helper.get_track_for_name("DrumBeat")
        if (track_helper is not None):
            value = value - 70
            if (value > 5):
                track_helper.get_track().clip_slots[self._currentClipNumber].fire()
            if (value < 5):
                track_helper.get_track().clip_slots[self._currentClipNumber].stop()
                
    def startClip(self, value):
        track_helper = self._parent._song_helper.get_track_for_name("DrumNorm")
        if (track_helper is not None):
            value = value - 70
            if (value != self._currentClipNumber):
                self._currentClipNumber = value
                track_helper.get_track().clip_slots[value].fire()
            #print('track: ' + track_helper.get_track().name)
            
            
    def handleKnob(self, type, value):
        
        track_helper = self._parent._song_helper.get_track_for_name("Alto Flute")
        if (track_helper is not None):
            device = track_helper.get_device("Flute")
            if (device is not None):
                #print('found hash device: ' + device.name)         
                
                valueX = self._range_util_android.get_value(device.parameters[type], value);
                #print('valueX ' + str(valueX))
                device.parameters[type].value = valueX

    def script_handle(self):
        return self._LightHouseMidiReceiver__c_instance.handle()
    
    def song(self):
        return self._parent.song()