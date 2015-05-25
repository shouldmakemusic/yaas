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
    Control every action around scenes
"""
from YaasController import *

class SceneController (YaasController):
    """
        Control every action around scenes
    """
    
    def __init__(self, yaas):

        YaasController.__init__(self, yaas)
        self.log.debug("(SceneController) init")
        self._session = yaas.get_session()
        
    def play_scene(self, params, value):
        """
            Plays the given scene     
                   
            @param params[0]: scene_index
        """
        self.log.verbose("(SceneController) play_scene called")
        
        scene_index = params[0]
        self.log.verbose("(SceneController) with index " + str(scene_index))
        
        self.scene_helper().get_scene(scene_index).fire()
    
    def play_scene_select_next(self, params, value):
        """
            Plays the given scene and then selects the next scene            
            
            @param params[0]: scene_index
        """
        self.log.verbose("(SceneController) play_scene_select_next called")
        
        scene_index = params[0]
        self.log.verbose("(SceneController) with index " + str(scene_index))

        self.scene_helper().get_scene(scene_index).fire_as_selected()

    def play_scene_only_tracks_with(self, params, value):
        """
            Plays the given scene but only clips in tracks whose name
            start with the given prefix 
            
            @param params[0]: scene_index
            @param params[1]: name
        """
        self.log.verbose("(SceneController) play_scene_only_tracks_with called")
        
        scene_index = params[0]
        name = params[1]
        self.log.verbose("(SceneController) with index " + str(scene_index) + " and name " + name)

        self.scene_helper().play_scene_only_tracks_with(scene_index, name)

    def play_i_tracks_in_current(self, params, value):
        """
            Plays the current scene but only clips in tracks whose name
            start with 'i<number> '
            
            If this clipslot has no clip but a stop button -> stop
            If this clip is playing -> stop
            
            @param params[0]: number
        """
        self.log.verbose("(SceneController) play_i_tracks_in_current called")
        
        number = params[0]
        self.log.verbose("(SceneController) with number " + str(number))

        self.scene_helper().play_scene_only_tracks_with(CURRENT, 'i' + str(number))

    def play_e_tracks_in_current(self, params, value):
        """
            Plays the current scene but only clips in tracks whose name
            start with 'e<number> '
            
            If this clipslot has no clip but a stop button -> stop
            If this clip is playing -> stop
            
            @param params[0]: number
        """
        self.log.verbose("(SceneController) play_e_tracks_in_current called")
        
        number = params[0]
        self.log.verbose("(SceneController) with number " + str(number))

        self.scene_helper().play_scene_only_tracks_with(CURRENT, 'e' + str(number))

    def stop(self, params, value):
        """
            Stops all clips in the given scene
            
            @param params[0]: scene_index
        """
        self.log.verbose("(SceneController) stop called")

        scene_index = params[0]
        self.log.verbose("(SceneController) with index " + str(scene_index))
        
        scene = self.scene_helper().get_scene(scene_index)
            
        for i in range(len(scene.clip_slots)):
            clip_slot = scene.clip_slots[i]
            if clip_slot.is_playing and clip_clot.has_stop_button:
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
        
