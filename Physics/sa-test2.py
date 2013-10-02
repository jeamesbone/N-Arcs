from annealing.annealing import *
import pyglet
from pyglet.gl import *
from view.pygdraw import *
from pyglet.image.codecs.png import PNGImageDecoder

# set pyglet window               
window = pyglet.window.Window()
pyglet.gl.glClearColor(1,1,1,1)
 
# setup background sprite
bgimage_stream = open("annealing/testRect.png", 'rb')
bgimage = pyglet.image.load("anealing/testRect.png", file=bgimage_stream)
bgsprite = pyglet.sprite.Sprite(bgimage)
bgsprite.x = window.width/2 - bgsprite.width/2
bgsprite.y = window.height/2 - bgsprite.height/2                                                                             
           
p = Particle()
p.p = Vec(bgsprite.width/2, bgsprite.height/2)   
narc = Narc(p, 4)     

image = getImage("annealing/testRect.png")
getCoverage(narc, image)
#getBest(10000, 0.003, 4, image)                                                                                                                                                                                                                                                                                                                                                                                                                                             
             
narc.particle.p = Vec(bgsprite.x + bgsprite.width/2, bgsprite.y + bgsprite.height/2)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      
@window.event
def on_draw():
    window.clear()
    bgsprite.draw()
    
    glPushMatrix()
    glColor3f(0.0, 0.0, 1.0)
    drawRect(bgsprite.x, bgsprite.y, bgsprite.width, bgsprite.height)
    drawNarc(narc)
    glPopMatrix()

pyglet.app.run()