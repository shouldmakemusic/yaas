from __future__ import with_statement
import Live

from consts import *
from _Framework.ControlSurfaceComponent import ControlSurfaceComponent
from TrackHelper import TrackHelper

track_helper = {}

class SongHelper(ControlSurfaceComponent):
    __module__ = __name__
    __doc__ = 'SongHelper provides easy access to the song'
    
    def __init__(self, parent):
        ControlSurfaceComponent.__init__(self)
        self._parent = parent
    
    def song(self):
        return self._parent.song()
    
    def disconnect(self):
        self._parent = None
        self.track_helper = None
        if IS_LIVE_9:
            ControlSurfaceComponent.disconnect(self)    
            
    def get_selected_track(self):
        selected_track = self.song().view.selected_track
        return self.createTrackHelper(selected_track)
    
    def get_track(self, track_index):
        if (track_index == CURRENT):
            return self.get_selected_track()
        
        track = self.song().tracks[track_index]
        return self.createTrackHelper(track)
    
    def get_all_tracks(self):
        all_tracks = ((self.song().tracks + self.song().return_tracks) + (self.song().master_track,))
        return all_tracks
    
    def on_enabled_changed(self):
        pass

    def update(self):    
        pass
    
    def createTrackHelper(self, track):                
        
        with self._parent.component_guard():
            new_track_helper = TrackHelper(self, track)
        index = new_track_helper.get_track_index()
        
        if index in track_helper:
            #self._parent.log_message("Has already track helper for " + str(index))
            new_track_helper = None
        else:
            self._parent.log_message("Created track helper for " + str(index))
            track_helper[index] = new_track_helper
            
        return track_helper[index]
        