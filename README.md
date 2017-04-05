# simplex-planet-gen

An attempt at a procedural planet generator in pygame.  

I don't have an easy way to make a gif of it, but it moves as well.  

There's several different maps which overlay on each other, but only the primary perlin noise map is used currently.  

Planet effect is created via a circular negative mask blitted on top of periodic perlin noise octaves.  

![Motion not depicted](https://raw.githubusercontent.com/koneill1994/simplex-planet-gen/master/terrain.png)
