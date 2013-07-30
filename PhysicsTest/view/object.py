'''
Created on 22/09/2012

@author: Robert
'''
import math

from physics.mathUtils.vec import Vec
from physics.contact import worldArc

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

class PhysicsObject():
    def __init__(self,particle):
        '''
        Constructor
        '''
        self.particle = particle
        
class CircleObject(PhysicsObject):
    def __init__(self,particle,color):
        PhysicsObject.__init__(self,particle)
    
    def rotate(self):
        pass
        
class PolyObject(PhysicsObject):
    def __init__(self,particle,color):
        PhysicsObject.__init__(self,particle)
        

class NarcObject(PhysicsObject):
    def __init__(self, particle):
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
        
    def draw(self):
        print self.particle.p
        for arc in self.particle.collider.arcs:
            wArc = worldArc(arc, self.particle)
            glTranslatef(wArc.pos.x, 0.0, wArc.pos.y)
            
            num_segments = 10
            theta = wArc.getEnd() / num_segments
            
            glColor3f(0.5, 0.5, 1.0)
            glBegin(GL_LINE_STRIP) # since the arc is not a closed curve, this is a strip now
            
            glVertex2f(wArc.pos.x, wArc.pos.y)
            
            for i in range(num_segments):
                x = wArc.radius * math.cos(wArc.getStart() + (theta * i))
                y = wArc.radius * math.sin(wArc.getStart() + (theta * i))
                glVertex2f(x, y)
            
            glVertex2f(wArc.pos.x, wArc.pos.y)
            
            glEnd()

class CircleUnionObject(PhysicsObject):
    def __init__(self,particle,color):
        PhysicsObject.__init__(self, particle)