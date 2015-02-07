from __future__ import with_statement

import Live # This allows us (and the Framework methods) to use the Live API on occasion
import time # We will be using time functions for time-stamping our log file outputs
import sys
import inspect
import os

from controller.RedFrameController import RedFrameController
from controller.TrackController import TrackController

""" Constants and configuration """
from consts import *
from config_midi import *

""" These handle the tasks """
from SongHelper import SongHelper
from LooperHelper import LooperHelper
from PedalHelper import PedalHelper
from DeviceHelper import DeviceHelper
from ValueContainer import ValueContainer
from LightHouseMidiReceiver import LightHouseMidiReceiver

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
scene = None
track = None
#button_play_current_scene = None
sceneindex = None

track_index = 0
track_volume_element = None
mixer_controller = None


looper_start_time = None
looper_last_track_index = None

class YAAS(ControlSurface):
	__module__ = __name__
	__doc__ = " yet another ableton controller script "

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

		# here i will handle midi messages from LightHouse
		self._lighthouse_receiver = LightHouseMidiReceiver(self, c_instance)
		
		ControlSurface.__init__(self, c_instance)

		with self.component_guard():
			self._setup_mixer_control() # Setup the mixer object
			self._setup_session_control()  # Setup the session object
			
			self._song_helper = SongHelper(self)
			
			self._pedal_helper = PedalHelper(self)
			
			self._device_helper = DeviceHelper(self)
			self.device_helper = self._device_helper
			
			self._looper_helper = LooperHelper(self)

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
		
		#Live.MidiMap.forward_midi_note(self.script_handle(), midi_map_handle, 0, 0)
		#Live.MidiMap.forward_midi_note(self.script_handle(), midi_map_handle, CHANNEL, 1)
		#Live.MidiMap.forward_midi_note(self.script_handle(), midi_map_handle, CHANNEL, 6)
		for index in range(len(rec_all_notes)):
			Live.MidiMap.forward_midi_note(self.script_handle(), midi_map_handle, CHANNEL, rec_all_notes[index])

		for index in range(len(click_notes)):
			Live.MidiMap.forward_midi_note(self.script_handle(), midi_map_handle, CHANNEL, click_notes[index])

		for index in range(len(tap_tempo_notes)):
			Live.MidiMap.forward_midi_note(self.script_handle(), midi_map_handle, CHANNEL, tap_tempo_notes[index])

		#select track
		for index in range(len(select_track_notes)):
			Live.MidiMap.forward_midi_note(self.script_handle(), midi_map_handle, CHANNEL, select_track_notes[index])


		#move red box
		for index in range(len(select_box_right)):
			Live.MidiMap.forward_midi_note(self.script_handle(), midi_map_handle, CHANNEL, select_box_right[index])
		for index in range(len(select_box_left)):
			Live.MidiMap.forward_midi_note(self.script_handle(), midi_map_handle, CHANNEL, select_box_left[index])
		for index in range(len(select_box_down)):
			Live.MidiMap.forward_midi_note(self.script_handle(), midi_map_handle, CHANNEL, select_box_down[index])
		for index in range(len(select_box_up)):
			Live.MidiMap.forward_midi_note(self.script_handle(), midi_map_handle, CHANNEL, select_box_up[index])

		#scene
		for index in range(len(scene_down)):
			Live.MidiMap.forward_midi_note(self.script_handle(), midi_map_handle, CHANNEL, scene_down[index])
		for index in range(len(scene_up)):
			Live.MidiMap.forward_midi_note(self.script_handle(), midi_map_handle, CHANNEL, scene_up[index])
		Live.MidiMap.forward_midi_note(self.script_handle(), midi_map_handle, CHANNEL, stop_all_clips)
		Live.MidiMap.forward_midi_note(self.script_handle(), midi_map_handle, CHANNEL, play_current_scene)
				
		# midi_note_definitions
		for k, v in midi_note_definitions.iteritems():
			self.log.verbose('registered midi note ' + str(k))
			Live.MidiMap.forward_midi_note(self.script_handle(), midi_map_handle, CHANNEL, k)
			
		# midi_cc_definitions
		for k, v in midi_cc_definitions.iteritems():
			self.log.verbose('registered midi cc ' + str(k))
			Live.MidiMap.forward_midi_cc(self.script_handle(), midi_map_handle, CHANNEL, k)
			
	def receive_midi(self, midi_bytes):

		#self.log.debug(str(midi_bytes))
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
					
					if (midi_note == 70):
						self.log.debug("Looper test");
						self.log.debug("Selected Track Index: " + str(self._song_helper.get_selected_track().get_track_index()))
						track_helper = self._song_helper.get_selected_track()
						looper = track_helper.get_device(LOOPER)
						self._device_helper.log_parameters_for_device(looper)
												
					elif (midi_note in select_track_notes):
						self.selectTrack(track_id)
										
					elif (midi_note in rec_all_notes):
						self.recAll(track_id)
						
					elif (midi_note in tap_tempo_notes):
						self.song().tap_tempo()
	
					# move red box
					elif (midi_note in select_box_right):
						self.move_track_view_horizontal(True)
					elif (midi_note in select_box_left):
						self.move_track_view_horizontal(False)
					elif (midi_note in select_box_down):
						self.move_track_view_vertical(True);
					elif (midi_note in select_box_up):
						self.move_track_view_vertical(False);
					# move scene
					elif (midi_note in scene_down):
						self.move_scene_view_vertical(True);
					elif (midi_note in scene_up):
						self.move_scene_view_vertical(False);
	
					# device helper
					elif (midi_note in midi_note_definitions):					
						self.handle_parametered_function(midi_note_definitions, midi_note, value);
					
					# metronome
					elif (midi_note in click_notes):
						if (self.song().metronome):
							self.song().metronome = OFF
						else:
							self.song().metronome = ON
							
	
					elif midi_note == stop_all_clips:
						self.song().stop_all_clips()
	
					elif midi_note == play_current_scene:
						self.song().view.selected_scene.fire_as_selected()
	
					else:
						self.log.debug("For the control surface: " + str(midi_bytes))
						ControlSurface.receive_midi(self, midi_bytes)
						
				elif (message_type == MESSAGE_TYPE_MIDI_CC):
					
					#self.log.debug("Received Midi CC: " + str(midi_note))
					
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
			#self.set_suppress_rebuild_requests(False)	
				
		except Exception, err:
			self.log.error("(YAAS) receive_midi")
			self.log.error("Could not execute midi " + str(midi_bytes))
			self.log.error("Because of " + str(err))

	def recAll(self, track_index):
		
		current_song_time = 0
		if (self.song().is_playing):
			current_song_time = self.song().current_song_time
			#self.song().stop_playing()

		if (self.song().record_mode == 0):
			self.log.info("Start recording from " + str(current_song_time));
			self.song().set_or_delete_cue()
			self.song().record_mode = 1
		else:
			self.song().record_mode = 0		
		#self.song().current_song_time = current_song_time
		#self.song().continue_playing()
		
	def selectTrack(self, track_index):
		
		track = self.song().tracks[track_index]
		#all_tracks = self._song_helper.get_all_tracks() #this is from the MixerComponent's _next_track_value method
		#self.song().view.selected_track = all_tracks[track_index]
		
		self.song().view.selected_track = track
		self.application().view.focus_view("Detail") 
		self.application().view.focus_view("Detail/DeviceChain") 
		
		#self.log.debug("arrayActiveDevices removed ")

		
#	def stopClip(self, track_index):
#		self.log.debug("stop clip " + str(track_index))
#		self.song().view.selected_track.stop_all_clips();
		
			
	def handle_parametered_function(self, definitions, button, value):
		
		function_and_param = definitions[button]
		helper_name = function_and_param[0]
		method =  function_and_param[1]
		param =  function_and_param[2]
		
		helper = self.get_helper(helper_name)
		try:
			getattr(helper, method)(param, value)
		except Exception, err:
			self.log.error(err)

		controller = self.get_controller(helper_name)
		getattr(controller, method)(param, value)
			
	def get_controller(self, name):
		"""
			Returns a controller from dir controller
			For these controllers the event handling is available
			(the methods have to accept params and value as parameters)
		"""
		controller = globals()[name](self)
		self.log.log_object_attributes(controller)
		return controller
		
	def get_helper(self, param):
		
		helper_name = None
		if isinstance(param, list):
			helper_name = param[0]
		else:
			helper_name = param
		
		if helper_name == TRACK_HELPER:
			return self._song_helper.get_track(param[1])
		if helper_name == DEVICE_HELPER:
			return self._device_helper
		if helper_name == LOOPER_HELPER:
			return self._looper_helper
		if helper_name == PEDAL_HELPER:
			return self._pedal_helper

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

		global scene
		global sceneindex
		scene = session.scene(0)
		sceneindex = 0;

		session.set_mixer(mixer) #Bind the mixer to the session so that they move together

	def _on_selected_track_changed(self):

		"""here we set the mixer and session to the selected track, when the selected track changes"""
		selected_track = self.song().view.selected_track #this is how to get the currently selected track, using the Live API
		mixer.channel_strip(0).set_track(selected_track)
		all_tracks = self._song_helper.get_all_tracks() #this is from the MixerComponent's _next_track_value method
		global track_index
		track_index = list(all_tracks).index(selected_track) #and so is this
		self.log.debug("Track " + str(track_index) + " selected (Scene " + str(sceneindex) + " still active)")

		global session
		session.set_offsets(track_index, session._scene_offset) #(track_offset, scene_offset); we leave scene_offset unchanged, but set track_offset to the selected track. This allows us to jump the red box to the selected track.		

	def _on_selected_scene_changed(self):

		global scene
		global sceneindex

		"""Here we set the mixer and session to the selected track, when the selected track changes"""
		selected_scene = self.song().view.selected_scene #this is how we get the currently selected scene, using the Live API
		all_scenes = self.song().scenes #then get all of the scenes
		sceneindex = list(all_scenes).index(selected_scene) #then identify where the selected scene sits in relation to the full list
		self.log.debug("Scene " + str(sceneindex+1) + " selected")
		
	def move_track_view_vertical(self, down):
		if down:
			self.log.debug("track view down")
			scene_offset = session._scene_offset + 1
			session.set_offsets(session._track_offset, scene_offset) #(track_offset, scene_offset) Sets the initial offset of the "red box" from top left
			self.song().view.selected_scene = self.song().scenes[scene_offset]

		else:
			self.log.debug("track view up")
			scene_offset = session._scene_offset - 1
			if scene_offset < 0:
				scene_offset = 0
			session.set_offsets(session._track_offset, scene_offset) #(track_offset, scene_offset) Sets the initial offset of the "red box" from top left
			self.song().view.selected_scene = self.song().scenes[scene_offset]

	def move_track_view_horizontal(self, down):
		if down:
			self.log.debug("track view right")
			track_offset = session._track_offset + 1
			session.set_offsets(track_offset, session._scene_offset) #(track_offset, scene_offset) Sets the initial offset of the "red box" from top left
			self.song().view.selected_track = self.song().tracks[track_offset]

		else:
			self.log.debug("track view left")
			track_offset = session._track_offset - 1
			if track_offset < 0:
				track_offset = 0
			session.set_offsets(track_offset, session._scene_offset) #(track_offset, scene_offset) Sets the initial offset of the "red box" from top left
			self.song().view.selected_track = self.song().tracks[track_offset]
			
	def move_scene_view_vertical(self, down):
				
		global sceneindex
		global scene
				
		if down:
			self.log.debug("scene view down")
			sceneindex = sceneindex + 1
			self.song().view.selected_scene = self.song().scenes[sceneindex]

		else:
			if sceneindex == 0:
				return
			self.log.debug("scene view up")
			sceneindex = sceneindex - 1
			self.song().view.selected_scene = self.song().scenes[sceneindex]
			
	def get_session(self):
		return session

	def disconnect(self):
		"""clean things up on disconnect"""
		self.log.info(time.strftime("%d.%m.%Y %H:%M:%S", time.localtime()) + "--------------= YAAS log closed =--------------") #Create entry in log file
		ControlSurface.disconnect(self)
		self._YAAS__main_script = None
		return None
		return self._YAAS__main_script.handle()

	def script_handle(self):
		return self._YAAS__main_script.handle()
