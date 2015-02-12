from YaasController import *

class SceneController (YaasController):
    __module__ = __name__
    __doc__ = "Control every action around scenes"
    
    def __init__(self, yaas):

        YaasController.__init__(self, yaas)
        self.log.debug("(SceneController) init")
        self._session = yaas.get_session()
        
    def play_scene(self, params, value):
        """
            Plays the given scene            
            0 -> scene_index
        """
        self.log.verbose("(SceneController) play_scene called")
        
        scene_index = params[0]
        self.log.verbose("(SceneController) with index " + str(scene_index))
        
        if (scene_index == CURRENT):
            self.song_helper().get_selected_scene().fire()
        else:
            self.song_helper().get_scene(scene_index).fire()
    
    def play_scene_select_next(self, params, value):
        """
            Plays the given scene and then selects the next scene            
            0 -> scene_index
        """
        self.log.verbose("(SceneController) play_scene_select_next called")
        
        scene_index = params[0]
        self.log.verbose("(SceneController) with index " + str(scene_index))

        self.song_helper().get_scene(scene_index).fire_as_selected()

    def stop(self, params, value):
        """
            Stops all clips in the given scene
            0 -> scene_index
        """
        self.log.verbose("(SceneController) stop called")

        scene_index = params[0]
        self.log.verbose("(SceneController) with index " + str(scene_index))
        
        if scene_index == CURRENT:
            scene = self.song_helper().get_selected_scene()
        else:
            self.song_helper().get_scene(scene_index)
            
        for i in range(len(scene.clip_slots)):
            clip_slot = scene.clip_slots[i]
            if clip_slot.is_playing:
                clip_slot.stop()

    def scene_down(self, params, value):
        """
            The next scene will be selected
        """
        self.log.verbose("(SceneController) scene_down called")
        self.view_helper().move_scene_view(True)
        
    def scene_up(self, params, value):
        """
            The previous scene will be selected
        """
        self.log.verbose("(SceneController) scene_up called")
        self.view_helper().move_scene_view(False)


