"""
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
    
    def scene_helper(self):
        return self.yaas._scene_helper
    
    def view_helper(self):
        return self.yaas._view_helper
    
    def device_helper(self):
        return self.yaas._device_helper
    
    def track_helper(self, track_index):
        """
            Returns either the current track or the track with
            the given index.
            The first track has the index '0'
        """
        track_helper = self.song_helper().get_track(track_index)
        return track_helper