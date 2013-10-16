import math
import random

class Arc:
    def __init__(self, pos, radius, start, end):
        self.pos = pos
        self.radius = radius
        self.start = start
        self.end = end
        self.worldArc = None
        
        self.startAngle = math.atan2(self.start.y, self.start.x)
        self.endAngle = math.atan2(self.end.y, self.end.x)
        
        self.r = random.random()
        self.g = random.random()
        self.b = random.random()
        
    def inArc(self, point):
        transPoint = point - self.pos
        return self.start.cross(transPoint) > 0 and self.end.cross(transPoint) < 0
    
    def copy(self):
        return Arc(self.pos.copy(), self.radius, self.start.copy(), self.end.copy())
    
    def getStart(self):
        return self.startAngle
    
    def getEnd(self):
        return self.endAngle
    
    def getCenterOfMass(self):
    	theta = endAngle - startAngle
    	# Gets radius of the center of mass of the circle segment
    	comArcRadius = 4 * radius * (math.sin(theta / 2) ** 3)
    	comArcRadius /= 3 * (theta - math.sin(theta))
    	
    	midAngle = (self.startAngle + self.endAngle) / 2
    	midPoint = self.pos + (makeVec(midAngle) * comArcRadius)
    	return midPoint

def makeVec(angle):
    return Vec(math.cos(angle), math.sin(angle))

def worldArc(arc, particle):
    position = particle.getPosition()
    rotation = particle.getRotationMatrix()
    
    return Arc(position + rotation.rotatePoint(arc.pos),
               arc.radius,
               rotation.rotatePoint(arc.start),
               rotation.rotatePoint(arc.end))