'''
Created on 22/09/2012

@author: Robert
'''
import math
from pygame import Rect
import pygame.gfxdraw
import pygame.draw
from pygame.locals import SRCALPHA
from physics.mathUtils.vec import Vec

class PhysicsObject(pygame.sprite.Sprite):
    '''
    classdocs
    '''


    def __init__(self,particle):
        '''
        Constructor
        '''
        pygame.sprite.Sprite.__init__(self)
        self.original = None;
        self.view = None;
        self.particle = particle
        self.rect = Rect(0,0,0,0);
        
    def update(self):            
        self.rect.center = self.particle.p
        
        r = self.particle.getRotation()
        if r:
            self.view = pygame.transform.rotate(self.original,math.degrees(-r))
            self.rect.width, self.rect.height = self.view.get_size()
        
        
class CircleObject(PhysicsObject):
    def __init__(self,particle,color):
        '''
        Constructor
        '''
        PhysicsObject.__init__(self,particle)
        radius = int(particle.collider.r)
        self.original = pygame.surface.Surface([radius*2+1, radius*2+1],SRCALPHA)
        pygame.gfxdraw.aacircle(self.original, radius,radius,radius,color)
        pygame.gfxdraw.filled_circle(self.original,radius,radius,radius,color)
        
        self.view = self.original
        self.rect = pygame.Rect(particle.p.x-radius,particle.p.y-radius,radius*2+1, radius*2+1)
        
    def rotate(self):
        pass
        
class PolyObject(PhysicsObject):
    def __init__(self,particle,color):
        '''
        Constructor
        '''
        PhysicsObject.__init__(self,particle)
        
        print particle.collider.points
        
        xs = [int(p.x) for p in particle.collider.points]
        ys = [int(p.y) for p in particle.collider.points]
        width = max(-min(xs),max(xs))*2
        height = max(-min(ys),max(ys))*2
        self.rect = Rect(-width/2,-height/2,width,height)
        print self.rect
        
        relps = zip([x-self.rect.left for x in xs],[y-self.rect.top for y in ys])
        
        self.original = pygame.surface.Surface([self.rect.width,self.rect.height],SRCALPHA)
        pygame.gfxdraw.aapolygon(self.original, relps, color)
        pygame.gfxdraw.filled_polygon(self.original, relps, color)
        
        self.view = self.original

class NarcObject(PhysicsObject):
    def __init__(self, particle, color):
        PhysicsObject.__init__(self, particle)
        
        for arc in particle.collider.arcs:
            if arc.inArc(arc.pos + Vec(-1, 0)):
                xMin = arc.pos.x - arc.radius
            if arc.inArc(arc.pos + Vec(1, 0)):
                xMax = arc.pos.x + arc.radius
            if arc.inArc(arc.pos + Vec(0, -1)):
                yMin = arc.pos.y - arc.radius
            if arc.inArc(arc.pos + Vec(0, 1)):
                yMax = arc.pos.y + arc.radius        
        
        width = xMax - xMin
        height = yMax - yMin
        
        self.original = pygame.surface.Surface([width, height], SRCALPHA)
        
        for arc in particle.collider.arcs:
            a1 = -arc.getStart()
            a2 = -arc.getEnd()
            if a2 - a1 > math.pi:
                a2 -= math.pi * 2
            if a1 < a2:
                start = a1
                end = a2
            else:
                start = a2
                end = a1
            pygame.draw.arc(self.original, color, Rect((arc.pos.x - xMin - arc.radius, arc.pos.y - yMin - arc.radius), (arc.radius * 2, arc.radius * 2)), start, end)
        
        self.view = self.original
        self.rect = pygame.Rect(particle.p.x - width / 2, particle.p.y - height / 2, width, height)

class CircleUnionObject(PhysicsObject):
    def __init__(self,particle,color):
        '''
        Constructor
        '''
        PhysicsObject.__init__(self,particle)
        
        self.rect = Rect(0,0,0,0)
        for c in particle.collider.colliders:
            radius = int(c.r)
            rect = pygame.Rect(c.p.x-radius,c.p.y-radius,radius*2+1, radius*2+1)   
            self.rect.union_ip(rect) 
        
        self.original = pygame.surface.Surface([self.rect.width,self.rect.height],SRCALPHA)
                
        for c in particle.collider.colliders:
            radius = int(c.r)
            x = int(c.p.x)
            y = int(c.p.y)
            pygame.gfxdraw.aacircle(self.original, x-self.rect.left,y-self.rect.top,radius,color)
            pygame.gfxdraw.filled_circle(self.original,x-self.rect.left,y-self.rect.top,radius,color)
        
        self.view = self.original
           
        self.update()