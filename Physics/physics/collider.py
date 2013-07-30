'''
Created on 21/09/2012

@author: rollingt
'''

import math
import random

from arc import Arc
from mathUtils.vec import Vec
        
class Collider(object):
    def __init__(self,particle):
        self.particle = particle
        self.restitution = 1.0

class Circle(Collider):
    def __init__(self,particle,p,r):
        Collider.__init__(self,particle)
        self.p = p 
        self.r = r      
        
class Arena(Collider):
    def __init__(self,particle,width,height):
        Collider.__init__(self,particle)
        self.left = particle.p.x
        self.right = particle.p.x + width
        self.top = particle.p.y
        self.bottom = particle.p.y + height
        
class Union(Collider):
    def __init__(self,particle):
        Collider.__init__(self,particle)
        self.colliders = []  
        
class Polygon(Collider):
    def __init__(self, particle, points):
        Collider.__init__(self,particle)
        self.points = points

class Narc(Collider):
    def __init__(self, particle):
        Collider.__init__(self, particle)
        
        posVariance = 40
        radiusVariance = 15
                
        c1 = Vec(random.uniform(-1, 1), random.uniform(-1, 1)) * posVariance
        dist1 = c1.magnitude()
        r1 = dist1 + 2 + random.uniform(0, radiusVariance)
        
        c2 = -c1.copy() / c1.magnitude() * random.uniform(r1 - dist1, posVariance)
        
        dist2 = c2.magnitude()
        r2 = dist2 + (r1 - dist1)
        maximum = (r1 + r2 - (dist1 + dist2)) * 0.5
        r3 = random.uniform(2, maximum)
        r4 = random.uniform(2, maximum)
    
        c1c2 = c2 - c1
            
        c1c2Dir = math.atan2(c1c2.y, c1c2.x)
        c1c2Dist = c1c2.magnitude()
                    
        c1c3Angle = calcAngle(r1, r3, r2, c1c2Dist)
        c1c4Angle = calcAngle(r1, r4, r2, c1c2Dist)
        c2c3Angle = calcAngle(r2, r3, r1, c1c2Dist)
        c2c4Angle = calcAngle(r2, r4, r1, c1c2Dist)
                    
        a1 = c1c2Dir - c1c3Angle
        a2 = c1c2Dir + c1c4Angle
        a3 = c1c2Dir + math.pi - c2c4Angle
        a4 = c1c2Dir + math.pi + c2c3Angle
        
        n1 = makeVec(a1)
        n2 = makeVec(a2)
        n3 = makeVec(a3)
        n4 = makeVec(a4)
                    
        c3 = Vec(math.cos(a1), math.sin(a1)) * (r1 - r3) + c1
        c4 = Vec(math.cos(a2), math.sin(a2)) * (r1 - r4) + c1
        
        self.arcs = [Arc(c1, r1, n1, n2),
                     Arc(c4, r4, n2, n3),
                     Arc(c2, r2, n3, n4),
                     Arc(c3, r3, n4, n1)]
                     
    	self.boundRadius = 0
        for arc in self.arcs:
        	radius = arc.pos + (arc.radius * (arc.pos.normalized()))
        	if radius > self.boundRadius:
        		self.boundRadius = radius
        
def calcAngle(r1, r2, r3, c1c2Dist):
    return math.acos(((r1 - r2) * (r1 - r2) + c1c2Dist * c1c2Dist - (r3 - r2) * (r3 - r2)) / (2 * (r1 - r2) * c1c2Dist))

def makeVec(angle):
    return Vec(math.cos(angle), math.sin(angle))