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
		
		
	