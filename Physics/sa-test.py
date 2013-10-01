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
from annealing.annealing import *

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

        self.rb = Rigidbody()
        self.rb.engine = self.engine
        self.rb.p = Vec(random.uniform(20,580),random.uniform(20,580))
        self.rb.v = Vec(0, 0)
        self.rb.w = 0
        self.rb.invmass = 1
        self.rb.invmoi = 0.001
        self.rb.collider = Narc(self.rb, 4)
        self.rb.mat.setRotation(random.uniform(0,2*math.pi))
        self.rb.collider.restitution = 1.0
        color = pygame.Color(random.randint(0,200),random.randint(0,200),random.randint(0,200))
        self.view.objects.append(NarcObject(self.rb,color))

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
            
            if totElapsed % 2 == 0:
                newrb = Rigidbody()
                newrb.engine = self.engine
                newrb.p = Vec(random.uniform(20,580),random.uniform(20,580))
                newrb.v = Vec(0, 0)
                newrb.w = 0
                newrb.invmass = 1
                newrb.invmoi = 0.001
                newrb.collider = Narc(self.rb, 4)
                newrb.collider.altered(self.rb.collider)
                newrb.mat.setRotation(random.uniform(0,2*math.pi))
                newrb.collider.restitution = 1.0
                color = pygame.Color(random.randint(0,200),random.randint(0,200),random.randint(0,200))
                self.view.objects.append(NarcObject(newrb,color))
                self.rb = newrb
		
                arena = Particle()
                arena.engine = self.engine
                arena.p = Vec(0,0)
                arena.collider = Arena(arena,600,600)
                arena.collider.restitution = 1.0
                self.engine.static.append(arena)
                arena.invmass = 0
            
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
        
            
if __name__=="__main__":
    #import cProfile
    
    t = Test()
    t.Run()
    #print cProfile.run("t.Run()","from test import Test")