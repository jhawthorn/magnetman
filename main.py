#!/usr/bin/env python

"""
DO NOT EVER USE THIS FOR REFERENCE
I REALLY RAN OUT OF TIME AND THIS IS THE UGLYEST CODE EVER!
THIS IS IN CAPS BECAUSE I DIDN'T HAVE TIME TO TAKE IT OFF
"""

import os, sys, math
import random

import pygame
from pygame.locals import *

from image import ImageController
from audio import AudioController

scale = 2

exe_base_dir = os.path.abspath(os.path.dirname(sys.argv[0]))
os.chdir(exe_base_dir)
sys.path.append(exe_base_dir)

if not pygame.font: print 'Warning, fonts disabled'
if not pygame.mixer: print 'Warning, sound disabled'

images = ImageController()
sounds = AudioController()

tiles = []

class Group(pygame.sprite.Group):
	def draw(self, surface):
		screenrect = pygame.Rect(screen_coord, (pygame.display.get_surface().get_width(), pygame.display.get_surface().get_height()))

		for sprite in self.sprites():
			if screenrect.colliderect(sprite.rect):
				sprite.draw(surface)

	def update(self):
		screenrect = pygame.Rect(screen_coord, (pygame.display.get_surface().get_width(), pygame.display.get_surface().get_height()))

		for sprite in self.sprites():
			if screenrect.colliderect(sprite.rect):
				sprite.update()


slist = []

magnetWalls = Group()
bullets = Group()
walls = Group()
enemies = Group()

screen_coord = [10,0]

def myblit(dest, src, rect):
	rect = pygame.Rect(rect)
	rect[0]-=screen_coord[0]
	rect[1]-=screen_coord[1]
	dest.blit(src, rect)

class Wall(pygame.sprite.Sprite):
	def __init__(self, rect, tile=10):
		pygame.sprite.Sprite.__init__(self)
		self.rect = pygame.Rect(rect)
		self.rect[0]-=1*scale
		self.rect[1]-=1*scale
		self.rect[2]+=2*scale
		self.rect[3]+=2*scale

		self.blit = pygame.Rect(rect)
		self.tile = tile

	def draw(self, surface):
		myblit(surface, tiles[self.tile], self.blit)

class Door:
	def __init__(self, coord):
		self.image = images["door.png"]
		self.coord = pygame.Rect(coord, (0,0))

		self.rect = pygame.Rect(coord, self.image.get_size())
		self.rect.inflate_ip(-16,0)

	def draw(self, surface):
		myblit(surface, self.image, self.coord)

class MagnetWall(Wall):
	def __init__(self, rect):
		pygame.sprite.Sprite.__init__(self)
		self.rect = rect

	def draw(self, surface):
		myblit(surface, tiles[13], self.rect)
		#surface.fill((230,15,15), self.rect)

class Bullet(pygame.sprite.Sprite):
	def __init__(self, coord, direction):
		pygame.sprite.Sprite.__init__(self)
		self.images = [images["bullet.png"], pygame.transform.flip(images["bullet.png"], True, False)]

		self.rect = pygame.Rect(coord, self.images[0].get_size())
		self.direction = direction

		self.ticks = 40

		if self.direction == 1:
			self.rect[0] += 12*scale
		else:
			self.rect[0] -= 12*scale

		self.rect.inflate_ip(-12, 0)

	def draw(self, surface):
		myblit(surface, self.images[self.direction], self.rect)

	def update(self):
		if not self.ticks:
			self.kill()
			return

		self.ticks-=1

		if self.direction == 1:
			self.rect[0] += 4
		else:
			self.rect[0] -= 4
			#todo
		if pygame.sprite.spritecollideany(self, magnetWalls) or pygame.sprite.spritecollideany(self, walls):
			self.kill()

class Enemy(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)

	def update(self):
		for bullet in pygame.sprite.spritecollide(self, bullets, True):
			self.damage()

class WheelBot(Enemy):
	def __init__(self, x, y):
		Enemy.__init__(self)
		image = images["wheelbot.png"]
		self.rect = pygame.Rect((x, y), (image.get_height(), image.get_height()-8))

		self.images = []

		self.count = random.randint(0, 120)

		self.direction = random.randint(0, 1)

		for i in xrange(2):
			surface = pygame.Surface((image.get_height(), image.get_height()))
			surface.fill((0xff, 0x00, 0xff))
			surface.set_colorkey(surface.get_at((0,0)), RLEACCEL)
			surface.blit(image, (0,0), (i*image.get_height(), 0, image.get_height(), image.get_height()))
			self.images.append(surface)

	def update(self):
		Enemy.update(self)
		self.count+=1


		if pygame.sprite.spritecollideany(self, walls):
			self.direction = not self.direction
			sounds["bump.wav"].play()
		else:
			for sprite in pygame.sprite.spritecollide(self, enemies, False):
				if sprite is not self:
					self.direction = not self.direction
					if not sounds["bump.wav"].get_num_channels(): sounds["bump.wav"].play()
					break

		if self.direction:
			self.rect[0] += 1
		else:
			self.rect[0] -= 1

	def damage(self):
		self.kill()

	def draw(self, surface):
		myblit(surface, self.images[(self.count/15)%2], self.rect)


class CircleBot(Enemy):
	def __init__(self, x, y):
		Enemy.__init__(self)
		image = images["circlebot.png"]
		self.rect = pygame.Rect((x, y), (image.get_height(), image.get_height()))
		self.rect = self.rect.inflate(-10,-10)

		self.images = []

		self.count = random.randint(0, 15*3)

		for i in xrange(4):
			surface = pygame.Surface((image.get_height(), image.get_height()))
			surface.fill((0xff, 0x00, 0xff))
			surface.set_colorkey(surface.get_at((0,0)), RLEACCEL)
			surface.blit(image, (0,0), (i*image.get_height(), 0, image.get_height(), image.get_height()))
			self.images.append(surface)

	def damage(self):
		self.kill()

	def update(self):
		Enemy.update(self)
		self.count+=1

	def draw(self, surface):
		myblit(surface, self.images[1+(self.count/15)%3], self.rect)


class Player(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)

		image = images["player.png"]

		self.images = ([], [], [], [], [], [], [], [], [], [])

		for i in xrange(8):
			surface = pygame.Surface((20*scale, 26*scale))
			surface.fill((0xff, 0x00, 0xff))
			surface.set_colorkey(surface.get_at((0,0)), RLEACCEL)
			surface.blit(image, (0,0), ((i%4)*22*scale, math.floor(i/4)*28*scale, 20*scale, 26*scale))
			self.images[0].append(surface)
			self.images[1].append(pygame.transform.flip(surface, True, False))

		for i in xrange(4):
			surface = pygame.Surface((20*scale, 26*scale))
			surface.fill((0xff, 0x00, 0xff))
			surface.set_colorkey(surface.get_at((0,0)), RLEACCEL)
			surface.blit(image, (0,0), ((i%4)*22*scale, (2*28*scale), 20*scale, 26*scale))
			self.images[i*2+2].append(surface)
			self.images[i*2+3].append(pygame.transform.flip(surface, True, False))

		self.hp = 6

		self.width = 20
		self.height = 26

		self.counter = 0
		self.direction = 1

		self.rect = pygame.Rect((1,1), (self.width*scale-2, self.height*scale))

		self.ldelay = 0
		self.rdelay = 0

		self.jdelay = 0

		self.x = x*scale-20
		self.y = y*scale

		self.vx = 0
		self.vy = 0

		self.isonwall = False
		self.isonground = False

		self.invincibility = 0

		self.dead = False

		self.updateRect()

	def blit(self, anim, surface):
		self.rect[0] -= 1
		myblit(surface, self.images[anim][(int(self.counter/7))%len(self.images[anim])], self.rect)
		self.rect[0] += 1

	def draw(self, surface):
		if self.invincibility:
			if self.counter % 20 < 10:
				return

		if self.dead:
			self.rect[1]+=38
			myblit(surface, images["dead.png"], self.rect)
			return

		if self.vx > 0:
			self.direction = 1
		elif self.vx < 0:
			self.direction = 0

		mwallrects = map(lambda x: x.rect, magnetWalls.sprites())

		if self.rrmag.collidelist(mwallrects) != -1:
			self.blit(0+6, surface)
		elif self.rlmag.collidelist(mwallrects) != -1:
			self.blit(1+6, surface)
		elif not self.onground():
			self.blit(self.direction+8, surface)
		elif self.vx == 0:
			self.blit(self.direction+2, surface)
		else:
			self.blit(self.direction, surface)

		"""wallrects = map(lambda x: x.rect, walls.sprites())

		for r in (self.rleft, self.rright, self.rtop, self.rbottom):
			r[0]-=screen_coord[0]
			r[1]-=screen_coord[1]
			if r.collidelist(wallrects) != -1:
				surface.fill((200,0,0), r)
			else:
				surface.fill((0,0,0), r)

		for r in (self.rrmag, self.rlmag):
			r[0]-=screen_coord[0]
			r[1]-=screen_coord[1]
			if r.collidelist(mwallrects) != -1:
				surface.fill((200,200,0), r)
			else:
				surface.fill((0,200,0), r)"""



	def updateRect(self):
		self.rect[0] = self.x*scale
		self.rect[1] = self.y*scale

		self.rleft   = pygame.Rect(self.rect[0]+2,              self.rect[1]+2,                2,              self.rect[3]-4)
		self.rright  = pygame.Rect(self.rect[0]+self.rect[2]-2, self.rect[1]+2,                2,              self.rect[3]-4)
		self.rtop    = pygame.Rect(self.rect[0]+4,              self.rect[1],                  self.rect[2]-6, 2)
		self.rbottom = pygame.Rect(self.rect[0]+4,              self.rect[1]+self.rect[3]-2,   self.rect[2]-6, 2)

		self.rrmag   = pygame.Rect(self.rect[0],                self.rect[1]+24,               2,              2)
		self.rlmag   = pygame.Rect(self.rect[0]+self.rect[2],   self.rect[1]+24,               2,              2)

	def keypress(self,key):
		if key == K_UP:
			mwallrects = map(lambda x: x.rect, magnetWalls.sprites())
			if self.rlmag.collidelist(mwallrects) != -1:
				self.vx -= .25
				self.x -= 1
				self.vy = -1
				self.rdelay = 30
			elif self.rrmag.collidelist(mwallrects) != -1:
				self.vx = .25
				self.x += 1
				self.vy = -1
				self.ldelay = 30
			elif self.onground():
				self.vy = -1
				self.y-=1
			elif self.jdelay:
				self.vy = -1
			self.updateRect()
		elif key == K_LCTRL:
			Bullet(((self.x)*scale, (self.y+11)*scale), self.direction).add(bullets)
			sounds["shot.wav"].stop()
			sounds["shot.wav"].play()


	def onground(self):
		return self.rbottom.collidelist(map(lambda x: x.rect, walls.sprites())) != -1

	#def onWall(self):
	#	if not pygame.sprite.spritecollideany(self, magnetWalls): return False
	#	return True

	def update(self):
		if self.dead:
			return

		keys = pygame.key.get_pressed()

		self.platforms = pygame.sprite.spritecollide(self, walls, False)
		wallrects = map(lambda x: x.rect, walls.sprites())
		mwallrects = map(lambda x: x.rect, magnetWalls.sprites())

		self.isonground = False
		if self.rbottom.collidelist(wallrects) != -1: #todo
				self.isonground = True

		if self.ldelay:
			if self.onground():
				self.ldelay = 0
			else:
				self.ldelay -= 1
		if self.rdelay:
			if self.onground():
				self.rdelay = 0
			else:
				self.rdelay -= 1

		if self.jdelay:
			self.jdelay -= 1

		if self.rrmag.collidelist(mwallrects) != -1:
			self.vx = 0
			self.vy = 0

			if keys[K_RIGHT]:
				self.x += 1
				self.jdelay = 12
		elif self.rlmag.collidelist(mwallrects) != -1:
			self.vx = 0
			self.vy = 0

			if keys[K_LEFT]:
				self.x -= 1
				self.jdelay = 12
		else:
			if keys[K_LEFT] and not self.ldelay:
				self.vx = max(self.vx-.125, -.5)
				self.rdelay = 0
				if keys[K_RIGHT] and self.onground():
					self.vx = 0
			if keys[K_RIGHT] and not self.rdelay:
				self.vx = min(self.vx+.125, .5)
				self.ldelay = 0
				if keys[K_LEFT] and self.onground():
					self.vx = 0
			if self.onground() and not keys[K_RIGHT] and not keys[K_LEFT]:
				self.vx = 0
			if self.vy < 0 and not keys[K_UP]:
				self.vy = max(self.vy, -.5)

			self.vy = min(self.vy+.015, 1)


			if self.rbottom.collidelist(wallrects) != -1 and self.vy > 0:
				self.vy = 0
			elif self.rtop.collidelist(wallrects) != -1 and self.vy < 0:
				self.vy = 0
			if self.rleft.collidelist(wallrects) != -1 and self.vx < 0:
				self.vx = 0
			elif self.rright.collidelist(wallrects) != -1 and self.vx > 0:
				self.vx = 0


			self.x += self.vx
			self.y += self.vy

		if pygame.sprite.spritecollideany(self, enemies) and not self.invincibility:
			self.hp -= 1

			if self.hp == 0:
				self.dead = True

			self.invincibility = 180
		elif self.invincibility:
			self.invincibility-=1

		self.updateRect()

		self.counter += 1

#if you're deading this: NOTE: sleep is a wonderful thing

def init():
	pygame.init()
	screen = pygame.display.set_mode((320*scale, 240*scale))

	pygame.display.set_caption('Magno-Man')
	pygame.mouse.set_visible(1)


class WinGame(Exception):
	pass

class LoseGame(Exception):
	pass

class Game:
	def __init__(self):
		#tiles
		tileimage = images["tiles.png"]

		for i in xrange((tileimage.get_width() * tileimage.get_height() / (8*8*scale*scale))):
			surface = pygame.Surface((8*scale, 8*scale))
			surface.fill((0xff, 0x00, 0xff))
			surface.set_colorkey(surface.get_at((0,0)), RLEACCEL)
			surface.blit(tileimage, (0,0), ((i%8)*8*scale, (i/8)*8*scale, 20*scale, 26*scale))
			tiles.append(surface)

		try:
			self.bg = pygame.image.load(os.path.join("data", "bg.png"))
		except pygame.error, message:
			print 'Cannot load level', num
			raise SystemExit, message
		self.bg = pygame.transform.scale(self.bg, (self.bg.get_width()*2, self.bg.get_height()*2))
		self.bg = self.bg.convert()

		self.level=0
		self.nextLevel()

	def nextLevel(self):
		self.level += 1

		self.loadLevel(self.level)

	def loadLevel(self, num):
		magnetWalls.empty()
		bullets.empty()
		walls.empty()
		enemies.empty()

		try:
			imgdata = pygame.image.load(os.path.join("levels", "".join((str(num), ".png"))))
		except pygame.error:
			#print 'Cannot load level', num
			raise WinGame

		self.mapwidth = imgdata.get_width()*8*scale
		self.mapheight = imgdata.get_height()*8*scale

		for y in xrange(imgdata.get_height()):
			for x in xrange(imgdata.get_width()):
				data = imgdata.get_at((x,y))[:3]

				if data[1:] == (0,0xff):
					Wall((x*8*scale,y*8*scale,8*scale,8*scale), tile=data[0]).add(walls)
				elif data == (0xff,0,0):
					MagnetWall((x*8*scale,y*8*scale,8*scale,8*scale)).add(magnetWalls)
				elif data == (0,0xff,0):
					try:
						hp = self.player.hp
						self.player = Player(x*4,y*4)
						self.player.hp = hp
					except:
						self.player = Player(x*4,y*4)
				elif data == (0,0xaa,0):
					self.door = Door((x*8*scale,y*8*scale))
				elif data == (0xff, 0xff, 0):
					CircleBot(x*8*scale, y*8*scale).add(enemies)
				elif data == (0xaa, 0xaa, 0):
					WheelBot(x*8*scale, y*8*scale).add(enemies)

	def input(self, events):
		for event in events:
			if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
				raise SystemExit
			elif event.type == KEYDOWN:
				if event.key == K_DOWN:
					if self.player.rect.colliderect(self.door.rect):
						self.nextLevel()
				else:
					self.player.keypress(event.key)
			else:
				#print "unhandled:", event
				pass

	def draw_hud(self):
		pygame.display.get_surface().fill((0,0,0), pygame.Rect(0,0,pygame.display.get_surface().get_width(),32))
		pygame.display.get_surface().fill((47,62,80), pygame.Rect(36,1*2,55*2,14*2))

		pygame.display.get_surface().blit(images["health.png"], pygame.Rect(4,2,0,0))

		for i in xrange(6):
			rect = pygame.Rect(36+i*18,2,0,0)
			if i < self.player.hp:
				pygame.display.get_surface().blit(images["hp1.png"], rect)
			else:
				pygame.display.get_surface().blit(images["hp0.png"], rect)


	def draw(self):
		screen = pygame.display.get_surface()

		for y in xrange(self.mapheight/scale/64+1):
			for x in xrange(self.mapwidth/scale/64+1):
				screen.blit(self.bg, pygame.Rect(x*64*scale-(screen_coord[0]/2), y*64*scale-(screen_coord[1]/4), 64*scale, 64*scale))

		self.door.draw(screen)
		enemies.draw(screen)
		self.player.draw(screen)
		magnetWalls.draw(screen)
		walls.draw(screen)
		bullets.draw(screen)

		self.draw_hud()

		pygame.display.flip()

		if self.player.dead:
			raise LoseGame

	def update(self):
		enemies.update()
		self.player.update()
		bullets.update()

		#screen coords
		dx= self.player.rect[0]-pygame.display.get_surface().get_width()/2
		dy = self.player.rect[1]-pygame.display.get_surface().get_height()/2

		screen_coord[0] = dx
		screen_coord[1] = dy

		screen_coord[0] = max(screen_coord[0], 0)
		screen_coord[0] = min(screen_coord[0], self.mapwidth-pygame.display.get_surface().get_width())

		screen_coord[1] = max(screen_coord[1], -32)
		screen_coord[1] = min(screen_coord[1], self.mapheight-pygame.display.get_surface().get_height())

	def run(self):
		clock = pygame.time.Clock()

		while True:
			self.input(pygame.event.get())

			self.update()
			self.update()
			self.update()

			self.draw()

			clock.tick(40)


def fprint(rect, string, colour=(0,0,0), size=25):
	font = pygame.font.Font("Volter.ttf", size)
	image =font.render(string, 0, colour)
	pygame.transform.scale(image, (image.get_width()*2, image.get_height()*2))

	pygame.display.get_surface().blit(image, rect)

def menu(args):
	options = []

	screen = pygame.display.get_surface()

	font = pygame.font.Font("Volter.ttf", 18)

	title = images["title.png"]
	x = 90
	for arg in args:
		image = font.render(arg, 0, (255,255,255))
		image = pygame.transform.scale(image, (image.get_width()*2, image.get_height()*2))
		image2 = font.render(arg, 0, (0,0,255))
		image2 = pygame.transform.scale(image2, (image2.get_width()*2, image2.get_height()*2))

		options.append((arg, (image, image2), pygame.Rect((x,410), image.get_size())))

		x += 350

	while True:
		for event in pygame.event.get():
			if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
				raise SystemExit
			elif event.type == MOUSEBUTTONUP and event.button == 1:
				for option in options:
					if option[2].collidepoint(event.pos):
						return option[0]

		#pygame.display.get_surface().fill((0xff, 0xff, 0xff))
		pygame.display.get_surface().blit(title, (0,0))

		for option in options:
			if option[2].collidepoint(pygame.mouse.get_pos()):
				screen.blit(option[1][1], option[2])
			else:
				screen.blit(option[1][0], option[2])

		pygame.display.flip()

def main():
	init()	#Game().run()
	#return

	sounds["song.ogg"].play(-1)

	while True:
		choice = menu(["NewGame", "Quit"])

		if choice == "NewGame":
			try:
				Game().run()
			except WinGame:
				cont = True
				while cont:
					fprint((125,100), "WINNER!", colour=(0xff,0xff,0xff), size=100)
					pygame.display.flip()
					for event in pygame.event.get():
						if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
							raise SystemExit
						elif event.type == KEYDOWN:
							cont = False
			except LoseGame:
				cont = True
				while cont:
					fprint((125,100), "YouLose", colour=(0xff,0xff,0xff), size=100)
					pygame.display.flip()
					for event in pygame.event.get():
						if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
							raise SystemExit
						elif event.type == KEYDOWN:
							cont = False
		else:
			raise SystemExit


if __name__ == "__main__":
	main()
