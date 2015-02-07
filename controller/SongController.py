from YaasController import YaasController

OFF = 0
ON = 1

class SongController (YaasController):

	__module__ = __name__
	__doc__ = "Control everything that has to do with the song"
    
	def __init__(self, yaas):

		YaasController.__init__(self, yaas)
		self.log.debug("(SongController) init")        
        
	def record(self, params, value):
		"""
			Start recording all armed tracks
		"""
		self.log.verbose("(SongController) record called")
		
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
		
	def metronom(self, params, value):
		"""
			Start or stop metronom
		"""
		self.log.verbose("(SongController) metronom called")
		if (self.song().metronome):
			self.song().metronome = OFF
		else:
			self.song().metronome = ON
			
	def tap_tempo(self, params, value):
		"""
			Tap tempo
		"""
		self.log.verbose("(SongController) tap_tempo called")
		self.song().tap_tempo()
		
	def select_track(self, params, value):
		"""
			Set current view to track
            0 -> track_index
		"""
		self.log.verbose("(SongController) select_track called")
		track_index = params[0] - 1
		
		track = self.song().tracks[track_index]
		#all_tracks = self._song_helper.get_all_tracks() #this is from the MixerComponent's _next_track_value method
		#self.song().view.selected_track = all_tracks[track_index]
		
		self.song().view.selected_track = track
		self.application().view.focus_view("Detail") 
		self.application().view.focus_view("Detail/DeviceChain") 
		
		#self.log.debug("arrayActiveDevices removed ")
		
	