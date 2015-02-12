from YaasController import *

class DeviceController (YaasController):
	__module__ = __name__
	__doc__ = "Control everything that can happen with or inside a device"

	def __init__(self, yaas):

		YaasController.__init__(self, yaas)
		self.log.debug("(DeviceController) init")        

	def navigate_device_focus(self, params, value):
		"""
			Selects next or previous device
			0 -> track_index
			1 -> next? True : False
		"""
		self.log.verbose("(DeviceController) navigate_device_focus called")
		track_index = params[0]
		self.log.verbose("(DeviceController) for track " + str(track_index))
		next = params[1]

		selected_track = self.song_helper().get_selected_track()
		target_track = self.song_helper().get_track(track_index)
		self.log.debug('target ' + target_track.get_name() + ', selected ' + selected_track.get_name())

		# ensures there is an active device
		device = self.device_helper().get_currently_selected_device(track_index)
		if device is None:
			device = target_track.get_device_for_id(0)		
		
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

			if device is not None:
				self.song().view.select_device(device)

	def toggle_device(self, params, value):
		"""
			Switches defined device on/off
			0 -> track_index
			1 -> device_index
		"""

		track_index = params[0]
		device_index = params[1]
		
		if track_index == CURRENT:
			track_index = self.song_helper().get_selected_track().get_track_index()
		
		if device_index == CURRENT:
			device = self.device_helper().get_currently_selected_device(track_index)
		else:
			device = self.song_helper().get_track(track_index).get_device_for_id(device_index)
			
		self.application().view.focus_view("Detail/DeviceChain") 
			
		if device.parameters[0].value == 0.0:

			device.parameters[0].value = 1.0
			self.log.debug("toogle " + device.name + " on")

		else:
			device.parameters[0].value = 0.0
			self.log.debug("toogle " + device.name + " off")
			
	def trigger_device_chain(self, params, value):
		"""
			Use the current active hash device and if it is a rack
			switch the chain with the given index
			
			exclusive means only one chain is not muted
			inclusive means the selected chain gets switched

			0 -> chain_index
			1 -> True means Exclusive / False means Inclusive
		"""
		self.log.verbose("(DeviceController) trigger_device_chain called")
		chain_index = params[0]
		exclusive = params[1]
		self.log.verbose("(DeviceController) for chain " + str(chain_index) + ", exclusive: " + str(exclusive))
		
		device = self.device_helper().get_hash_device()
		
		if device is not None:
			
			if exclusive:
				if len(device.chains) > chain_index:
					
					#self.log.debug("Trigger chain " + str(chain_index + 1) + " with " + str(len(device.chains)) + " chains")				
					if device.chains[chain_index].mute == True:
						self.log.debug("was muted")
						for index in range(len(device.chains)):
						
							if index == chain_index:
								device.chains[index].mute = False
							else:		   
								device.chains[index].mute = True
					else:
						self.log.debug("was not muted")
						device.chains[chain_index].mute = True
						device.chains[0].mute = False
			else:
				if len(device.chains) > chain_index:
					
					self.log.debug("Trigger chain " + str(chain_index + 1) + " with " + str(len(device.chains)) + " chains")
					
					if device.chains[chain_id].mute == True:
						device.chains[chain_id].mute = False
					else:		   
						device.chains[chain_id].mute = True
						
	def set_chain_selector(self, params, value):
		"""
			Use the current active hash device and if it is a rack
			select the chain with the given index
			Save the values from device knobs 1-4
			0 -> chain_index
		"""
		self.log.verbose("(DeviceController) set_chain_selector called")
		chain_index = params[0]
		self.log.verbose("(DeviceController) for chain " + str(chain_index))
		
		device = self.device_helper().get_hash_device()
		
		if device is not None:
			
			# find chain parameter
			chain_parameter = None
			if device.parameters[9].is_enabled == True:
				self.log.verbose('the chain selector is not bound to a control')
				chain_parameter = device.parameters[9]
			else:
				for i in range(len(device.parameters)):
					if device.parameters[i].name == "Chain Selector" and device.parameters[i].is_enabled:
						chain_parameter = device.parameters[i]
						self.log.verbose('the chain selector is parameter ' + str(i) )
			
			# store old values
			chain_name = device.name + '_' + str(int(chain_parameter.value)) + '_'
			self.log.verbose('chain_name: ' + str(chain_name))
			self.yaas._value_container.set_value(chain_name + device.parameters[1].name, device.parameters[1].value)
			self.yaas._value_container.set_value(chain_name + device.parameters[2].name, device.parameters[2].value)
			self.yaas._value_container.set_value(chain_name + device.parameters[3].name, device.parameters[3].value)
			self.yaas._value_container.set_value(chain_name + device.parameters[4].name, device.parameters[4].value)							
			
			debug_message = 'set chain activator to ' + str(chain_index + 1) + ' from ' + str(len(device.chains)) + ' for ' + device.name
			self.log.debug(str(debug_message))
			
			if len(device.chains) > chain_index:
				# set selector
				value = chain_index
				#self.log.debug("max " + str(chain_parameter.max))
				#self.log.debug("min " + str(chain_parameter.min))
				#if CHAIN_MODE_SHORTENED:
				#	value = 127 / 7 * value
				#self.log.debug("new value " + str(value))
				chain_parameter.value = value
				
				#self.log.debug("done for " + chain_parameter.name)
							
				# restore values of first four parameters
				# only if new chain is not 0 (=normal)
				if (chain_index > 0):
					chain_name = device.name + '_' + str(chain_index) + '_'
					if self.yaas._value_container.has_value(chain_name + device.parameters[1].name):
						device.parameters[1].value = self.yaas._value_container.get_single_value(chain_name + device.parameters[1].name)
					if self.yaas._value_container.has_value(chain_name + device.parameters[2].name):
						device.parameters[2].value = self.yaas._value_container.get_single_value(chain_name + device.parameters[2].name)
					if self.yaas._value_container.has_value(chain_name + device.parameters[3].name):
						device.parameters[3].value = self.yaas._value_container.get_single_value(chain_name + device.parameters[3].name)
					if self.yaas._value_container.has_value(chain_name + device.parameters[4].name):
						device.parameters[4].value = self.yaas._value_container.get_single_value(chain_name + device.parameters[4].name)
		else:
			self.log.verbose('hash device was none')
			
	def select_current_then_select_next_hash_device(self, params, value):
		""" 
			First call select first device that starts with '#'
			If the name of the appointed device starts with '#' find a new '#'-device
			Store this device - from now on the first call selects this one			 
			0 -> track_index to start search from
		"""
		self.log.verbose("(DeviceController) set_chain_selector called")
		track_index = params[0]
		self.log.verbose("(DeviceController) for chain " + str(track_index))
		
		
		self.device_helper().select_current_then_select_next_hash_device(track_index)
