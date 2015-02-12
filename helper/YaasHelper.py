import Live

CURRENT = -1

class YaasHelper:
    __module__ = __name__
    __doc__ = "Base class for helpers"
    
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
    
    def device_helper(self):
        return self.yaas._device_helper
    
    def track_helper(self, track_index):
        return self.yaas._song_helper.get_track(track_index)