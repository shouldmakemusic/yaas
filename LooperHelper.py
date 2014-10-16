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
        