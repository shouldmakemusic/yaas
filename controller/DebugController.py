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
    Debug methods and tests
"""
from YaasController import *

class DebugController (YaasController):
    """
        Debug methods and tests
    """
        
    def __init__(self, yaas):

        YaasController.__init__(self, yaas)
        self.log.debug("(DebugController) init")
        
    def send_available_methods_to_lighthouse(self, params, value):
        
        self.yaas.send_available_methods_to_lighthouse()
        
    def show_parameters_for_device(self, params, value):
        """
            Logs the parameter names for the given device
            
            @param params[0]: track_index
            @param params[1]: device_name or CURRENT
        """

        track_index = params[0]
        device_name = params[1]
        
        track_helper = self.song_helper().get_track(track_index)
        
        if device_name == CURRENT:
            device = track_helper.get_selected_device()
        else:
            device = track_helper.get_device(device_name)
        self.log.verbose('Device ' + str(device))
        
        self.device_helper().log_parameters_for_device(device)
        
    def show_value(self, params, value):
        self.log.debug("(DebugController) show_value: " + str(value))
