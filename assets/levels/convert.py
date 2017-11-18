import pygame
import sys

template = """<?xml version="1.0" encoding="UTF-8"?>
<map version="1.0" tiledversion="1.0.3" orientation="orthogonal" renderorder="right-down" width="%(width)i" height="%(height)i" tilewidth="8" tileheight="8" nextobjectid="%(nextobjectid)i">
 <tileset firstgid="1" source="tiles.tsx"/>
 <objectgroup name="objects">
%(objects)s
 </objectgroup>
 <layer name="background" width="%(width)i" height="%(height)i">
  <data encoding="csv">
%(background)s
  </data>
 </layer>
</map>
"""

objectTemplate = """
<object id="%(nextobjectid)i" name="%(name)s" type="%(type)s" gid="1" x="%(x)i" y="%(y)i" width="8" height="8"/>
"""

imgdata = pygame.image.load(sys.argv[1])

nextobjectid=1
background = ""
objects = []

def addObject(type, x, y):
	x *= 8
	y *= 8
	name = type
	nextobjectid = len(objects) + 1
	objects.append(objectTemplate % locals())

width = imgdata.get_width()
height = imgdata.get_height()

for y in xrange(imgdata.get_height()):
	for x in xrange(imgdata.get_width()):
		data = imgdata.get_at((x,y))[:3]
		tile = -1

		if data[1:] == (0,0xff):
			tile = data[0]
		elif data == (0xff,0,0):
			tile = 14
		elif data == (0,0xff,0):
			addObject("player", x, y)
		elif data == (0,0xaa,0):
			addObject("exit", x, y)
		elif data == (0xff, 0xff, 0):
			addObject("circlebot", x, y)
		elif data == (0xaa, 0xaa, 0):
			addObject("wheelbot", x, y)

		background += str(tile+1) + ","
	background += "\n"

nextobjectid = len(objects) + 1
objects = "".join(objects)
background = background[:-2]

print(template % locals())
