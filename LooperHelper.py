from __future__ import with_statement
import Live

from consts import *
from _Framework.ControlSurfaceComponent import ControlSurfaceComponent
from TrackHelper import TrackHelper

looper_last_track_index = 0

class LooperHelper(ControlSurfaceComponent):
    __module__ = __name__
    __doc__ = 'SongHelper provides easy access to the song'
        
    def __init__(self, parent):
        ControlSurfaceComponent.__init__(self)
        self._parent = parent
    
    def song(self):
        return self._parent.song()
    
    def log_message(self, message):
        self._parent.log_message(message)
    
    def disconnect(self):
        self._parent = None
        if IS_LIVE_9:
            ControlSurfaceComponent.disconnect(self)                
    
    def on_enabled_changed(self):
        pass

    def update(self):    
        pass
    
    def get_looper_index_in_returns(self, targetcount):
        
        rts = self.song().return_tracks
        count = 0
        for i in range(len(rts)):

            if LOOPER in rts[i].name:
                count = count + 1
            if targetcount == count:
                return i
    
    def activate_looper(self, param, value):
        
        index = param[0]
        selected_track = self._parent._song_helper.get_selected_track()
        looperindex = self.get_looper_index_in_returns(index)
        if selected_track.get_send_value(looperindex) == MAX_LOOPER:
            selected_track.set_send_value(looperindex, MIN_LOOPER)
        else:
            selected_track.set_send_value(looperindex, MAX_LOOPER)
        
    def switch_view(self, param, value):
        
        index = param[0]
        global looper_last_track_index
        self._parent.log_message("test switch_view for " + str(index))
        
        looperindex = self.get_looper_index_in_returns(index)
        
        if looper_last_track_index is None:
            # gehe zu looper
            self._parent.log_message("zum looper ")
            looper_last_track_index = self._parent._song_helper.get_selected_track().get_track_index() 
            self.song().view.selected_track = self.song().return_tracks[looperindex]
        else:        

            self._parent.log_message("zur spur " + str(looper_last_track_index))
            self.song().view.selected_track = self.song().tracks[looper_last_track_index]
            looper_last_track_index = None
            
    emulatedLoopClip = {}

    """ 
        Here we define some global variables 
    """
    def clipLooper(self, param, value):
        track_index = param[0]
        
        current_slot = None;
        if str(track_index) in self.emulatedLoopClip:
            current_slot = self.emulatedLoopClip[str(track_index)]
        self.log_message("Emulate Looper 2 for track " + str(track_index) + " with slot " + str(current_slot))
        
        track = self.song().tracks[track_index]
        i = 0
        foundClip = None
        while i<50:            
            if i>=len(track.clip_slots):
                self.log_message("did not find empty clip until " + str(i))
                break;
            clip = track.clip_slots[i].clip

            if clip == None and (len(track.clip_slots) > i+1 and track.clip_slots[i+1].clip == None) and (len(track.clip_slots) > i+2 and track.clip_slots[i+2].clip == None): 
                self.log_message("Clip " + str(i+1) + " is empty");
                foundClip = i
                i = 50;
            i = i + 1

        if foundClip != None:
            if current_slot != None:
                
                if track.clip_slots[current_slot].is_recording:
                    
                    track.clip_slots[current_slot].stop()
                    track.clip_slots[current_slot].fire()
                    del self.emulatedLoopClip[str(track_index)]
                else:
                    self.log_message("else")
                    i = current_slot
                    while i<50:            
                        clip = track.clip_slots[i].clip
                        #self.log_message("Clip " + str(clip));
                        if clip == None:
                            #self.log_message("Clip " + str(i) + " is empty");
                            foundClip = i
                            i = 50;
                        i = i + 1
                    track.clip_slots[foundClip].fire()
                    self.emulatedLoopClip[str(track_index)] = foundClip
            else:
                self.log_message("Switch Looper 1")
                track.clip_slots[foundClip].fire()
                self.emulatedLoopClip[str(track_index)] = foundClip

        