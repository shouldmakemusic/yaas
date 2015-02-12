from __future__ import with_statement

import Live # This allows us (and the Framework methods) to use the Live API on occasion
import time # We will be using time functions for time-stamping our log file outputs
import sys
import inspect
import os
import traceback
#import marshal <- this would be for saving the config in .conf files instead of .py

""" These handle the tasks """
from LightHouseMidiReceiver import LightHouseMidiReceiver
from controller.DebugController import DebugController
from controller.DeviceController import DeviceController
from controller.LooperController import LooperController
from controller.PedalController import PedalController
from controller.RedFrameController import RedFrameController
from controller.SceneController import SceneController
from controller.SongController import SongController
from controller.TrackController import TrackController
# add new controllers here!

""" Constants and configuration """
from consts import *
from config_midi import *

""" Helper classes """
from helper.SongHelper import SongHelper
from helper.DeviceHelper import DeviceHelper
from helper.ViewHelper import ViewHelper
from LooperHelper import LooperHelper
from ValueContainer import ValueContainer

""" Classes for LiveOSC """
from LiveOSC.LiveOSCCallbacks import LiveOSCCallbacks

# RemixNet
from LiveOSC.OSCClient import OSCClient
from LiveOSC.OSCServer import OSCServer
from LiveOSC.UDPClient import UDPClient
from LiveOSC.UDPServer import UDPServer

# OSC
from LiveOSC.OSCMessage import OSCMessage
from LiveOSC.CallbackManager import CallbackManager
from LiveOSC.OSCUtils import *
from LiveOSC.LiveUtils import *

# LiveOSC
from LiveOSC.LiveOSC import LiveOSC

# YAAS OSC
from LightHouseOSCReceiver import LightHouseOSCReceiver
from util.Logger import Logger

""" Framework classes """
from _Framework.ControlSurface import ControlSurface # Central base class for scripts based on the new Framework
from _Framework.MixerComponent import MixerComponent # Class encompassing several channel strips to form a mixer
from _Framework.SessionComponent import SessionComponent # Class encompassing several scene to cover a defined section of Live's session

""" Here we define some global variables """
session = None #Global session object - global so that we can manipulate the same session object from within any of our methods
mixer = None #Global mixer object - global so that we can manipulate the same mixer object from within any of our methods
track = None

# these are for session and mixer handling
sceneindex = None
track_index = 0

class YAAS(ControlSurface):
	__module__ = __name__
	__doc__ = " yet another ableton controller script "
	
	midi_note_definitions_from_lighthouse = {}   
	midi_cc_definitions_from_lighthouse = {} 

	def __init__(self, c_instance):

		self._YAAS__main_script = c_instance
		self._YAAS__main_parent = self
		self._c_instance = c_instance
				
		# Logger
		self.log = Logger(self)
		self.log.info(time.strftime("%d.%m.%Y %H:%M:%S", time.localtime()) + "--------------= YAAS log opened =--------------") # Writes message into Live's main log file. This is a ControlSurface method.
		self.log.info('Opened OSC Server for YAAS with incoming port 9190 and outgoing port 9050 (lighthouse)')
			
		# this enables the function from LiveOSC
		self._LIVEOSC = LiveOSC(c_instance)
		
		# setting up the YAAS OSC Server
		self.basicAPI = 0	
		self.oscServer = OSCServer('localhost', 9050, None, 9190)		
		self.oscServer.sendOSC('/yaas/oscserver/startup', 1)
		self.oscServer.sendOSC('/yaas/config/port', 9190);

		# here i will handle midi messages from LightHouse
		self._lighthouse_receiver = LightHouseMidiReceiver(self, c_instance)
		
		ControlSurface.__init__(self, c_instance)

		with self.component_guard():
			
			self._setup_mixer_control() # Setup the mixer object
			self._setup_session_control()  # Setup the session object
			
			# Initialize the possible helpers
			self._song_helper = SongHelper(self)			
			self._device_helper = DeviceHelper(self)			
			self._looper_helper = LooperHelper(self)			
			self._view_helper = ViewHelper(self)

		# store and retrieve values
		self._value_container = ValueContainer(self)
		
		
	def connect_script_instances(self, instanciated_scripts):
		"""
		Called by the Application as soon as all scripts are initialized.
		You can connect yourself to other running scripts here, as we do it
		connect the extension modules
		"""
		self.log.debug('(YAAS) connect_script_instances')
		return

	def update_display(self):
		"""
		This function is run every 100ms, so we use it to initiate our Song.current_song_time
		listener to allow us to process incoming OSC commands as quickly as possible under
		the current listener scheme.
		"""
		# Enable LiveOSC functions
		self._LIVEOSC.update_display()
		
		######################################################
		# START OSC LISTENER SETUP
			  
		if self.basicAPI == 0:
			
			try:
				doc = self.song()
			except Exception, err:
				self.log.error("Could not setup lighthouse osc recevier (song not found)")
				return
			try:
				self.basicAPI = LightHouseOSCReceiver(self.oscServer, self.log)
				self.basicAPI.setMainScript(self)
				self.log.info('LightHouseOSCReceiver running')
			except Exception, err:
				self.log.error("Could not setup lighthouse osc recevier: " + str(err))
				return
			
			# If our OSC server is listening, try processing incoming requests.
			# Any 'play' initiation will trigger the current_song_time listener
			# and bump updates from 100ms to 60ms.
			
		if self.oscServer:
			try:
				self.oscServer.processIncomingUDP()
			except:
				pass
			
		# END OSC LISTENER SETUP
		######################################################

			
	def send_midi(self, midi_event_bytes):
		"""
		Use this function to send MIDI events through Live to the _real_ MIDI devices 
		that this script is assigned to.
		"""
		self.log.debug('(YAAS) send_midi')
		pass
		
	def build_midi_map(self, midi_map_handle):

		self.log.debug("build_midi_map() called")
		ControlSurface.build_midi_map(self, midi_map_handle)
		self._lighthouse_receiver.build_midi_map(midi_map_handle)
						
		# midi_note_definitions
		for k, v in self.midi_note_definitions_from_lighthouse.iteritems():
			self.log.verbose('registered midi note (lighthouse) ' + str(k))
			Live.MidiMap.forward_midi_note(self.script_handle(), midi_map_handle, CHANNEL, k)

		# midi_note_definitions
		for k, v in midi_note_definitions.iteritems():
			if not self.midi_note_definitions_from_lighthouse.has_key(k):
				self.log.verbose('registered midi note ' + str(k))
				Live.MidiMap.forward_midi_note(self.script_handle(), midi_map_handle, CHANNEL, k)
			
		# midi_cc_definitions
		for k, v in midi_cc_definitions.iteritems():
			self.log.verbose('registered midi cc ' + str(k))
			Live.MidiMap.forward_midi_cc(self.script_handle(), midi_map_handle, CHANNEL, k)
			
	def receive_midi(self, midi_bytes):

		self.log.verbose(str(midi_bytes))
		try:
			assert (midi_bytes != None)
			assert isinstance(midi_bytes, tuple)
	
			if (len(midi_bytes) is 3):
				
				message_type = midi_bytes[0]
				midi_note = midi_bytes[1]
				value = midi_bytes[2]
	
				if (message_type == MESSAGE_TYPE_MIDI_NOTE_RELEASED):
					
					#self.log.debug("Button released");
					return
	
				elif (message_type == MESSAGE_TYPE_MIDI_NOTE_PRESSED):
					
					self.log.debug("Received Midi Note: " + str(midi_note))
					
					# bank
					# 1 => 0, 11 => 1, 21 => 2
					track_id = (midi_note//10) - 1
					# hier waere ein mapping besser
					# welche taste
					# 1 => 1, 11 => 1, 12 => 2
					pedalnumber = midi_note%10												
	
					# definitions from lighthouse
					#self.log.verbose(str(self.midi_note_definitions_from_lighthouse))

					if (midi_note in self.midi_note_definitions_from_lighthouse):	
						self.log.debug('Found it in lighthouse definitions')				
						self.handle_parametered_function(self.midi_note_definitions_from_lighthouse, midi_note, value);
					
					# definitions from config_midi.py
					elif (midi_note in midi_note_definitions):					
						self.handle_parametered_function(midi_note_definitions, midi_note, value);
	
					else:
						self.log.debug("For the control surface: " + str(midi_bytes))
						ControlSurface.receive_midi(self, midi_bytes)
						
				elif (message_type == MESSAGE_TYPE_MIDI_CC):
					
					self.log.verbose("Received Midi CC: " + str(midi_note))
					
					if (midi_note in midi_cc_definitions):					
						self.handle_parametered_function(midi_cc_definitions, midi_note, value);
					
					else:
						self.log.debug("CC for the control surface: " + str(midi_bytes))
						ControlSurface.receive_midi(self, midi_bytes)				
				
				elif (message_type == MESSAGE_TYPE_LIGHTHOUSE_MIDI_NOTE_PRESSED):
					
					self._lighthouse_receiver.receive_midi(midi_bytes)
				elif (message_type == MESSAGE_TYPE_LIGHTHOUSE_MIDI_NOTE_RELEASED):
					
					self._lighthouse_receiver.receive_midi(midi_bytes)
				else:
					self.log.debug("Midi for the control surface: " + str(midi_bytes))
					ControlSurface.receive_midi(self, midi_bytes)
	
			else:
				self.log.debug("Different: " + str(midi_bytes))
				self.handle_sysex(midi_bytes)
				ControlSurface.receive_midi(self, midi_bytes)
				
		except Exception, err:
			self.log.error("(YAAS) receive_midi")
			self.log.error("Could not execute midi " + str(midi_bytes))
			self.log.error("Because of " + str(err))
		
	def handle_parametered_function(self, definitions, button, value):
		
		function_and_param = definitions[button]
		name = function_and_param[0]
		method =  function_and_param[1]
		param =  function_and_param[2]

		found = False
		try:
			controller = self.get_controller(name)

			if (hasattr(controller, method)):
				found = True
				self.log.debug("(YAAS) Calling " + name + "." + method)
				getattr(controller, method)(param, value)
	
			if not found:
				self.log.error("(YAAS) Could not find controller for " + name + "." + method)
				
		except Exception, err:
			self.log.error("(YAAS) Error executing " + name + "." + method)
			self.log.error("(YAAS) Message: " + str(err))	
			traceback.print_exc(file=sys.stderr)
	
	controller_dict = {}	
	def get_controller(self, name):
		"""
			Returns a controller from dir controller
			For these controllers the event handling is available
			(the methods have to accept params and value as parameters)
		"""
		if self.controller_dict.has_key(name):
			#self.log.verbose("return existing controller " + name)
			return self.controller_dict[name]
		
		controller = None
		if isinstance(name, basestring):
			try:
				controller = globals()[name](self)
			except Exception, err:
				self.log.verbose("(YAAS) get_controller problem: " + str(err))
		if controller is not None:
			self.log.log_object_attributes(controller)
			self.controller_dict[name] = controller
		return controller
		
	def _setup_mixer_control(self):

		is_momentary = True
		num_tracks = 7 #A mixer is one-dimensional; here we define the width in tracks - seven columns, which we will map to seven "white" notes
		"""Here we set up the global mixer""" #Note that it is possible to have more than one mixer...
		global mixer #We want to instantiate the global mixer as a MixerComponent object (it was a global "None" type up until now...)
		mixer = MixerComponent(num_tracks, 2, with_eqs=True, with_filters=True) #(num_tracks, num_returns, with_eqs, with_filters)
		mixer.set_track_offset(0) #Sets start point for mixer strip (offset from left)
		self.song().view.selected_track = mixer.channel_strip(0)._track #set the selected strip to the first track, so that we don't, for example, try to assign a button to arm the master track, which would cause an assertion error

	def _setup_session_control(self):

		is_momentary = True
		num_tracks = 1 #single column
		num_scenes = 7 #seven rows, which will be mapped to seven "white" notes
		global session #We want to instantiate the global session as a SessionComponent object (it was a global "None" type up until now...)
		session = SessionComponent(num_tracks, num_scenes) #(num_tracks, num_scenes) A session highlight ("red box") will appear with any two non-zero values
		self.set_highlighting_session_component(session)
		session.set_offsets(0, 0) #(track_offset, scene_offset) Sets the initial offset of the "red box" from top left

		global sceneindex
		sceneindex = 0;

		session.set_mixer(mixer) #Bind the mixer to the session so that they move together

	def _on_selected_track_changed(self):

		"""here we set the mixer and session to the selected track, when the selected track changes"""
		selected_track = self.song().view.selected_track #this is how to get the currently selected track, using the Live API
		mixer.channel_strip(0).set_track(selected_track)
		all_tracks = self._song_helper.get_all_tracks() #this is from the MixerComponent's _next_track_value method
		global track_index
		track_index = list(all_tracks).index(selected_track) #and so is this
		self.log.debug("(YAAS) Track " + str(track_index) + " selected (Scene " + str(sceneindex) + " still active)")

		global session
		session.set_offsets(track_index, session._scene_offset) #(track_offset, scene_offset); we leave scene_offset unchanged, but set track_offset to the selected track. This allows us to jump the red box to the selected track.		

	def _on_selected_scene_changed(self):

		global scene
		global sceneindex

		"""Here we set the mixer and session to the selected track, when the selected track changes"""
		selected_scene = self.song().view.selected_scene #this is how we get the currently selected scene, using the Live API
		all_scenes = self.song().scenes #then get all of the scenes
		sceneindex = list(all_scenes).index(selected_scene) #then identify where the selected scene sits in relation to the full list
		self.log.debug("(YAAS) Scene " + str(sceneindex+1) + " selected")

# Connections to ligthhouse	
	def send_available_methods_to_lighthouse(self):
		"""
			All controllers and their commands will send to lighthouse (OSC)			
		"""
		self.log.verbose("(YAAS) send_available_methods_to_lighthouse called")
		self.oscServer.sendOSC('/yaas/commands/clear', 1)
		g = globals().copy()		
		for name, obj in g.iteritems():
			
			if "Controller" in str(name):				
				self.log.verbose("Name: " + name)				
				for attr in dir(obj):				
					method_desc = getattr(obj, attr)
										
					if "method" in str(method_desc):						
						self.log.verbose( "obj.%s = %s" % (attr, method_desc))
						
						if hasattr(method_desc, 'func_code'):
							params = method_desc.func_code.co_varnames
							#for i in range(method_desc.func_code.co_argcount):
								#self.log.verbose("param: " + params[i])
							
							if hasattr(method_desc, 'func_code'):
								if method_desc.func_code.co_argcount == 3:
									#self.log.verbose("criteria 1")
									if params[0] == "self":
										#self.log.verbose("criteria 2")
										if params[1] == "params":
											#self.log.verbose("criteria 3")
											if params[2] == "value":
												#self.log.verbose("criteria 4")
												self.oscServer.sendOSC('/yaas/commands/list', [name, attr])
		self.oscServer.sendOSC('/yaas/commands/done', 1)
		self.log.debug("sent command list to lighthouse")
				

	def get_session(self):
		"""
			Helper method to get the global sesseion	
		"""
		return session
	
	def request_rebuild_midi_map(self):
		"""
			Initiates a call of rebuild_midi_map() through Live
		"""
		self._YAAS__main_script.request_rebuild_midi_map()
	
# Administration methods
	def disconnect(self):
		"""clean things up on disconnect"""
		self.log.info(time.strftime("%d.%m.%Y %H:%M:%S", time.localtime()) + "--------------= YAAS log closed =--------------") #Create entry in log file
		ControlSurface.disconnect(self)
		self._YAAS__main_script = None
		return None
		return self._YAAS__main_script.handle()

	def script_handle(self):
		return self._YAAS__main_script.handle()
