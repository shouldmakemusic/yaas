from YaasController import *

class RedFrameController (YaasController):
    __module__ = __name__
    __doc__ = "Control the behavior of the red frame"
    
    def __init__(self, yaas):

        YaasController.__init__(self, yaas)
        self.log.debug("(RedFrameController) init")
        
    def play_clip(self, params, value):
        """
            Plays the xth clip in the red frame
            At the moment this works only for the track style red frame 
            Has to be tested when triing different styles for the red frame
            0 -> clip_number                       
        """
        self.log.verbose("(RedFrameController) play_clip called")
        clip_number = params[0]
        self.log.verbose("(RedFrameController) for clip " + str(clip_number))
        self.log.verbose("(RedFrameController) scene_offset: " + str(self.yaas.get_session()._scene_offset))

        #if (clip_number > 4):
        """clip_number = clip_number -1"""
        clip_number = self.yaas.get_session()._scene_offset + clip_number
        self.log.verbose("(RedFrameController) calculated number " + str(clip_number))

        self.song_helper().get_selected_track().fire(clip_number);
        
    def move_track_view_vertical(self, params, value):
        """
            Moves the current position down or up
            0 -> True ? down : up                
        """
        self.log.verbose("(RedFrameController) move_track_view_vertical called")
        down = params[0]
        self.log.verbose("(RedFrameController) down? " + str(down))

        self.view_helper().move_track_view_vertical(down)
        
    def move_track_view_horizontal(self, params, value):
        """
            Moves the red frame left or right
            0 -> True ? right : left                
        """
        self.log.verbose("(RedFrameController) move_track_view_horizontal called")
        right = params[0]
        self.log.verbose("(RedFrameController) right? " + str(right))

        self.view_helper().move_track_view_horizontal(right)
