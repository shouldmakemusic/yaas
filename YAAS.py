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
# This software contains code with
# Copyright (C) 2007 Nathan Ramella (nar@remix.net)
# Copyright (C) 2007 Rob King (rob@re-mu.org)
# When i used the hole files the copyright is at the top but some parts
# are integrated in this class
#
# For questions regarding this module contact
# Manuel Hirschauer <manuel@hirschauer.net> 
"""
	Main controller script
"""
from __future__ import with_statement

import Live # This allows us (and the Framework methods) to use the Live API on occasion
import time, sys, inspect, os, traceback 

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
from config.Configuration import Configuration

""" Helper classes """
from helper.DeviceHelper import DeviceHelper
from helper.SceneHelper import SceneHelper
from helper.SongHelper import SongHelper
from helper.ViewHelper import ViewHelper
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

# Logger
from util.Logger import Logger

""" Framework classes """
from _Framework.ControlSurface import ControlSurface # Central base class for scripts based on the new Framework
from _Framework.MixerComponent import MixerComponent # Class encompassing several channel strips to form a mixer
from _Framework.SessionComponent import SessionComponent # Class encompassing several scene to cover a defined section of Live's session

""" Here we define some global variables """
# TODO: make them class variables
session = None #Global session object - global so that we can manipulate the same session object from within any of our methods
mixer = None #Global mixer object - global so that we can manipulate the same mixer object from within any of our methods
track = None

# these are for session and mixer handling
sceneindex = None
track_index = 0

class YAAS(ControlSurface):
	__module__ = __name__
	__doc__ = " yet another ableton controller script "
	
	midi_note_definitions_for_lighthouse = {}
	midi_note_definitions = {}
	midi_note_off_definitions = {}
	midi_cc_definitions = {}
	follow_up_events = {}
	
	oscReceiver = 0
	last_midi_note = None
	
	def __init__(self, c_instance):

		self._YAAS__main_script = c_instance
		self._YAAS__main_parent = self
		self._c_instance = c_instance
		self.__c_instance = c_instance
						
		# Logger
		self.log = Logger(self)
		self.log.info(time.strftime("%d.%m.%Y %H:%M:%S", time.localtime()) + "--------------= YAAS log opened =--------------") # Writes message into Live's main log file. This is a ControlSurface method.
				
		# Configuration	
		self.config = Configuration(self)
		self.log.info('Configuration loaded')		
		self.init_midi_config()

		# this enables the function from LiveOSC
		self._LIVEOSC = LiveOSC(c_instance)
		
		# setting up the YAAS OSC Server
		self.oscReceiver = 0
		
		try:
			osc_receive = self.config.get_osc_receive()
			self.log.verbose('(YAAS) osc_receive: ' + str(osc_receive))
			if osc_receive:
				incoming_port = self.config.get_yaas_port()
			else:
				incoming_port = None
			outgoing_port = self.config.get_lighthouse_port()
			
			self.oscServer = OSCServer('localhost', outgoing_port, None, incoming_port)		
			self.oscServer.sendOSC('/osc/yaasserver/startup', 'successfull')
			self.log.info('Opened OSC Server for YAAS with incoming port ' + str(incoming_port) + ' and outgoing port ' + str(outgoing_port) + ' (lighthouse)')
		except Exception, err:
			self.log.error("Could not setup lighthouse osc recevier (song not found)")
			return
		
		# here i will handle midi messages from LightHouse
		self._lighthouse_receiver = LightHouseMidiReceiver(self, c_instance)
		
		ControlSurface.__init__(self, c_instance)

		with self.component_guard():
			
			self._setup_mixer_control() # Setup the mixer object
			self._setup_session_control()  # Setup the session object
			
			# Initialize the possible helpers
			self._device_helper = DeviceHelper(self)			
			self._scene_helper = SceneHelper(self)			
			self._song_helper = SongHelper(self)			
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
			  
		if self.oscReceiver == 0:
			
			try:
				doc = self.song()
			except Exception, err:
				self.log.error("Could not setup lighthouse osc recevier (song not found)")
				return
			try:
				self.oscReceiver = LightHouseOSCReceiver(self.oscServer, self.log)
				self.oscReceiver.setMainScript(self)
				self.oscReceiver.send_controller_info(None)
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

			
	def send_midi(self, midi_bytes):
		"""
			Use this function to send MIDI events through Live to the _real_ MIDI devices 
			that this script is assigned to.
		"""
		if midi_bytes is not None:
			self.log.debug('(YAAS) send_midi' + str(midi_bytes))
			self._YAAS__main_script.send_midi(midi_bytes)
		
	def refresh_state(self):
		self.log.verbose('(YAAS) refresh')	
		
	def build_midi_map(self, midi_map_handle):
		"""
			New MIDI mappings can only be set when the scripts 'build_midi_map' function
			is invoked by our C instance sibling. Its either invoked when we have requested it
			(see 'request_rebuild_midi_map') or when due to a change in Lives internal state,
			a rebuild is needed.
		"""
		self.log.debug("build_midi_map() called")
		for i in range(127):
			Live.MidiMap.forward_midi_note(self.script_handle(), midi_map_handle, CHANNEL, i)
			Live.MidiMap.forward_midi_cc(self.script_handle(), midi_map_handle, CHANNEL, i)
		for i in range(16):
			try:
				Live.MidiMap.forward_midi_pitchbend(self.script_handle(), midi_map_handle, i)
			except Exception, err:
				self.log.error("channel " + str(i) + "could not be initialized")
	
	def receive_midi(self, midi_bytes):

		self.log.verbose("(Yaas) received midi: " + str(midi_bytes))
		try:
			assert (midi_bytes != None)
			assert isinstance(midi_bytes, tuple)
	
			if (len(midi_bytes) is 3):
				
				message_type = midi_bytes[0]
				midi_note = midi_bytes[1]
				value = midi_bytes[2]
	
				if message_type == MESSAGE_TYPE_MIDI_NOTE_RELEASED:
					
					# definitions from config_midi.py
					if (midi_note in self.midi_note_off_definitions):					
						self.handle_parametered_function(self.midi_note_off_definitions, midi_note, value, midi_bytes);
	
					else:
						self.log.verbose("For the control surface (note off): " + str(midi_bytes))
						ControlSurface.receive_midi(self, midi_bytes)
	
				elif message_type == MESSAGE_TYPE_MIDI_NOTE_PRESSED:
					
					self.log.debug("Received Midi Note: " + str(midi_note))
					self.last_midi_note = midi_note
					
					if (midi_note in self.midi_note_definitions):					
						self.handle_parametered_function(self.midi_note_definitions, midi_note, value, midi_bytes);
	
					else:
						self.log.verbose("For the control surface: " + str(midi_bytes))
						ControlSurface.receive_midi(self, midi_bytes)
						
				elif message_type == MESSAGE_TYPE_MIDI_CC:
					
					self.log.verbose("Received Midi CC: " + str(midi_note))
					
					if (midi_note in self.midi_cc_definitions):					
						self.handle_parametered_function(self.midi_cc_definitions, midi_note, value, midi_bytes);
					
					else:
						self.log.debug("CC for the control surface: " + str(midi_bytes))
						ControlSurface.receive_midi(self, midi_bytes)				
				
				elif message_type == MESSAGE_TYPE_LIGHTHOUSE_MIDI_NOTE_PRESSED:					
					self._lighthouse_receiver.receive_midi(midi_bytes)
					
				elif message_type == MESSAGE_TYPE_LIGHTHOUSE_MIDI_NOTE_RELEASED:					
					self._lighthouse_receiver.receive_midi(midi_bytes)
					
				elif message_type in self.follow_up_events.keys():
					midi_note = self.follow_up_events[message_type]
					self.log.verbose("Received follow up event for " + str(midi_note))
					self.handle_parametered_function(self.midi_note_definitions, midi_note, value, midi_bytes);
					
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
		
	def handle_parametered_function(self, definitions, button, value, midi_bytes):
		
		function_and_param = definitions[button]
		name = function_and_param[0]
		method =  function_and_param[1]
		param =  function_and_param[2]

		found = False
		try:
			controller = self.get_controller(name)
			#self.log.verbose(str(controller))

			if (hasattr(controller, method)):
				found = True
				self.log.debug("(YAAS) Calling " + name + "." + method)
				show_light = getattr(controller, method)(param, value)
				self.log.verbose("(YAAS) Lights " + str(show_light))
				if show_light is not None:
					if show_light is False:
						midi_bytes = list(midi_bytes)
						midi_bytes[2] = 0
					self.send_midi(tuple(midi_bytes))
	
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
				self.log.error("(YAAS) get_controller problem: " + str(err))
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

		global session #We want to instantiate the global session as a SessionComponent object (it was a global "None" type up until now...)
		global sceneindex

		if self.config.red_frame_visible():
			is_momentary = True
			num_tracks = self.config.red_frame_width()
			num_scenes = self.config.red_frame_height()
			session = SessionComponent(num_tracks, num_scenes) #(num_tracks, num_scenes) A session highlight ("red box") will appear with any two non-zero values
			self.set_highlighting_session_component(session)
			session.set_offsets(0, 0) #(track_offset, scene_offset) Sets the initial offset of the "red box" from top left
	
			sceneindex = 0;
	
			session.set_mixer(mixer) #Bind the mixer to the session so that they move together

	def _on_selected_track_changed(self):

		global track_index
		global session
		
		selected_track = self.song().view.selected_track #this is how to get the currently selected track, using the Live API
		all_tracks = self._song_helper.get_all_tracks() #this is from the MixerComponent's _next_track_value method
		track_index = list(all_tracks).index(selected_track) #and so is this
		self.log.debug("(YAAS) Track " + str(track_index) + " selected (Scene " + str(sceneindex) + " still active)")

		if self.config.red_frame_visible():
			mixer.channel_strip(0).set_track(selected_track)
			session.set_offsets(track_index, session._scene_offset) #(track_offset, scene_offset); we leave scene_offset unchanged, but set track_offset to the selected track. This allows us to jump the red box to the selected track.		

	def _on_selected_scene_changed(self):

		global scene
		global sceneindex

		selected_scene = self.song().view.selected_scene #this is how we get the currently selected scene, using the Live API
		all_scenes = self.song().scenes #then get all of the scenes
		sceneindex = list(all_scenes).index(selected_scene) #then identify where the selected scene sits in relation to the full list
		self.log.debug("(YAAS) Scene " + str(sceneindex) + " selected")

		if self.config.red_frame_visible():
			if not self.config.red_frame_fixed_on_top():
				self.log.verbose("(Yaas) scene_offset: " + str(session._scene_offset))
				session.set_offsets(track_index, sceneindex)
				self.log.verbose("(Yaas) scene_offset: " + str(session._scene_offset))
		
	def init_midi_config(self):
		
		self.midi_note_definitions = self.config.get_midi_note_definitions()		
		self.follow_up_events = {}
		for k, v in self.midi_note_definitions.iteritems():
			if len(v) == 4:
				#self.log.verbose("(Yaas) found follow up note " + str(v[3]))
				key = v[3][0]
				self.follow_up_events[key] = k
		self.log.verbose("(Yaas) follow up events: " + str(self.follow_up_events))
			
		self.midi_note_off_definitions = self.config.get_midi_note_off_definitions()
		self.midi_cc_definitions = self.config.get_midi_cc_definitions()
		
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
	
	def can_lock_to_devices(self):
		return False

