
import os

import pygame
from pygame.locals import *

from controller import Controller

class ImageController(Controller):
	def loader(self, name):
		fullname = os.path.join('data', name)
		try:
			image = pygame.image.load(fullname)
		except pygame.error, message:
			print 'Cannot load image:', name
			raise SystemExit, message
		image = pygame.transform.scale(image, (image.get_width()*2, image.get_height()*2))
		
		image = image.convert()
		colorkey = image.get_at((0,0))
		image.set_colorkey(colorkey, RLEACCEL)
		#if colorkey is not None:
		#	if colorkey is -1:
		#		colorkey = image.get_at((0,0))
		#		image.set_colorkey(colorkey, RLEACCEL)
		return image
