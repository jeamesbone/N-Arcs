
import random
import math

import pygame
from pygame.locals import *

from physics.physicsEngine import PhysicsEngine
from physics.particle import Particle
from physics.rigidbody import Rigidbody
from physics.mathUtils.vec import Vec
from physics.collider import Circle, Arena, Union, Polygon, Narc
from physics.contactGenerator import ContactGenerator
from view.view import View
from view.object import CircleObject, CircleUnionObject, PolyObject, NarcObject

class Test(object):
    
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        
        self.screen = pygame.display.set_mode([600, 600])
        self.view = View(self.screen)
        self.font = pygame.font.Font(None,30)
        
        self.engine = PhysicsEngine()
        self.engine.contactGenerators.append(ContactGenerator(self.engine))
        self.engine.gravity = Vec(0,0)


#for i in range(5):
#    c = Particle()
#    c.engine = engine
#    c.p = Vec(random.uniform(20,580),random.uniform(20,580))
#    c.v = Vec(random.uniform(-150,150),random.uniform(-150,150))
#    c.m = random.uniform(40,1000)
#    c.collider = Circle(c,Vec(0,0),math.sqrt(c.m))
#    c.collider.restitution = 0.75
#    
#    engine.moving.append(c)
#    color = pygame.Color(random.randint(0,200),random.randint(0,200),random.randint(0,200))
#    view.objects.append(CircleObject(c,color))
#    
#u = Particle()
#u.engine = engine
#u.p = Vec(100,100)
#u.v = Vec(0,0)
#u.m = 100.0
#u.collider = Union(u)
#u.collider.colliders.append(Circle(u,Vec(0,-10),20))
#u.collider.colliders.append(Circle(u,Vec(0,10),20))
#u.collider.restitution = 0.75

#for i in range(25):
#    p = Particle();
#    p.engine = engine
#    p.p = Vec(random.uniform(20,580),random.uniform(20,580))
#    p.v = Vec(random.uniform(-50,50),random.uniform(-50,50))
#    p.collider = Polygon(p,[Vec(random.uniform(-30,-10),random.uniform(10,30)), 
#                            Vec(random.uniform(-30,-10),random.uniform(-30,-10)),
#                            Vec(random.uniform(10,30),random.uniform(-30,-10)), 
#                            Vec(random.uniform(10,30),random.uniform(10,30))])
#    p.collider.restitution = 1.0
#
#    engine.moving.append(p)
#    color = pygame.Color(random.randint(0,200),random.randint(0,200),random.randint(0,200))
#    view.objects.append(PolyObject(p,color))


            
        '''for i in range(15):
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
            color = pygame.Color(random.randint(0,200),random.randint(0,200),random.randint(0,200))
            self.view.objects.append(NarcObject(rb,color))'''

        arena = Particle()
        arena.engine = self.engine
        arena.p = Vec(0,0)
        arena.collider = Arena(arena,600,600)
        arena.collider.restitution = 1.0
        self.engine.static.append(arena)
        arena.invmass = 0
        
    def Run(self):
        dt = 0
        fps = 0
        physicsdt = 0.025
        elapsed = 0
        running = True
        while running:
            event = pygame.event.poll()
            if event.type == pygame.QUIT:
                running = False
            
            self.screen.fill([245, 240, 230]) # blank the screen.
        
            # Save time by only calling this once
            dt = self.clock.tick(40)*0.001
            elapsed += dt
            #while elapsed>0:
            #    elapsed -= physicsdt
            
            self.engine.step(physicsdt)   
            self.view.update() 
                
            fpstext = '%.1f'%(1.0/dt)
            fpsSurface = self.font.render(fpstext,False,Color(0,0,0))
            self.screen.blit(fpsSurface,(0,0))
            
            pygame.display.update()
            
if __name__=="__main__":
    import cProfile
    
    t = Test()
    
    print cProfile.run("t.Run()","from test import Test")