from __future__ import with_statement
import Live

from consts import *
from _Framework.ControlSurfaceComponent import ControlSurfaceComponent
from TrackHelper import TrackHelper

looper_last_track_index = 0
_parameter_names_for_device_in_set = {}

class PedalHelper(ControlSurfaceComponent):
    __module__ = __name__
    __doc__ = 'PedalHelper handles Pedal actions'
    
    def __init__(self, parent):
        ControlSurfaceComponent.__init__(self)
        self._parent = parent
    
    def song(self):
        return self._parent.song()
    
    def log_message(self, message):
        self._parent.log_message(message)
    
    def disconnect(self):
        self._parent = None
        if IS_LIVE_9:
            ControlSurfaceComponent.disconnect(self)                
    
    def on_enabled_changed(self):
        pass

    def update(self):    
        pass
    
    def handle_send(self, params, value):
        
        track_id = params[0]
        send_id = params[1]
        
        track_helper = self._parent._song_helper.get_track(track_id)
        
        new_value = self.get_normalized_value_from_target(track_helper.get_track().mixer_device.sends[send_id], value)        
        #self.log_message("set send " + str(send_id) + " for track " + str(track_id) + " to value " + str(new_value))
        track_helper.set_send_value(send_id, new_value)
        
    def get_normalized_value_from_target(self, target, value):
        '''
            Takes min and max from target and returns get_normalized_value
            The target could be e.g. a DeviceParameter like send (has to have the properties .min and .max) 
        '''
        min = target.min
        max = target.max    
        return self.get_normalized_value(min, max, value)

    def get_normalized_value(self, min, max, value):
        '''
            Returns a normalized value.
            ((max + min) * value / 128) - min
        '''
        new_value = ((max + min) * value / 128.0) - min
        #self.log_message("new value " + str(new_value))    
        return new_value
    
    def handle_volume(self, params, value):
        
        track_id = params[0]        
        track_helper = self._parent._song_helper.get_track(track_id)
        #self.log_message("Volume note code " + str(value) + " and value " + str(midi_bytes[2]))
        # value is between 0 and 127 - for volume the wanted max value is 0.85
        value = (0.85 * value) / 128.0
        selected_track = track_helper.get_track()
        selected_track.mixer_device.volume.value = value

    def handle_effect_slider(self, params, value):
        
        track_id = params[0]
        parameter_id = params[1]
        global _parameter_names_for_device_in_set
        
        device = self._parent._device_helper.get_hash_device()
                    
        if device is not None:
            
            set_name = 'default'
            name = set_name + '_' + device.name
            parameter = device.parameters[parameter_id]
            
            if not(name in _parameter_names_for_device_in_set.keys()):
                parameter_names = {}
                for index in range(len(device.parameters)):
                    parameter_name = device.parameters[index].name
                    parameter_names[parameter_name] = index
                    #self._parent.log_message("added param " + parameter_name + " with index " + str(index))
                    
                _parameter_names_for_device_in_set[name] = parameter_names
                self._parent.log_message("stored parameters for " + name)

            min = parameter.min
            max = parameter.max
            
            max_name = "Max " + parameter.name
            #self._parent.log_message("max name " + max_name)
            if max_name in _parameter_names_for_device_in_set[name]:
                #self._parent.log_message("found")
                index = _parameter_names_for_device_in_set[name][max_name]
                #self._parent.log_message("index " + str(index))
                max = device.parameters[index].value + 1
            #self._parent.log_message("max value " + str(max))
                
            value = self.get_normalized_value(min, max, value)    
            parameter.value = value
            #save_name = name + '_' + parameter.name
            #self._parent._value_container.set_value(save_name, value)
                