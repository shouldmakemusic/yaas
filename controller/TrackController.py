"""
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
from YaasController import *

class TrackController (YaasController):
	__module__ = __name__
	__doc__ = "Control everything that can happen inside a track"

	def __init__(self, yaas):

		YaasController.__init__(self, yaas)
		self.log.debug("(TrackController) init")        

	def stop_or_restart_clip(self, params, value):
		"""
			If a clip is playing in the given track - stop it and remember it
			If this method is called again and no clip is playing - start it again
			0 -> track_index
		"""
		self.log.verbose("(TrackController) stop_or_restart_clip called")
		track_index = params[0]
		self.log.verbose("(TrackController) for clip " + str(track_index))

		track_helper = self.track_helper(track_index)
		track_helper.stop_or_restart_clip()

	def stop(self, params, value):
		"""
			Stop the clip in the given track
			0 -> track_index
		"""

		self.log.verbose("(TrackController) stop called")
		track_index = params[0]
		self.log.verbose("(TrackController) for clip " + str(track_index))

		track_helper = self.track_helper(track_index)
		track_helper.get_track().stop_all_clips()
		
	def arm(self, params, value):
		"""
			Arms the given track or switches it off
			0 -> track_index
		"""

		self.log.verbose("(TrackController) arm called")
		track_index = params[0]
		self.log.verbose("(TrackController) for clip " + str(track_index))

		track_helper = self.track_helper(track_index)
		track_helper.arm()

	def get_focus(self, params, value):
		"""
			Requests the view focus for the given track
			0 -> track_index
		"""

		self.log.verbose("(TrackController) get_focus called")
		track_index = params[0]
		self.log.verbose("(TrackController) for clip " + str(track_index))
		
		track = self.track_helper(track_index).get_track()
		self.view_helper().focus_on_track(track)
