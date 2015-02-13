from __future__ import with_statement

from YaasHelper import *
from TrackHelper import TrackHelper

track_helper = {}

class SongHelper(YaasHelper):
    __module__ = __name__
    __doc__ = 'SongHelper provides easy access to the song'
    
    def __init__(self, yaas):
        YaasHelper.__init__(self, yaas)
        self.log.debug("(SongHelper) init")
    
    def get_selected_track(self):
        """
            Returns a track_helper for the currently selected track
        """
        selected_track = self.song().view.selected_track
        return self.getOrCreateTrackHelper(selected_track)

    def set_selected_track(self, track_helper):
        self.song().view.selected_track = track_helper.get_track()
        
    def get_track(self, track_index):
        
        if (track_index == CURRENT):
            return self.get_selected_track()

        track = self.song().tracks[int(track_index)]
        return self.getOrCreateTrackHelper(track)
    
    def get_track_for_name(self, name):
        for i in range(len(self.song().tracks)):
            if self.song().tracks[i].name == name:
                return self.get_track(i)
        return None
    
    def get_all_tracks(self):
        return self.song().tracks
    
    def get_all_tracks_including_return_and_master(self):
        all_tracks = ((self.song().tracks + self.song().return_tracks) + (self.song().master_track,))
        return all_tracks
    
    def getOrCreateTrackHelper(self, track):                
        
        with self.yaas.component_guard():
            new_track_helper = TrackHelper(self.yaas, track)
        index = new_track_helper.get_track_index()
        
        if index in track_helper:
            self.log.verbose("Has already track helper for " + str(index))
            new_track_helper = None
        else:
            self.log.verbose("Created track helper for " + str(index))
            track_helper[index] = new_track_helper
            
        return track_helper[index]
        