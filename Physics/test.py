import random
import math
import pyglet

from pyglet import clock

from view.pygdraw import *

from physics.physicsEngine import PhysicsEngine
from physics.particle import Particle
from physics.rigidbody import Rigidbody
from physics.mathUtils.vec import Vec
from physics.collider import Circle, Arena, Union, Polygon, Narc
from physics.contactGenerator import ContactGenerator

class Test(object):
    def __init__(self):        
        self.engine = PhysicsEngine()
        self.engine.contactGenerators.append(ContactGenerator(self.engine))
        self.engine.gravity = Vec(0,0)
        
        self.objects = []
        
        # Create objects
        for i in range(10):
            self.createNarc()
            # self.createPoly()
        
        # Create arena 
        self.createArena(600, 600)        
    
    def draw(self):
        for o in self.objects:
            glPushMatrix()
            glColor3f(0.0, 1.0, 0.0)
            drawObject(o)
            glPopMatrix()
    
    def createArena(self, width, height):
        arena = Particle()
        arena.engine = self.engine
        arena.p = Vec(0,0)
        arena.collider = Arena(arena,width,height)
        arena.collider.restitution = 1.0
        self.engine.static.append(arena)
        arena.invmass = 0
        
    def createNarc(self):
        rb = Rigidbody()
        rb.engine = self.engine
        rb.p = Vec(random.uniform(20,580),random.uniform(20,580))
        rb.v = Vec(random.uniform(-100,100),random.uniform(-100,100))
        rb.w = random.uniform(-0.5,0.5)
        rb.invmass = 1
        rb.invmoi = 0.001
        rb.collider = Narc(rb, 4)
        rb.mat.setRotation(random.uniform(0,2*math.pi))
        rb.collider.restitution = 1.0

        self.engine.moving.append(rb)
        self.objects.append(rb.collider)
        
    def createPoly(self):
        rb = Rigidbody()
        rb.engine = self.engine
        rb.p = Vec(random.uniform(20,580),random.uniform(20,580))
        rb.v = Vec(random.uniform(-50,50),random.uniform(-50,50))
        rb.w = random.uniform(-0.25,0.25)
        rb.invmass = 1
        rb.invmoi = 0.001 
        rb.collider = Polygon(rb,[Vec(random.uniform(-30,-10),random.uniform(10,30)),
				  Vec(random.uniform(-30,-10),random.uniform(-30,-10)),
				  Vec(random.uniform(10,30),random.uniform(-30,-10)), 
			          Vec(random.uniform(10,30),random.uniform(10,30))])
        rb.collider.restitution = 1.0
        self.engine.moving.append(rb)
        self.objects.append(rb.collider)

# set pyglet window               
window = pyglet.window.Window(width=600, height=600)
pyglet.gl.glClearColor(1,1,1,1)

t = Test()

def update(dt):
    t.engine.step(dt)
    #window.invalid = True

pyglet.clock.schedule(update)

fps_display = clock.ClockDisplay()

@window.event
def on_draw():      
    window.clear()
    
    fps_display.draw()
    t.draw()

pyglet.app.run()