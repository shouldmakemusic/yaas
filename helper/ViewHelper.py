from YaasHelper import *

class ViewHelper (YaasHelper):
    __module__ = __name__
    __doc__ = "Control the view"
    
    
    def __init__(self, yaas):

        YaasHelper.__init__(self, yaas)
        self.log.debug("(ViewHelper) init")
        
    def move_scene_view(self, down):
                
        all_scenes = self.song().scenes #then get all of the scenes
        scene_index = list(all_scenes).index(self.song().view.selected_scene) #then identify where the selected scene sits in relation to the full list

        self.log.verbose("(ViewHelper) current scene index is " + str(scene_index + 1))
                
        if down:
            self.log.debug("(ViewHelper) scene view down")
            scene_index = scene_index + 1
            self.song().view.selected_scene = self.song().scenes[scene_index]

        else:
            if scene_index == 0:
                return
            self.log.debug("(ViewHelper) scene view up")
            scene_index = scene_index - 1
            self.song().view.selected_scene = self.song().scenes[scene_index]
