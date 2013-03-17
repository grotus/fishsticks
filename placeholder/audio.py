import pygame.mixer

class NoMixer:
	
	#def __init__(self):
	def init():
		return False
		
	def get_init():
		return False

class Audio:
	
	tracks = {'hkblue': './mods/hkblue.xm'}
	if pygame.mixer:
		mixer = pygame.mixer
	else:
		mixer = NoMixer()
	
	def __init__(self):
		self.mixer.init()
	
	def play_music(self, track):
		
		if self.mixer.get_init():
			
				self.mixer.music.load(self.tracks[track])
				self.mixer.music.play()

