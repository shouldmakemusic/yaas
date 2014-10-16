import Live

from consts import *
from _Framework.ControlSurfaceComponent import ControlSurfaceComponent

lastPlayedClipForTrack = None

class TrackHelper(ControlSurfaceComponent):
    __module__ = __name__
    __doc__ = 'TrackHelper provides easy access to the track functions'
    
    def __init__(self, song_helper, track):
        ControlSurfaceComponent.__init__(self)
        self._song_helper = song_helper
                
        # if the track given is a number
        if isinstance(track, int):            
            if track == CURRENT:
                # get the current track
                self._track = self._song_helper.get_selected_track()
            else:
                # or the track with this index
                self._track = self._song_helper.get_track(track)        
        else:
            # we got the track object
            self._track = track
            
        # get the index of this track
        all_tracks = self._song_helper.get_all_tracks()
        for i in range(len(all_tracks)):
            if all_tracks[i].name == self._track.name:
                self._track_index = i
    
    def song(self):
        return self._song_helper._parent.song()
    
    def log_message(self, message):
        self._song_helper._parent.log_message(message)
    
    def disconnect(self):
        self._song_helper = None
        self._track = None
        
        if IS_LIVE_9:
            ControlSurfaceComponent.disconnect(self)                
    
    def on_enabled_changed(self):
        pass

    def update(self):    
        pass
    
    def get_track(self):
        return self._track
    
    def get_track_index(self):
        return self._track_index
    
    def stop_clips_on_track(self):
        
        self.log_message("Stopping clips for track " + self._track.name)
            
        # before stopping - is some clip currently playing?
        was_playing = False
        for i in range(len(self._track.clip_slots)):
            if self._track.clip_slots[i].is_playing or self._track.clip_slots[i].is_recording:
                global arrayLastPlayedClipForTrack
                # remember track number
                lastPlayedClipForTrack = i
                was_playing = True 
        
        if was_playing:
            # stop
            self._track.stop_all_clips()
            # if track was used in looper - free it
            ''' TODO '''
            #if str(trackIndex) in emulatedLoopClip:
            #    del emulatedLoopClip[str(trackIndex)]
        else:
            # if there is a remembered track - play it
            if lastPlayedClipForTrack != None:
                self._track.clip_slots[lastPlayedClipForTrack].fire()
                
    def get_device(self, name):
        
        device = None
        #all_tracks = self._song_helper.get_all_tracks()
        #trackIndex = self._track_index
        
        for i in range(len(self._track.devices)):
            
            dname = self._track.devices[i].name;
            if dname == name:
                device = self._track.devices[i]
        return device

    def get_device_for_id(self, id):
        
        all_tracks = self._song_helper.get_all_tracks()
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
        
        if value > MAX:
            value = self._track.mixer_device.sends[index].max
        if value < MIN:
            value = self._track.mixer_device.sends[index].min
        self._track.mixer_device.sends[index].value = value
        
    def arm(self, params, value):
        if self._track.arm == True:
            self._track.arm = False
        else:
            self._track.arm = True;
            
    def get_focus(self, params, value):
        self._song_helper._parent.song().view.selected_track = self._track
        