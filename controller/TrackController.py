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
