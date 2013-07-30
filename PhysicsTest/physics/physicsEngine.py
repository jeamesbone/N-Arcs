'''
Created on 21/09/2012

@author: rollingt
'''
from mathUtils.vec import Vec

class PhysicsEngine(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.moving = []
        self.static = []
        
        self.contactGenerators = []
        self.forceGenerators = []
        
        self.contacts = []
        
        self.gravity = Vec(0,0)
        
    
    def step(self, dt):
        for p in self.moving:
            p.accumulator = Vec(0,0)
            
        for fg in self.forceGenerators:
            fg.update()
            
        for p in self.moving:
            p.integrate(dt)
            
        self.contacts = []
        
        for cg in self.contactGenerators:
            cg.update()
            
        for c in self.contacts:
            c.resolve()
            
            
    