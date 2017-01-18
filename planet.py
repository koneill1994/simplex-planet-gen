# planet.py
# K. O'Neill

import sys, os, pygame, math, PIL, noise
from PIL import Image
from noise import snoise2

from pygame import gfxdraw

if not pygame.font: print 'Warning, fonts disabled'
if not pygame.mixer: print 'Warning, sound disabled'

pygame.init()

size = width, height = 640, 400


black = 0,0,0,255
white = 255,255,255,255
red = 255,0,0,255
blue = 0,0,255,255
green = 0,255,0,255
yellow = 255,255,0,255

screen = pygame.display.set_mode(size)

mask = pygame.image.load("mask.png")
maskrect=mask.get_rect()

#ball = pygame.image.load("ball.gif")
#ballrect = ball.get_rect()

#planet = pygame.image.fromstring(string, size, format, Flipped=false)


# string = im.convert("RGBA").tostring("raw", "RGBA")


# functions go here

#planetsize = w, h = 128, 128
planetsize = w, h = 400, 400

#TESTING
def Ice(height, y):
  # y normalized between 0 and 1
  ice_cutoff = .05
  ice_prob=y*height
  # math.sin
  if ice_prob > ice_cutoff:
    return True
  return False

def PlanetColor(height,coords):
  # coords = [x,y]
  color = (0,0,0,0)
  #assuming height is between -1 and 1
  height=(height+1)/2
  if height<.5:
    color = (0,0,int(256*height),256)
  else:
    color = (0,int(256*height),0,256)
  
  if Ice(height,coords[1]/h):
    color = (256,256,256,256)
  
  return color

def GradientColor(height):
  return (int(256*height),int(256*height),int(256*height),256)

def PerlinNoise(width, height, xoff, yoff, scale=.01, octaves=2, persistence=.2, lacunarity=3):
  im = Image.new( 'RGBA', (width*3,height), "black") # create a new black image
  pix = im.load()
  for x in range(width*3):
    for y in range(height):
      pix[x, y] = PlanetColor(snoise2((x+xoff)*scale,(y+yoff)*scale,octaves, persistence, lacunarity,width*scale),(x,y))
      #noise2(x, y, octaves=1, persistence=0.5, lacunarity=2.0, repeatx=1024, repeaty=1024, base=0.0)
      #print snoise2(x+xoff,y+yoff,1, 0.6,5,width)
  return im.convert("RGBA").tobytes("raw", "RGBA")

# TESTING
def TestGradient(width, height, xoff, yoff):
  im = Image.new( 'RGBA', (width*3,height), "black") # create a new black image
  pix = im.load()
  for x in range(width*3):
    for y in range(height):
      col=black
      if Ice(.5,y/h):
        col= white
      pix[x, y] = col
      
  return im.convert("RGBA").tobytes("raw", "RGBA")
















#planet = pygame.image.fromstring(PerlinNoise(w,h,0,0), (w*3,h), 'RGBA')
planet = pygame.image.fromstring(TestGradient(w,h,0,0),(w*3,h), 'RGBA')
planetrect = planet.get_rect()
planetrect=planetrect.move(-w,0)

ticks_start=0
ideal_framerate=1000/60
wait_time=0

rot_counter=0
rotation = .1

while 1:
  #main loop

  rot_counter+= rotation
  
  if rot_counter==w:
    rot_counter=0
    planetrect=planetrect.move(-w,0)
  else:
    if rot_counter%1<rotation:
      planetrect=planetrect.move(1,0)

  fill = black
  keys = pygame.key.get_pressed()
  for event in pygame.event.get():
    if event.type == pygame.QUIT: sys.exit()
    if keys[pygame.K_ESCAPE]: sys.exit()

  screen.fill(fill)

  screen.blit(planet, planetrect)
  screen.blit(mask,maskrect)
  pygame.display.flip()


  ticks_end=pygame.time.get_ticks()
  calc_time=ticks_end-ticks_start
  wait=(ideal_framerate)-calc_time
  wait_time = pygame.time.wait(wait)
