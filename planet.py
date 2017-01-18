# planet.py
# K. O'Neill

import sys, os, pygame, math, PIL, noise, time
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
'''
mask = pygame.image.load("mask.png")
maskrect=mask.get_rect()
'''
maps=[]


#ball = pygame.image.load("ball.gif")
#ballrect = ball.get_rect()

#planet = pygame.image.fromstring(string, size, format, Flipped=false)


# string = im.convert("RGBA").tostring("raw", "RGBA")

# to do clouds make sure to use 
# convert_alpha(Surface) -> Surface

#https://stackoverflow.com/questions/16880128/pygame-is-there-any-way-to-only-blit-or-update-in-a-mask


# functions go here

#planetsize = w, h = 128, 128
planetsize = w, h = 400, 400



def sqrdistance(a,b):
  return (a[0]-b[0])**2 + (a[1]-b[1])**2

def createmask(width,height):
  start_time = time.clock()
  im = Image.new( 'RGBA', (width,height), (0,0,0,0)) # create a new blank image
  r = min(width/2, height/2)
  center=(int(width/2),int(height/2))
  pix = im.load()
  for x in range(width):
    for y in range(height):
      sqrdist=sqrdistance((x,y),center)
      if sqrdist < r**2:
        pix[x, y] = (256,256,256,256)
  print "mask created,", time.clock() - start_time, "SECONDS"
  return im.convert("RGBA").tobytes("raw", "RGBA")

def createdarkmask(width,height):
  start_time = time.clock()
  im = Image.new( 'RGBA', (width,height), (0,0,0,256)) # create a new blank image
  r = min(width/2, height/2)
  center=(int(width/2),int(height/2))
  pix = im.load()
  for x in range(width):
    for y in range(height):
      sqrdist=sqrdistance((x,y),center)
      if sqrdist < r**2:
        pix[x, y] = (0,0,0,0)
  print "mask created,", time.clock() - start_time, "SECONDS"
  return im.convert("RGBA").tobytes("raw", "RGBA")

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
  '''
  if height > 1.0:
    print "warning: height of ", height, "Greater than 1"
    '''
  return (int(256*height),int(256*height),int(256*height),256)

def PerlinNoise(width, height, xoff, yoff, scale=.01, octaves=2, persistence=.2, lacunarity=3):
  start_time = time.clock()
  im = Image.new( 'RGBA', (width*3,height), "black") # create a new black image
  pix = im.load()
  for x in range(width*3):
    for y in range(height):
      pix[x, y] = PlanetColor(snoise2((x+xoff)*scale,(y+yoff)*scale,octaves, persistence, lacunarity,width*scale),(x,y))
      #noise2(x, y, octaves=1, persistence=0.5, lacunarity=2.0, repeatx=1024, repeaty=1024, base=0.0)
      #print snoise2(x+xoff,y+yoff,1, 0.6,5,width)
  print "Terrain created,", time.clock() - start_time, "SECONDS"
  return im.convert("RGBA").tobytes("raw", "RGBA")
  
def PerlinNoise_Raw(width, height, xoff, yoff, scale=.01, octaves=2, persistence=.2, lacunarity=3):
  start_time = time.clock()
  im = Image.new( 'RGBA', (width*3,height), "black") # create a new black image
  pix = im.load()
  for x in range(width*3):
    for y in range(height):
      pix[x, y] = GradientColor(snoise2((x+xoff)*scale,(y+yoff)*scale,octaves, persistence, lacunarity,width*scale)/2+1/2)
      #noise2(x, y, octaves=1, persistence=0.5, lacunarity=2.0, repeatx=1024, repeaty=1024, base=0.0)
      #print snoise2(x+xoff,y+yoff,1, 0.6,5,width)
  print "Perlin created,", time.clock() - start_time, "SECONDS"
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


def create_map(surface):
  rect=surface.get_rect()
  rect=rect.move(-w,0)
  maps.append([surface,rect])



# this will create the different maps for the planet
create_map(pygame.image.fromstring(PerlinNoise(w,h,0,0), (w*3,h), 'RGBA'))
create_map(pygame.image.fromstring(PerlinNoise_Raw(w,h,0,0), (w*3,h), 'RGBA'))
create_map(pygame.image.fromstring(TestGradient(w,h,0,0),(w*3,h), 'RGBA'))


# this creates the black mask that goes over & makes it a circle
mask = pygame.image.fromstring(createdarkmask(width,height),(width,height), 'RGBA').convert_alpha()
maskrect=mask.get_rect()

# transparency mask dummied out code
#https://stackoverflow.com/questions/16880128/pygame-is-there-any-way-to-only-blit-or-update-in-a-mask
'''
mask_new = pygame.image.fromstring(createmask(width,height),(width,height), 'RGBA').convert_alpha()
mask_new_rect=mask_new.get_rect()
'''


ticks_start=0
ideal_framerate=1000/60
wait_time=0

rot_counter=0
rotation = .1
map_counter = 0

# transparency mask dummied out code
'''
print "begin test"
masked = maps[map_counter][0].copy().convert_alpha()
masked.blit(mask, (0, 0), None, pygame.BLEND_RGBA_MULT)
screen.blit(masked, (0, 0))

#screen.blit(mask_new,mask_new_rect)
#dummied out code to check that the mask created correctly

'''

print "Running"
while 1:
  #main loop

  rot_counter+= rotation
  
  if rot_counter>=w:
    rot_counter=0
    for m in maps:
      m[1]=m[1].move(-w,0)
  else:
    if rot_counter%1<rotation:
      for m in maps:
        m[1]=m[1].move(1,0)
  # 


  fill = black
  keys = pygame.key.get_pressed()
  for event in pygame.event.get():
    if event.type == pygame.QUIT: sys.exit()
    if keys[pygame.K_ESCAPE]: sys.exit()
    if keys[pygame.K_SPACE]: map_counter=(map_counter+1)%len(maps)

  screen.fill(fill)

  screen.blit(maps[map_counter][0],maps[map_counter][1])
  screen.blit(mask,maskrect)
  pygame.display.flip()


  ticks_end=pygame.time.get_ticks()
  calc_time=ticks_end-ticks_start
  wait=(ideal_framerate)-calc_time
  wait_time = pygame.time.wait(wait)
