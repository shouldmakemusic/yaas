from YaasController import YaasController

class RedFrameController (YaasController):
    __module__ = __name__
    __doc__ = "Control the behavior of the red frame"
    
    def __init__(self, yaas):

        YaasController.__init__(self, yaas)
        self.log.debug("(RedFrameController) init")
        self._session = yaas.get_session()
        
    def play_clip(self, params, value):
        """
            Plays the xth clip in the red frame
            At the moment this works only for the track style red frame 
            Maybe even only if it is fixated to the top
            Has to be tested when triing different styles for the red frame
            0 -> clip_number                       
        """
        self.log.verbose("(RedFrameController) play_clip called")

        clip_number = params[0] - 1
        self.log.verbose("(RedFrameController) for clip " + str(clip_number))

        if (clip_number > 4):
            """clip_number = clip_number -1"""
            clip_number = self._session._scene_offset + clip_number
        self.log.verbose("(RedFrameController) calculated number " + str(clip_number))

        self.song_helper().get_selected_track().fire(clip_number);
        