from YaasHelper import *

class SceneHelper(YaasHelper):
    __module__ = __name__
    __doc__ = 'SceneHelper provides easy access to the scene functions'
    
    def __init__(self, yaas):

        YaasHelper.__init__(self, yaas)
    
    def get_scene(self, scene_index):
        """
            Returns the scene with the given index
            Starting at 0
            Can also be CURRENT
        """
        if (scene_index == CURRENT):
            return self.song().view.selected_scene
        
        return self.song().scenes[scene_index]
        
    def get_selected_scene(self):
        """
            Returns the selected scene
        """
        return self.get_scene(CURRENT)
        
    def get_name(self, scene_index):
        """
            Returns the name of the scene with given scene_index
        """
        return self.get_scene(scene_index).name
    
    def get_scene_index(self, scene):
        """
            Returns the scene_index of the given scene
            This is only accomplished by the name.
            It finds the first scene with the same name
        """
        for i in range(len(self.song().scenes)):
            current_scene = self.song().scenes[i]
            if current_scene.name == scene.name:
                return i
        return None
                
    def play_scene_only_tracks_with(self, scene_index, name):
        """
            Plays the given scene but only clips in tracks whose name
            start with the given prefix 
            Works also for '# ' track names (that are replaced by numbers)
            If this clipslot has no clip but a stop button -> stop
        """        
    	for i in range(len(self.song().tracks)):
            
            track = self.song().tracks[i]
            track_name = str(track.name)
            if track_name.startswith(name) or track_name.startswith(name, 2):

                clip_slot_index = scene_index
                if scene_index == CURRENT:
                    scene = self.get_scene(CURRENT)
                    clip_slot_index = self.get_scene_index(scene)

                clip_slot = track.clip_slots[clip_slot_index]
                if (clip_slot.has_clip or track.is_foldable) and not clip_slot.will_record_on_start:
                    clip_slot.fire()
                elif clip_slot.has_stop_button and not clip_slot.has_clip:
                    track.stop_all_clips()
            