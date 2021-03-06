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
        
        '''for i in range(10):
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
            color = pygame.Color(random.randint(0,200),random.randint(0,200),random.randint(0,200))
            self.view.objects.append(PolyObject(rb,color))'''

        for i in range(10):
            rb = Rigidbody()
            rb.engine = self.engine
            rb.p = Vec(random.uniform(20,580),random.uniform(20,580))
            rb.v = Vec(random.uniform(-50,50),random.uniform(-50,50))
            rb.w = random.uniform(-0.5,0.5)
            rb.invmass = 1
            rb.invmoi = 0.001
            rb.collider = Narc(rb, 6)
            rb.mat.setRotation(random.uniform(0,2*math.pi))
            rb.collider.restitution = 1.0
            
            self.engine.moving.append(rb)
            color = pygame.Color(random.randint(0,200),random.randint(0,200),random.randint(0,200))
            self.view.objects.append(NarcObject(rb,color))

        arena = Particle()
        arena.engine = self.engine
        arena.p = Vec(0,0)
        arena.collider = Arena(arena,600,600)
        arena.collider.restitution = 1.0
        self.engine.static.append(arena)
        arena.invmass = 0
        
    def Run(self):
        avefps = 0
        numFrames = 1
        dt = 0
        fps = 0
        physicsdt = 0.025
        elapsed = 0
        totElapsed = 0
        running = True
        while running:
            event = pygame.event.poll()
            if event.type == pygame.QUIT or totElapsed >= 20:
                running = False
            
            self.screen.fill([245, 240, 230]) # blank the screen.
        
            # Save time by only calling this once
            dt = self.clock.tick() * 0.001
            elapsed += dt
            while elapsed>0:
                elapsed -= physicsdt
            
            self.engine.step(physicsdt)
            
            self.view.update()
        
            totElapsed += dt
        
            newfps = 1.0/dt
        
            avefps *= numFrames
            avefps += newfps
                
            numFrames += 1

            avefps /= numFrames
        
            fpstext = 'Current: %.1f | Average: %.1f | Frames: %d'%(newfps, avefps, numFrames)
            fpsSurface = self.font.render(fpstext,False,Color(0,0,0))
            self.screen.blit(fpsSurface,(0,0))
            
            pygame.display.update()
        #print "Average: " + str(avefps)
        #print "Time: " + str(totElapsed)
        #print "Frames: " + str(numFrames)
        
t = Test()
t.Run

if __name__=="__main__":
    #import cProfile
    
    t = Test()
    t.Run()
    #print cProfile.run("t.Run()","from test import Test")