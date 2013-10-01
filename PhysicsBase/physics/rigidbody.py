'''
Created on 23/09/2012

@author: Robert
'''
import math

from mathUtils.vec import Vec
from mathUtils.rotationMatrix import RotationMatrix

class Rigidbody(object):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self.p = Vec(0,0)
        self.mat = RotationMatrix()
        self.v = Vec(0,0)
        self.w = 0
        self.invmass = 1.0
        self.invmoi = 1.0
        self.accumulator = Vec(0,0)
        self.torqueAccumulator = 0
        self.collider = None
        self.engine = None
        
    def worldPosition(self,point):
        return self.p + self.mat.rotatePoint(point)
    
    def worldVelocity(self,worldPoint):
        point = worldPoint - self.p
        return self.v + Vec(point.y*-self.w, point.x*self.w)
        
    def integrate(self, dt):
        self.p += self.v * dt
        self.mat.rotate(self.w*dt)
        
        a = self.accumulator * self.invmass
        wa = self.torqueAccumulator * self.invmoi
        if self.engine:
            a += self.engine.gravity
        
        self.v += a*dt
        self.w += wa*dt
        
    def deltaVperImpulse(self, worldPoint, normal):
        point = worldPoint - self.p
        #linear
        deltaV = self.invmass
        
        #rotation
        torque = point.cross(normal)
        deltaW =  torque * self.invmoi
        
        deltaV += Vec(point.y*-deltaW, point.x*deltaW).dot(normal)
        
        return deltaV
    
    def getPosition(self):
        return self.p
    
    def getRotation(self):
        return self.mat.r
    
    def getRotationMatrix(self):
        return self.mat
    
    def applyImpulse(self,worldPoint,impulse):
        point = worldPoint - self.p
        
        self.v += impulse * self.invmass
        
        self.w += point.cross(impulse) * self.invmoi
        
        
        