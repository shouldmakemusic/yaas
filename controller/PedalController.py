from YaasController import *

looper_last_track_index = 0
_parameter_names_for_device_in_set = {}

class PedalController(YaasController):
    __module__ = __name__
    __doc__ = 'PedalController handles Pedal actions'
    
    def __init__(self, yaas):

        YaasController.__init__(self, yaas)
        self.log.debug("(PedalController) init")     
    
    def handle_send(self, params, value):
        
        track_id = params[0]
        send_id = params[1]
        
        track_helper = self.song_helper().get_track(track_id)
        
        new_value = self.get_normalized_value_from_target(track_helper.get_track().mixer_device.sends[send_id], value)        
        #self.log.debug("set send " + str(send_id) + " for track " + str(track_id) + " to value " + str(new_value))
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
        #self.log.debug("new value " + str(new_value))    
        return new_value
    
    def handle_volume(self, params, value):
        
        track_id = params[0]        
        track_helper = self.song_helper().get_track(track_id)
        #self.log.debug("Volume note code " + str(value) + " and value " + str(midi_bytes[2]))
        # value is between 0 and 127 - for volume the wanted max value is 0.85
        value = (0.85 * value) / 128.0
        selected_track = track_helper.get_track()
        selected_track.mixer_device.volume.value = value

    def handle_effect_slider(self, params, value):
        
        track_id = params[0]
        parameter_id = params[1]
        global _parameter_names_for_device_in_set
        
        device = self.device_helper().get_hash_device()
                    
        if device is not None:
            
            set_name = 'default'
            name = set_name + '_' + device.name
            parameter = device.parameters[parameter_id]
            
            if not(name in _parameter_names_for_device_in_set.keys()):
                parameter_names = {}
                for index in range(len(device.parameters)):
                    parameter_name = device.parameters[index].name
                    parameter_names[parameter_name] = index
                    self.log.verbose("added param " + parameter_name + " with index " + str(index))
                    
                _parameter_names_for_device_in_set[name] = parameter_names
                self.log.debug("stored parameters for " + name)

            min = parameter.min
            max = parameter.max
            
            max_name = "Max " + parameter.name
            self.log.verbose("max name " + max_name)
            if max_name in _parameter_names_for_device_in_set[name]:
                #self.log.debug("found")
                index = _parameter_names_for_device_in_set[name][max_name]
                #self.log.debug("index " + str(index))
                max = device.parameters[index].value + 1
            #self.log.debug("max value " + str(max))
                
            value = self.get_normalized_value(min, max, value)    
            parameter.value = value
                