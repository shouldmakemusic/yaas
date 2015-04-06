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
    TrackHelper provides easy access to the track functions
"""
from YaasHelper import *

class TrackHelper(YaasHelper):
    """
        TrackHelper provides easy access to the track functions
    """
    
    def __init__(self, yaas, track):

        YaasHelper.__init__(self, yaas)
        self.last_played_clip = None
                
        # if the track given is a number
        if isinstance(track, int):            
            if track == CURRENT:
                # get the current track
                self._track = self.song_helper().get_selected_track()
            else:
                # or the track with this index
                self._track = self.song_helper().get_track(track)        
        else:
            # we got the track object
            self._track = track
            
        # get the index of this track
        all_tracks = self.song_helper().get_all_tracks_including_return_and_master()
        self.log.verbose('looking for track ' + self._track.name)
        for i in range(len(all_tracks)):
            if all_tracks[i].name == self._track.name:
                self._track_index = i
                return
    
    def get_track(self):
        return self._track
    
    def get_name(self):
        return self._track.name
    
    def get_track_index(self):
        return self._track_index
                
    def get_devices(self):
        return self._track.devices

    def get_device(self, name):
        
        device = None
        #all_tracks = self.song_helper().get_all_tracks()
        #trackIndex = self._track_index
        
        for i in range(len(self._track.devices)):
            
            dname = self._track.devices[i].name;
            if dname == name:
                device = self._track.devices[i]
        return device

    def get_device_for_id(self, id):
        
        all_tracks = self.song_helper().get_all_tracks()
        trackIndex = self._track_index
        
        if id < len(all_tracks[trackIndex].devices):
            return all_tracks[trackIndex].devices[id]
        return None
            
    def get_selected_device(self):
        device = self._track.view.selected_device
        return device
                    
    def get_send_value(self, index):
        
        if index is None:
            return

        return self._track.mixer_device.sends[index].value
    
    def set_send_value(self, index, value):
        
        if index is None:
            return
        value = float(value);
        
        max = self._track.mixer_device.sends[index].max
        min = self._track.mixer_device.sends[index].min
        if value > max:
            value = max
        if value < min:
            value = min
        self._track.mixer_device.sends[index].value = value
            
    def fire(self, clip_number):
    	"""
    		Fires clip with the given number
    	"""
        if clip_number < len(self._track.clip_slots):
    	       self._track.clip_slots[clip_number].fire()
               
    def get_playing_clip(self):
        """
            Returns the currently playing clip
        """
        track = self._track
        for i in range(len(track.clip_slots)):
            if track.clip_slots[i].is_playing or track.clip_slots[i].is_recording or track.clip_slots[i].is_triggered:
                return track.clip_slots[i].clip
        return None
            
    def stop_or_restart_clip(self):
        """
            If a clip is playing in the this track - stop it and remember it
            If this method is called again and no clip is playing - start it again
        """        
        self.log.verbose("Stopping clips for track " + self._track.name)
            
        track = self._track
        # before stopping - is some clip currently playing?
        was_playing = False
        for i in range(len(track.clip_slots)):
            if track.clip_slots[i].is_playing or track.clip_slots[i].is_recording or track.clip_slots[i].is_triggered:

                # remember track number
                self.last_played_clip = i
                was_playing = True 
        
        if was_playing:
            # stop
            track.stop_all_clips()
            # if track was used in looper - free it
            # TODO: what was that again??????
            #if str(track_index) in self._looper_helper.emulatedLoopClip:
            #    del self._looper_helper.emulatedLoopClip[str(track_index)]
            #self.last_played_clip = None
        else:
            # if there is a remembered track - play it
            if self.last_played_clip is not None:
                track.clip_slots[self.last_played_clip].fire()            

    
