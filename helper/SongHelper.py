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
    
    def set_current_time(self):
        """
            Sets the current song time (in beats)
            0 -> beats
        """
        beats = params[0]
        self.song().current_song_time = beats

    def get_current_time(self):
        """
            Sets the current song time (in beats)
        """
        return self.song().current_song_time

        