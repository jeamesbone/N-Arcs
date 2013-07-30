import random
import math

from physics.physicsEngine import PhysicsEngine
from physics.particle import Particle
from physics.rigidbody import Rigidbody
from physics.mathUtils.vec import Vec
from physics.collider import Circle, Arena, Union, Polygon, Narc
from physics.contactGenerator import ContactGenerator
from view.view import Vew
from view.object import NarcObject

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

class Test(object):
    
    def __init__(self):        
        self.view = View()
        self.view.setup()
        
        
        self.engine = PhysicsEngine()
        self.engine.contactGenerators.append(ContactGenerator(self.engine))
        self.engine.gravity = Vec(0,0)

        for i in range(12):
            rb = Rigidbody()
            rb.engine = self.engine
            rb.p = Vec(random.uniform(20,580),random.uniform(20,580))
            rb.v = Vec(random.uniform(-250,250),random.uniform(-250,250))
            rb.w = random.uniform(-0.5,0.5)
            rb.invmass = 1
            rb.invmoi = 0.001
            rb.collider = Narc(rb)
            rb.mat.setRotation(random.uniform(0,2*math.pi))             
            rb.collider.restitution = 1.0
            
            self.engine.moving.append(rb)
            self.view.objects.append(NarcObject(rb))

        arena = Particle()
        arena.engine = self.engine
        arena.p = Vec(0,0)
        arena.collider = Arena(arena,600,600)
        arena.collider.restitution = 1.0
        self.engine.static.append(arena)
        arena.invmass = 0
        
    def Run(self):
        width = 800
        height = 600

        View.ContextMainLoop()
        
        dt = 0
        fps = 0
        physicsdt = 0.025
        elapsed = 0
        running = True
        while running:
            # Save time by only calling this once
            dt = 0.00001
            elapsed += dt
            while elapsed > 0:
                elapsed -= physicsdt
                self.engine.step(physicsdt)
            self.view.update()
            
if __name__=="__main__":
    import cProfile
    
    t = Test()
    
    print cProfile.run("t.Run()","from test import Test")