import Live

CURRENT = -1

class YaasController:
    __module__ = __name__
    __doc__ = "Base class for controllers"
    
    def __init__(self, yaas):
        self.yaas = yaas
        self.log = yaas.log
        
    def application(self):
        """
            Returns the Live.Application object (live_app)
        """
        return Live.Application.get_application()

    def song(self):
        """
            Returns the Live.Song object (live_set)
        """
        return Live.Application.get_application().get_document()
    
    def song_helper(self):
        return self.yaas._song_helper
    
    def view_helper(self):
        return self.yaas._view_helper
    
    def device_helper(self):
        return self.yaas._device_helper
    
    def track_helper(self, track_index):
        """
            Returns either the current track or the track with
            the given index.
            The first track has the index '1'
            
            0 -> track_index
        """
        if (track_index == CURRENT):
            track_helper = self.song_helper().get_selected_track()
        else:
            track_helper = self.song_helper().get_track(track_index - 1)

        return track_helper