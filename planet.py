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
names=[]

# to do clouds make sure to use 
# convert_alpha(Surface) -> Surface

#https://stackoverflow.com/questions/16880128/pygame-is-there-any-way-to-only-blit-or-update-in-a-mask


# functions go here



# planetary parameters

#planetsize = w, h = 128, 128
planetsize = w, h = 400, 400
water_cutoff = .5










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
  y-=0.5 # make it so 0 is at the equator
  if height<water_cutoff: height=water_cutoff # no underwater ice  
  ice_cutoff = .2
  ice_prob=y*height
  # math.sin
  if abs(ice_prob) > ice_cutoff:
    return True
  return False

def PlanetColor(height,coords):
  # coords = [x,y]
  color = (0,0,0,0)
  #assuming height is between -1 and 1
  height=(height+1)/2
  if height< water_cutoff:
    color = (0,0,int(256*(height/2+water_cutoff)),256)
  else:
    color = (0,int(256*height),0,256)
  
  if Ice(height,float(coords[1])/h):
    color = (256,256,256,256)
  
  return color

def GradientColor(height):
  '''
  if height > 1.0:
    print "warning: height of ", height, "Greater than 1"
    '''
  return (int(256*height),int(256*height),int(256*height),256)

def PerlinList(width, height, xoff, yoff, scale=.012, octaves=2, persistence=.2, lacunarity=4):
  start_time = time.clock()
  hlist = [[0 for i in range(width*2)] for j in range(height)]
  for x in range(width*2):
    for y in range(height):
      hlist[y][x] = snoise2((x+xoff)*scale,(y+yoff)*scale,octaves, persistence, lacunarity,width*scale)
      #noise2(x, y, octaves=1, persistence=0.5, lacunarity=2.0, repeatx=1024, repeaty=1024, base=0.0)
  print "PerlinList created,", time.clock() - start_time, "SECONDS"
  return hlist


def TempList(width, height, xoff, yoff, scale=.012, octaves=2, persistence=.2, lacunarity=4):
  start_time = time.clock()
  tlist= [[0 for i in range(width*2)] for j in range(height)]
  miny=1
  maxy=0
  print height
  for x in range(width*2):
    for y in range(height):
      lat=2.0*abs((1.0*y/height)-0.5)
      triglat=math.cos(math.asin(lat))
      tlist[y][x] = triglat**2*(snoise2((x+xoff)*scale,(y+yoff)*scale,octaves, persistence, lacunarity,width*scale)+1)/2
      #tlist[y][x] = triglat**5
      if tlist[y][x] < miny: miny=tlist[y][x]
      if tlist[y][x] > maxy: maxy=tlist[y][x]
      #noise2(x, y, octaves=1, persistence=0.5, lacunarity=2.0, repeatx=1024, repeaty=1024, base=0.0)
  print "TempList created,", time.clock() - start_time, "SECONDS"
  print "Miny", miny, "Maxy",maxy
  return tlist

#  how is snoise2 returning negative values?  prolly clamped between -1 and 1




# remove alpha component, should speed up computation
# it doesn't help more than marginally
def TerrainFromList(hlist):
  start_time = time.clock()
  im = Image.new( 'RGBA', (len(hlist[0]),len(hlist)), "black") # create a new black image
  pix = im.load()
  for x in range(len(hlist[0])):
    for y in range(len(hlist)):
      pix[x, y] = PlanetColor(hlist[y][x],(x,y))
      #noise2(x, y, octaves=1, persistence=0.5, lacunarity=2.0, repeatx=1024, repeaty=1024, base=0.0)
  print "TerrainFromList created,", time.clock() - start_time, "SECONDS"
  return im.convert("RGBA").tobytes("raw", "RGBA")

def GradientFromList(hlist):
  start_time = time.clock()
  im = Image.new( 'RGBA', (len(hlist[0]),len(hlist)), "black") # create a new black image
  pix = im.load()
  for x in range(len(hlist[0])):
    for y in range(len(hlist)):
      pix[x, y] = GradientColor(hlist[y][x])
      #noise2(x, y, octaves=1, persistence=0.5, lacunarity=2.0, repeatx=1024, repeaty=1024, base=0.0)
  print "GradientFromList created,", time.clock() - start_time, "SECONDS"
  return im.convert("RGBA").tobytes("raw", "RGBA")




# TESTING
def TestGradient(width, height, xoff, yoff):
  im = Image.new( 'RGBA', (width*2,height), "black") # create a new black image
  pix = im.load()
  for x in range(width*2):
    for y in range(height):
      col=black
      if Ice(.5,y/h):
        col= white
      pix[x, y] = col
      
  return im.convert("RGBA").tobytes("raw", "RGBA")

## doesn't work
def RGBA_to_int(col):
  total=0
  n=len(col)-1
  while n>=0:
    a=256*col[n]
    b=16**(len(col)-n)
    total+=int(a*b)
    n-=1
    print col, total
  return total

def list_2d_to_1d(l):
  out=[]
  for row in l:
    out+=row
  return out

def display_mapname(name):
  if pygame.font:
    font = pygame.font.Font(None, 24)
    
    text = font.render(name, 1, (255,255,0))
    textpos = text.get_rect(right=width-20, top=20)
    screen.blit(text, textpos)

def create_map(surface,name):
  rect=surface.get_rect()
  if(width>height):
    rect=rect.move(int(width/2-height/2),0)
  rect=rect.move(-w,0)
  maps.append([surface,rect])
  names.append(name)

#create map 

print "Make HeightMap:"
hlist=PerlinList(w,h,0,0) # make heightmap
print "Make TemperatureMap:"
tlist=TempList(w,h,0,20432) # make temperature map

# todo: trigonometic dropoff  for extreme latitudes
#     i.e. generally colder at poles than equator
# add in a sin function to simulate axial tilt.

# todo: implement biomes


# this will create the different maps for the planet
create_map(pygame.image.fromstring(TerrainFromList(hlist), (w*2,h), 'RGBA'),"Terrain")
create_map(pygame.image.fromstring(GradientFromList(hlist), (w*2,h), 'RGBA'),"Perlin")
create_map(pygame.image.fromstring(GradientFromList(tlist), (w*2,h), 'RGBA'),"Temperature")

# this creates the black mask that goes over & makes it a circle
mask = pygame.image.fromstring(createdarkmask(width,height),(width,height), 'RGBA').convert_alpha()
maskrect=mask.get_rect()


ticks_start=0
ideal_framerate=1000/60
wait_time=0

rot_counter=0
rotation = .1
map_counter = 0


print "Running"
while 1:
  #main loop

  rot_counter+= rotation
  
  if rot_counter>=w:
    for m in maps:
      m[1]=m[1].move(-rot_counter,0)
    rot_counter=0
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
    if keys[pygame.K_LEFT]: map_counter=(map_counter-1)%len(maps)
    if keys[pygame.K_RIGHT]: map_counter=(map_counter+1)%len(maps)

  screen.fill(fill)

  screen.blit(maps[map_counter][0],maps[map_counter][1])
  screen.blit(mask,maskrect)
  display_mapname(names[map_counter])
  pygame.display.flip()


  ticks_end=pygame.time.get_ticks()
  calc_time=ticks_end-ticks_start
  wait=(ideal_framerate)-calc_time
  wait_time = pygame.time.wait(wait)
