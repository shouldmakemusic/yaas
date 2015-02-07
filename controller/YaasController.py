import Live

class YaasController:
    __module__ = __name__
    __doc__ = "Control the behavior of the red frame"
    
    def __init__(self, yaas):
        self.yaas = yaas
        self.log = yaas.log
        self._song_helper = yaas._song_helper
        self._device_helper = yaas._device_helper
        
    def application(self):
        return Live.Application.get_application()

    def song(self):
        return Live.Application.get_application().get_document()
    
    def song_helper(self):
        return self._song_helper
    
    def device_helper(self):
        return self._device_helper
    
    def track_helper(self, track_index):
        return self._song_helper.get_track(track_index)