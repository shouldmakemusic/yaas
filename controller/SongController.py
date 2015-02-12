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
		
	def set_tempo(self, params, value):
		"""
			Set tempo to 
			0 -> new tempo
		"""
		self.log.verbose("(SongController) set_tempo called")
		self.song().tempo = params[0]
		
	def play(self, params, value):
		"""
			Play song
		"""
		self.log.verbose("(SongController) play called")
		self.song().start_playing()
		
	def stop(self, params, value):
		"""
			Stop song
		"""
		self.log.verbose("(SongController) stop called")
		if self.song().is_playing:
			self.song().is_playing = False
		else:
			self.song().current_song_time = 0
		
		
	