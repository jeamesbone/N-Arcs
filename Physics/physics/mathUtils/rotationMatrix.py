'''
Created on 23/09/2012

@author: Robert
'''

import math
from vec import Vec

class RotationMatrix(object):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self.r = 0
        self.setRotation(self.r)
        
    def setRotation(self,r):
        self.r = math.fmod(r,math.pi*2)
        self.row0 = Vec(math.cos(self.r),-math.sin(self.r))
        self.row1 = Vec(math.sin(self.r),math.cos(self.r))
        
    def rotate(self,dr):
        self.setRotation(self.r+dr)
        
    def rotatePoint(self,p):
        return Vec(p.dot(self.row0),p.dot(self.row1))
    
if __name__=="__main__":
    p = Vec(1,0)
    m = RotationMatrix(math.radians(-90))
    
    print m.rotatePoint(p)