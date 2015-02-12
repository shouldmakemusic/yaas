from __future__ import with_statement
import Live

from YaasHelper import *
from TrackHelper import TrackHelper

active_device = None

class DeviceHelper(YaasHelper):
    
    __module__ = __name__
    __doc__ = 'DeviceHelper handles Device actions'
    
    hash_device_track_id = 0
    hash_device_track_helper = None
    hash_device = None

    def __init__(self, yaas):
        YaasHelper.__init__(self, yaas)
        self.log.debug("(SongHelper) init")
    
    
    def log_parameters_for_device(self, device):
        """
            Takes a live device and debugs all parameters and settings
        """
        for index in range(len(device.parameters)):
            self.log.debug("Param " + str(index) + " = " + device.parameters[index].name)
                


    def get_currently_selected_device(self, track_index):
        """
            Return the currently selected device
        """        
        track_helper = self.track_helper(track_index)
        device = track_helper.get_selected_device()        
        return device
    
    """ Stores the device in this class """
    def store_hash_device(self, track_id, device):
        
        self.hash_device_track_id = track_id
        self.hash_device_track_helper = self.song_helper().get_track(track_id)
        self.hash_device = device
        
    def get_hash_device(self):
        return self.hash_device
            
    def get_hash_device_helper(self):
        return self.hash_device_track_helper
            
    def select_current_then_select_next_hash_device(self, track_index):
        """ 
            First call select first device that starts with '#'
            If the name of the appointed device starts with '#' find a new '#'-device
            Store this device - from now on the first call selects this one
        """
        
        self.log.debug("select_current_then_select_next_hash_device")

        selected_track_helper = self.song_helper().get_selected_track()
        
        if self.hash_device_track_helper is None:
            self.log.debug("no device was selected so far")
            self.select_next_hash_device(0)
        #elif self.song().appointed_device.name.startswith('#'):
        elif selected_track_helper.get_track_index() != self.hash_device_track_id:
            self.log.debug("there was a different track selected")
            self.song_helper().set_selected_track(self.hash_device_track_helper)
            
        elif self.song().appointed_device.name.startswith('#'):
            self.log.debug("focus was already on hash device")
            self.select_next_hash_device(self.hash_device_track_id)

        # get the focus to the selected device
        if self.hash_device is not None:
            self.view_helper().focus_on_track(self.hash_device_track_helper.get_track())
            self.view_helper().focus_on_device(self.hash_device)
            
    def select_next_hash_device(self, track_id):

        # iterate through devices and tracks until the next device that startswith '#'        
        max = len(self.song().tracks)
        for i in range(track_id, max):
            track = self.song_helper().get_track(i)
            #self.log.debug("track " + str(i))
            for j in range(len(track.get_devices())):
                device = track.get_devices()[j]
                #self.log.debug("device " + str(j) + ": " + device.name)
                if device.name.startswith('#'):
                    #if self.hash_device is not None:
                    #    self.log.debug("hash_device.name " + self.hash_device.name + ", hash_track_id " + str(self.hash_device_track_id))
                    if (self.hash_device is None) or not (device.name == self.hash_device.name and i == self.hash_device_track_id):
                        self.store_hash_device(i, device)
                        self.log.debug("found hash device on track " + str(i))
                        return 
        if track_id > 0:
            self.log.debug("start from beginning ")
            self.select_next_hash_device(0)
        else:
            self.hash_device_track_helper = None
            self.hash_device_track_id = 0
            self.hash_device = None
        