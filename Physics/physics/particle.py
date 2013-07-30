'''
Created on 21/09/2012

@author: rollingt
'''

from mathUtils.rotationMatrix import RotationMatrix
from mathUtils.vec import Vec

class Particle(object):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self.p = Vec(0,0)
        self.v = Vec(0,0)
        self.invmass = 1.0
        self.accumulator = Vec(0,0)
        
        self.collider = None
        self.engine = None
        
    def integrate(self, dt):
        self.p += self.v * dt
        
        a = self.accumulator * self.invmass
        if self.engine:
            a += self.engine.gravity
        
        self.v += a*dt
        
    def getRotation(self):
        return None;
        
    def deltaVperImpulse(self, point, normal):
        return self.invmass
    
    def applyImpulse(self, point, impulse):
        self.v += impulse * self.invmass
    
    def worldPosition(self,point):
        return self.p + point
    
    def worldVelocity(self,point):
        return self.v
        
        
        
    