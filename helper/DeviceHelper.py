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
    DeviceHelper handles Device actions
"""
from __future__ import with_statement
import Live

from YaasHelper import *
from TrackHelper import TrackHelper
from ..consts import CURRENT

active_device = None

class DeviceHelper(YaasHelper):
    """
        DeviceHelper handles Device actions
    """
    
    hash_device_track_id = 0
    hash_device_track_helper = None
    hash_device = None

    def __init__(self, yaas):
        
        YaasHelper.__init__(self, yaas)
        self.log.debug("(DeviceHelper) init")
    
    def log_parameters_for_device(self, device):
        """
            Takes a live device and debugs all parameters and settings
            
            @param device: device to debug
        """
        if device is not None:
            self.log.verbose('(DeviceHelper) log parameters for ' + device.name)
            for index in range(len(device.parameters)):
                self.log.debug("Param " + str(index) + " = " + device.parameters[index].name)
        else:
            self.log.error('(DeviceHelper) no device given')

    def get_currently_selected_device(self, track_index):
        """
            Return the currently selected device
            
            @param track_index: int
            @return: Live Device
        """        
        track_helper = self.track_helper(track_index)
        device = track_helper.get_selected_device()        
        return device
    
    def store_hash_device(self, track_index, device):
        """ 
            Stores the device in this class 

            @param track_index: index of track that contains hash device
            @param device: hash device itself
        """
        self.log.verbose('(DeviceHelper) store track ' + str(track_index) + ' device ' + device.name)
        self.hash_device_track_id = track_index
        self.hash_device_track_helper = self.song_helper().get_track(track_index)
        self.hash_device = device
        
    def get_hash_device(self):
        """
            Return the currently selected hash device.
            
            If none is seleceted then the next one is searched and returned
            
            @return: Live Device
        """        
    	if self.hash_device is None:
    		self.select_current_then_select_next_hash_device(CURRENT)
        return self.hash_device
            
    def get_hash_device_helper(self):
        """
            Return the track helper for the currently selected hash device.
            
            If none is seleceted then the next one is searched and returned
            
            @return: TrackHelper
        """        
        if self.hash_device_track_helper is None:
    		self.select_current_then_select_next_hash_device(CURRENT)
        return self.hash_device_track_helper
            
    def select_current_then_select_next_hash_device(self, track_index = 0):
        """ 
            First call select first device that starts with '#'
            If the name of the appointed device starts with '#' find a new '#'-device
            Store this device - from now on the first call selects this one
            
            @param track_index: track_index to start search from (optional)
        """
        
        self.log.debug("(DeviceHelper) select_current_then_select_next_hash_device starting at " + str(track_index))

        start_track_helper = self.song_helper().get_track(track_index)
        
        if self.hash_device_track_helper is None:
            self.log.debug("(DeviceHelper) no device was selected so far")
            self.select_next_hash_device(track_index)
        #elif self.song().appointed_device.name.startswith('#'):
        elif start_track_helper.get_track_index() != self.hash_device_track_id:
            self.log.debug("(DeviceHelper) there was a different track selected")
            self.song_helper().set_selected_track(self.hash_device_track_helper)
            
        elif self.song().appointed_device is not None and self.song().appointed_device.name.startswith('#'):
            self.log.debug("(DeviceHelper) focus was already on hash device")
            self.select_next_hash_device(self.hash_device_track_id)

        elif self.get_currently_selected_device(track_index) is not None and self.get_currently_selected_device(track_index).name.startswith('#'):
            self.log.debug("(DeviceHelper) focus was already on hash device")
            self.select_next_hash_device(self.hash_device_track_id)

        # get the focus to the selected device
        if self.hash_device is not None:
            self.log.verbose("(DeviceHelper) focus on hash device")
            self.view_helper().focus_on_track(self.hash_device_track_helper.get_track())
            self.view_helper().focus_on_device(self.hash_device)
            
    def select_next_hash_device(self, track_index = 0):
        """ 
            First call select first device that starts with '#'
            If the name of the appointed device starts with '#' find a new '#'-device
            Store this device - from now on the first call selects this one        
                 
            @param track_index: track_index to start search from (optional)
        """
        # iterate through devices and tracks until the next device that startswith '#' 
        # TODO: add master       
        all_tracks = self.song_helper().get_all_tracks_including_return_and_master()
        max = len(all_tracks)
        for i in range(track_index, max):
            track = all_tracks[i]
            #self.log.debug("track " + str(i))
            for j in range(len(track.devices)):
                device = track.devices[j]
                #self.log.debug("device " + str(j) + ": " + device.name)
                if device.name.startswith('#'):
                    #if self.hash_device is not None:
                    #    self.log.debug("hash_device.name " + self.hash_device.name + ", hash_track_id " + str(self.hash_device_track_id))
                    if (self.hash_device is None) or not (device.name == self.hash_device.name and i == self.hash_device_track_id):
                        self.log.verbose("found hash device on track " + str(i))
                        self.store_hash_device(i, device)
                        return 
        
        if track_index > 0:
            self.log.verbose("start from beginning ")
            self.select_next_hash_device(0)
        else:
            self.hash_device_track_helper = None
            self.hash_device_track_id = 0
            self.hash_device = None
            
