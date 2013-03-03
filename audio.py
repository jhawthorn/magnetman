import os

import pygame
import pygame.image

from controller import Controller

class AudioController(Controller):
	def loader(self, name):
		class NoneSound:
			def play(self): pass
		if not pygame.mixer:
			return NoneSound()
		
		fullname = os.path.join('sound', name)
		try:
			sound = pygame.mixer.Sound(fullname)
		except pygame.error, message:
			print 'Cannot load sound:', name
			raise SystemExit, message
		return sound

