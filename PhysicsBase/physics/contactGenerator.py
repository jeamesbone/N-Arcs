'''
Created on 21/09/2012

@author: rollingt
'''
from itertools import combinations
import contact

class ContactGenerator(object):
    '''
    classdocs
    '''


    def __init__(self, engine):
        '''
        Constructor
        '''
        self.engine = engine
        
    
    def update(self):
        for p1, p2 in combinations(self.engine.moving,2):
            if p1.collider and p2.collider:
                self.engine.contacts += contact.collide(p1.collider,p2.collider)
                    
        for m in self.engine.moving:
            for s in self.engine.static:
                if m.collider and s.collider:
                    contacts = contact.collide(m.collider,s.collider)
                    for c in contacts:
                        c.p2static = True
                    self.engine.contacts += contacts
                        
                
            
                    