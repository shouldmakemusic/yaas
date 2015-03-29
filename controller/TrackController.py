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
	Control everything that can happen inside a track
"""
from YaasController import *

class TrackController (YaasController):
	"""
		Control everything that can happen inside a track
	"""

	def __init__(self, yaas):

		YaasController.__init__(self, yaas)
		self.log.debug("(TrackController) init")

	def stop_or_restart_clip(self, params, value):
		"""
			If a clip is playing in the given track - stop it and remember it
			
			If this method is called again and no clip is playing - start it again
			
			@param params[0]: track_index
		"""
		self.log.verbose("(TrackController) stop_or_restart_clip called")
		track_index = params[0]
		self.log.verbose("(TrackController) for track " + str(track_index))

		track_helper = self.track_helper(track_index)
		track_helper.stop_or_restart_clip()

	def stop(self, params, value):
		"""
			Stop the clip in the given track
			
			@param params[0]: track_index
		"""

		self.log.verbose("(TrackController) stop called")
		track_index = params[0]
		self.log.verbose("(TrackController) for track " + str(track_index))

		track_helper = self.track_helper(track_index)
		track_helper.get_track().stop_all_clips()
		
	def stop_immediately(self, params, value):
		"""
			Stop the clip in the given track immediately
			
			@param params[0]: track_index
		"""

		self.log.verbose("(TrackController) stop_immediately called")
		track_index = params[0]
		self.log.verbose("(TrackController) for track " + str(track_index))

		track_helper = self.track_helper(track_index)
		clip = track_helper.get_playing_clip()
		if clip is not None:
			clip.muted = True
			clip.muted = False
		
	def arm(self, params, value):
		"""
			Arms the given track or switches it off
			
			@param params[0]: track_index
		"""

		self.log.verbose("(TrackController) arm called")
		track_index = params[0]
		self.log.verbose("(TrackController) for track " + str(track_index))

		track_helper = self.track_helper(track_index)
		track_helper.arm()

	def get_focus(self, params, value):
		"""
			Requests the view focus for the given track
			
			@param params[0]: track_index
		"""

		self.log.verbose("(TrackController) get_focus called")
		track_index = params[0]
		self.log.verbose("(TrackController) for track " + str(track_index))
		
		track = self.track_helper(track_index).get_track()
		self.view_helper().focus_on_track(track)

	def toggle_mute_track(self, params, value):
		"""
			Toggles the muted state for the given track
			
			@param params[0]: track_index
		"""
		if value == 0:
			return

		self.log.verbose("(TrackController) toggleMuteTrack called")
		track_index = params[0]
		self.log.verbose("(TrackController) for track " + str(track_index))
		
		track = self.track_helper(track_index).get_track()
		muted = track.mute
		if muted:
			track.mute = 0
		else:
			track.mute = 1

	def toggle_solo_track(self, params, value):
		"""
			Toggles the soloed state for the given track
			
			@param params[0]: track_index
		"""
		if value == 0:
			return
		
		self.log.verbose("(TrackController) toggle_solo_track called")
		track_index = params[0]
		self.log.verbose("(TrackController) for track " + str(track_index))

		track = self.track_helper(track_index).get_track()
		if track.solo:
			track.solo = 0
			return True
		else:
			track.solo = 1
			return False

	def set_pan(self, params, value):
		"""
			Sets the pan for the given track
			
			@param params[0]: track_index
		"""
		self.log.verbose("(TrackController) set_pan called (" + str(value) + ")")
		track_index = params[0]
		self.log.verbose("(TrackController) for track " + str(track_index))

		track_helper = self.track_helper(track_index)
		track = track_helper.get_track()
		new_value = self.range_util.get_value(track.mixer_device.panning, value);
		track.mixer_device.panning.value = new_value
		
	def set_send(self, params, value):
		"""
			Sets the send value for the given track
			
			@param params[0]: track_index
			@param params[1]: send_index
		"""
		self.log.verbose("(TrackController) set_send called")
		track_index = params[0]
		send_index = params[1]
		self.log.verbose("(TrackController) for track " + str(track_index) + " and send " + str(send_index))
		
		track_helper = self.song_helper().get_track(track_index)
		new_value = self.range_util.get_value(track_helper.get_track().mixer_device.sends[send_id], value);		
		#self.log.verbose("set send " + str(send_index) + " for track " + str(track_index) + " to value " + str(new_value))
		track_helper.set_send_value(send_index, new_value)
		
	def set_volume(self, params, value):
		"""
			Sets the volume for the given track
			
			@param params[0]: track_index
		"""
		self.log.verbose("(TrackController) set_volume called")
		track_index = params[0]
		self.log.verbose("(TrackController) for track " + str(track_index))

		track_helper = self.song_helper().get_track(track_index)
		#self.log.debug("Volume note code " + str(value) + " and value " + str(midi_bytes[2]))
		# value is between 0 and 127 - for volume the wanted max value is 0.85
		value = (0.85 * value) / 128.0
		selected_track = track_helper.get_track()
		selected_track.mixer_device.volume.value = value


