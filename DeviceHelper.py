from __future__ import with_statement
import Live

from consts import *
from _Framework.ControlSurfaceComponent import ControlSurfaceComponent
from TrackHelper import TrackHelper

active_device = None

class DeviceHelper(ControlSurfaceComponent):
    __module__ = __name__
    __doc__ = 'DeviceHelper handles Device actions'
    
    def __init__(self, parent):
        ControlSurfaceComponent.__init__(self)
        self._parent = parent
        self.log = self._parent.log
    
    def song(self):
        return self._parent.song()
    
    def disconnect(self):
        self._parent = None
        if IS_LIVE_9:
            ControlSurfaceComponent.disconnect(self)                
    
    def on_enabled_changed(self):
        pass

    def update(self):    
        pass
    
    def log_parameters_for_device(self, device):
    
        for index in range(len(device.parameters)):
            self.log.debug("Param " + str(index) + " = " + device.parameters[index].name)
                
    def trigger_device_chain(self, params, value):
        """
            effect has to be named like TRIGGER_DEVICE_CHAIN_NAME_ INC/EXC
            exclusive means only one chain is not muted
            inclusive means the selected chain gets switched
        """
        track_id = params[0]
        chain_id = params[1]
        
        track_helper = self._parent._song_helper.get_track(track_id)
        #number = chain[:-1]
        device = track_helper.get_device(TRIGGER_DEVICE_CHAIN_NAME_EXC)
        if device is not None:
            if len(device.chains) > chain_id:
                
                #self.log.debug("Trigger chain " + str(chain_id + 1) + " with " + str(len(device.chains)) + " chains")                
                if device.chains[chain_id].mute == True:
                    self.log.debug("was muted")
                    for index in range(len(device.chains)):
                    
                        if index == chain_id:
                            device.chains[index].mute = False
                        else:           
                            device.chains[index].mute = True
                else:
                    self.log.debug("was not muted")
                    device.chains[chain_id].mute = True
                    device.chains[0].mute = False

        device = track_helper.get_device(TRIGGER_DEVICE_CHAIN_NAME_INC)
        if device is not None:
            if len(device.chains) > chain_id:
                
                self.log.debug("Trigger chain " + str(chain_id + 1) + " with " + str(len(device.chains)) + " chains")
                
                if device.chains[chain_id].mute == True:
                    device.chains[chain_id].mute = False
                else:           
                    device.chains[chain_id].mute = True

    def get_currently_selected_device(self, track_id):
        """
            Return TrackHelper of the currently selected device
        """
        
        track_helper = self._parent._song_helper.get_track(track_id)        
        device = track_helper.get_selected_device()
        
        if device is None:            
            device = track_helper.get_selected_device()

        return device
    
    def navigate_device_focus(self, params, value):
        """
            Selects next or previous device
        """
        
        # ensures there is an active device
        track_id = params[0]
        next = params[1]
        device = self.get_currently_selected_device(track_id)
        
        selected_track = self._parent._song_helper.get_selected_track()
        target_track = self._parent._song_helper.get_track(track_id)
        self.log.debug('target ' + target_track.name + ', selected ' + selected_track.name)
        
        if selected_track.get_track_index() == target_track.get_track_index() and self.application().view.is_view_visible("Detail/DeviceChain"):
            if next == True:
                self.application().view.focus_view("Detail") 
                self.application().view.scroll_view(3, "Detail/DeviceChain", 0)
            else:
                self.application().view.focus_view("Detail") 
                self.application().view.scroll_view(2, "Detail/DeviceChain", 0)
        else:
            target_track.get_focus(None)
            self.application().view.focus_view("Detail") 
            self.application().view.focus_view("Detail/DeviceChain")
            if device is None:
                device = target_track.get_device_for_id(0)
                if device is not None:
                    self.song().view.select_device(device)
            else:
                self.song().view.select_device(device)

    def toggle_device(self, params, value):
        """
            Switches selected of defined device on/off
        """

        track_id = params[0]
        device_id = params[1]
        
        if track_id == CURRENT:
            track_id = self._parent._song_helper.get_selected_track().get_track_index()
        
        if device_id == CURRENT:
            device = self.get_currently_selected_device(track_id)
        else:
            device = self._parent._song_helper.get_track(track_id).get_device_for_id(device_id)
            
        global active_device
        
        self.application().view.focus_view("Detail/DeviceChain") 
            
        if device.parameters[0].value == 0.0:

            device.parameters[0].value = 1.0
            active_device = device.name
            self.log.debug("toogle " + device.name + " on")

        else:
            device.parameters[0].value = 0.0
            active_device = None
            self.log.debug("toogle " + device.name + " off")
        
    def set_chain_selector(self, params, value):
        
        chain_id = params[0]
        device = self.get_hash_device()
        
        if device is not None:
            
            # find chain parameter
            chain_parameter = None
            if device.parameters[9].is_enabled == True:
                self.log.debug('chain 9 is enabled' )
                chain_parameter = device.parameters[9]
            else:
                for i in range(len(device.parameters)):
                    if device.parameters[i].name == "Chain Selector" and device.parameters[i].is_enabled:
                        chain_parameter = device.parameters[i]
            
            # store old values
            global _chain_parameter_values
            chain_name = device.name + '_' + str(int(chain_parameter.value)) + '_'
            self._parent._value_container.set_value(chain_name + device.parameters[1].name, device.parameters[1].value)
            self._parent._value_container.set_value(chain_name + device.parameters[2].name, device.parameters[2].value)
            self._parent._value_container.set_value(chain_name + device.parameters[3].name, device.parameters[3].value)
            self._parent._value_container.set_value(chain_name + device.parameters[4].name, device.parameters[4].value)                            
            
            self.log.debug("set chain activator to " + str(chain_id + 1) + ' from ' + str(len(device.chains)) + ' for ' + device.name)
            if len(device.chains) > chain_id:
                # set selector
                value = chain_id
                #self.log.debug("max " + str(chain_parameter.max))
                #self.log.debug("min " + str(chain_parameter.min))
                #if CHAIN_MODE_SHORTENED:
                #    value = 127 / 7 * value
                #self.log.debug("new value " + str(value))
                chain_parameter.value = value
                
                #self.log.debug("done for " + chain_parameter.name)
                            
                # restore values of first four parameters
                # only if new chain is not 0 (=normal)
                if (chain_id > 0):
                    chain_name = device.name + '_' + str(chain_id) + '_'
                    if self._parent._value_container.has_value(chain_name + device.parameters[1].name):
                        device.parameters[1].value = self._parent._value_container.get_single_value(chain_name + device.parameters[1].name)
                    if self._parent._value_container.has_value(chain_name + device.parameters[2].name):
                        device.parameters[2].value = self._parent._value_container.get_single_value(chain_name + device.parameters[2].name)
                    if self._parent._value_container.has_value(chain_name + device.parameters[3].name):
                        device.parameters[3].value = self._parent._value_container.get_single_value(chain_name + device.parameters[3].name)
                    if self._parent._value_container.has_value(chain_name + device.parameters[4].name):
                        device.parameters[4].value = self._parent._value_container.get_single_value(chain_name + device.parameters[4].name)

    hash_device_track_id = 0
    hash_device_track_helper = None
    hash_device = None
    
    """ Stores the device in this class """
    def store_hash_device(self, track_id, device):
        
        self.hash_device_track_id = track_id
        self.hash_device_track_helper = self._parent._song_helper.get_track(track_id)
        self.hash_device = device
        
    def get_hash_device(self):
        return self.hash_device
            
    def get_hash_device_helper(self):
        return self.hash_device_track_helper
            
    def select_current_then_select_next_hash_device(self, params, value):
        """ 
            First call select first device that starts with '#'
            If the name of the appointed device starts with '#' find a new '#'-device
            Store this device - from now on the first call selects this one
             
            params[0] = trackid i.e. [0] 
            value = unused
        """
        
        self.log.debug("select_current_then_select_next_hash_device")
        track_id = params[0]        
        #track_helper = self._parent._song_helper.get_track(track_id)
        selected_track_helper = self._parent._song_helper.get_selected_track()
        
        if self.hash_device_track_helper is None:
            self.log.debug("no device was selected so far")
            self.select_next_hash_device(0)
        #elif self.song().appointed_device.name.startswith('#'):
        elif selected_track_helper.get_track_index() != self.hash_device_track_id:
            self.log.debug("there was a different track selected")
            self._parent._song_helper.set_selected_track(self.hash_device_track_helper)
            
        elif self.song().appointed_device.name.startswith('#'):
            self.log.debug("focus was already on hash device")
            self.select_next_hash_device(self.hash_device_track_id)

        # get the focus to the selected device
        if self.hash_device is not None:
            self.focus(self.hash_device)
            
    def focus(self, device):        
        self.log.debug("get focus")
        self.hash_device_track_helper.get_focus(None, None)
        self.application().view.focus_view("Detail/DeviceChain")  
        self.song().view.select_device(device)      
        
    def select_next_hash_device(self, track_id):

        # iterate through devices and tracks until the next device that startswith '#'        
        max = len(self.song().tracks)
        for i in range(track_id, max):
            track = self._parent._song_helper.get_track(i)
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
        