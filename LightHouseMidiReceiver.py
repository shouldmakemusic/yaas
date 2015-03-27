"""
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
import Live
""" Constants and configuration """
from consts import *
from util.RangeUtil import RangeUtil

class LightHouseMidiReceiver:
    __module__ = __name__
    __doc__ = "LightHouseMidiReceiver handles incoming messages from LightHouse"
    
    def __init__(self, yaas, c_instance):
        self.log = yaas.log
        self._LightHouseMidiReceiver__c_instance = c_instance
        self.yaas = yaas
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
        for k, v in self.yaas.midi_note_definitions_for_lighthouse.iteritems():
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
                if (midi_note in self.yaas.midi_note_definitions_for_lighthouse):
                    self.log.verbose('found action');                    
                    self.yaas.handle_parametered_function(self.yaas.midi_note_definitions_for_lighthouse, midi_note, value);
                if (midi_note == 1):
                    if (value == 1):                        
                        #print('found start')
                        track_helper = self.yaas._song_helper.get_track_for_name("Alto Flute")
                        if (track_helper is not None):
                            #print('track: ' + track_helper.get_track().name)
                            #device = track_helper.get_device("Flute")
                            track_helper.get_track().clip_slots[1].fire()
                    if (value == 2):                        
                        #print('found stop')
                        track_helper = self.yaas._song_helper.get_track_for_name("Alto Flute")
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
        
        track_helper = self.yaas._song_helper.get_track_for_name("DrumBeat")
        if (track_helper is not None):
            value = value - 70
            if (value > 5):
                track_helper.get_track().clip_slots[self._currentClipNumber].fire()
            if (value < 5):
                track_helper.get_track().clip_slots[self._currentClipNumber].stop()
                
    def startClip(self, value):
        track_helper = self.yaas._song_helper.get_track_for_name("DrumNorm")
        if (track_helper is not None):
            value = value - 70
            if (value != self._currentClipNumber):
                self._currentClipNumber = value
                track_helper.get_track().clip_slots[value].fire()
            #print('track: ' + track_helper.get_track().name)
            
            
    def handleKnob(self, type, value):
        
        track_helper = self.yaas._song_helper.get_track_for_name("Alto Flute")
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
        return self.yaas.song()