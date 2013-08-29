'''
Created on 21/09/2012

@author: rollingt
'''

import math
import random

from arc import Arc, worldArc
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
    def __init__(self, particle, n):
        Collider.__init__(self, particle)
        
        posVariance = 40
        radiusVariance = 15
        
        if n == 4:        
			c1 = Vec(random.uniform(-1, 1), random.uniform(-1, 1)) * posVariance
			dist1 = c1.magnitude()
			r1 = dist1 + 2 + random.uniform(0, radiusVariance)
			
			c2 = -c1.copy() / c1.magnitude() * random.uniform(r1 - dist1, posVariance)
			
			dist2 = c2.magnitude()
			r2 = dist2 + 2 + random.uniform(0, radiusVariance)
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

        elif n == 6:
            posVariance = 80
            radiusVariance = 50
            
            #c1 = Vec(random.uniform(-1, 1), random.uniform(-1, 1)) * posVariance
            c1 = Vec(0, 1) * 40
            dist1 = c1.magnitude()
            #r1 = dist1 + 2 + random.uniform(0, radiusVariance)
            r1 = 60
            
            angle = 2 * math.pi / (n / 2)
            print str(angle)
            #c2 = c1.rotated(angle) / c1.magnitude() * random.uniform(0, posVariance / 2)
            c2 = c1.rotated(-angle) / c1.magnitude() * 40
            dist2 = c2.magnitude()
            #r2 = dist2 + 2 + random.uniform(r1, radiusVariance)
            r2 = 60
            
            c3 = c2.rotated(-angle) / c2.magnitude() * 40
            dist3 = c3.magnitude()
            #r3 = dist3 + 2 + random.uniform(r2, radiusVariance)
            r3 = 60

            #maximum = (r1 + r2 + r3 - (dist1 + dist2 + dist3)) / 6
            
            c1c2 = c2 - c1
            c2c3 = c3 - c2
            c3c1 = c1 - c3
			
            c1c2Dir = math.atan2(c1c2.y, c1c2.x)
            c1c2Dist = c1c2.magnitude()
			
            c2c3Dir = math.atan2(c2c3.y, c2c3.x)
            c2c3Dist = c2c3.magnitude()
						
            c3c1Dir = math.atan2(c3c1.y, c3c1.x)
            c3c1Dist = c3c1.magnitude()
			
            #r4 = random.uniform(0, (r1 + r2 - c1c2Dist) / 2)
            #r5 = random.uniform(0, (r2 + r3 - c2c3Dist) / 2)
            #r6 = random.uniform(0, (r3 + r1 - c3c1Dist) / 2)

            r4 = 5
            r5 = 5
            r6 = 5

			# Calculate Angles
            c1c4Angle = calcAngle(r1, r4, r2, c1c2Dist)
            c2c4Angle = calcAngle(r2, r4, r1, c1c2Dist)

            c2c5Angle = calcAngle(r2, r5, r3, c2c3Dist)
            c3c5Angle = calcAngle(r3, r5, r2, c2c3Dist)

            c3c6Angle = calcAngle(r3, r6, r1, c3c1Dist)
            c1c6Angle = calcAngle(r1, r6, r3, c3c1Dist)
            
            print "c1c2Dir:" + str(c1c2Dir)
            print "c1c4Angle:" + str(c1c4Angle)
            
			# Get local angles
            a1 = c1c2Dir - c1c4Angle
            a2 = c3c1Dir + math.pi + c1c6Angle
            a3 = c3c1Dir - c3c6Angle
            a4 = c2c3Dir + math.pi + c3c5Angle
            a5 = c2c3Dir - c2c5Angle
            a6 = c1c2Dir + math.pi + c2c4Angle
			
            print "a1:" + str(a1)
            
            n1 = makeVec(a1)
            n2 = makeVec(a2)
            n3 = makeVec(a3)
            n4 = makeVec(a4)
            n5 = makeVec(a5)
            n6 = makeVec(a6)
						
            c4 = Vec(math.cos(a1), math.sin(a1)) * (r1 - r4) + c1
            c5 = Vec(math.cos(a5), math.sin(a5)) * (r2 - r5) + c2
            c6 = Vec(math.cos(a3), math.sin(a3)) * (r3 - r6) + c3
			
            self.arcs = [Arc(c1, r1, n1, n2),
						 Arc(c6, r6, n2, n3),
						 Arc(c3, r3, n3, n4),
						 Arc(c5, r5, n4, n5),
						 Arc(c2, r2, n5, n6),
						 Arc(c4, r4, n6, n1)]


        self.boundRadius = 0
        for arc in self.arcs:
			radius = abs(self.particle.p - arc.pos) + arc.radius
			if radius > self.boundRadius:
				self.boundRadius = radius
        self.boundRadius = 150
    
    def getCenterOfMass(self):
    	points = []
    	centerOfMass = Vec(0, 0)
    	for arc in self.arcs:
    		centerOfMass += arc.getCenterOfMass()
    		points.append(arc.start)
    	points.append(self.arcs[len(self.arcs)-1].end)
    	
    	area = 0
    	cx = 0
    	cy = 0
    	for i in range(len(points)-1):
    		area += points[i].x * points[i+1] + points[i+1].x * points[i].y
    		cx += (points[i].x + points[i+1].x) * (points[i].x * points[i+1].y - points[i+1].x * points[i].y)
    		cy += (points[i].y + points[i+1].y) * (points[i].x * points[i+1].y - points[i+1].x * points[i].y)
    	area /= 2
    	cx *= 1 / (6 * area)
    	cy *= 1 / (6 * area)
    	
    	centerOfMass += Vec(cx, cy)
    	centerOfMass /= len(self.arcs) + 1
    	return centerOfMass

    def updateWorldArcs(self):
        for arc in self.arcs:
            arc.worldArc = worldArc(arc, self.particle)
    
def calcAngle(r1, r2, r3, c1c2Dist):
    '''print "((r1 - r2) ** 2 + c1c2Dist ** 2 - (r3 - r2) ** 2) = " + str((r1 - r2) ** 2 + c1c2Dist ** 2 - (r3 - r2) ** 2)
    print "(2 * (r1 - r2) * c1c2Dist) = " + str(2 * (r1 - r2) * c1c2Dist)
    print "A / B = " + str(((r1 - r2) ** 2 + c1c2Dist ** 2 - (r3 - r2) ** 2) / (2 * (r1 - r2) * c1c2Dist))'''
    return math.acos(((r1 - r2) ** 2 + c1c2Dist ** 2 - (r3 - r2) ** 2) / (2 * (r1 - r2) * c1c2Dist))

def makeVec(angle):
    return Vec(math.cos(angle), math.sin(angle))
