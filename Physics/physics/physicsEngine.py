'''
Created on 21/09/2012

@author: rollingt
'''

import math
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
        
        self.cells = []
        self.initHash()
        
    
    def step(self, dt):   
    
        for p in self.moving:
            p.accumulator = Vec(0,0)
            
        for fg in self.forceGenerators:
            fg.update()
            
        for p in self.moving:
            p.integrate(dt)
            
        self.contacts = []
        
        # Spatial hashing stuff
        '''self.clearCells()
        for o in self.moving:
        	self.addObjectToCells(o) '''
        
        for cg in self.contactGenerators:
            cg.update()
            
        for c in self.contacts:
            c.resolve()
            
    def initHash(self):
    	self.cellSize = 200
    	cols = 600 / self.cellSize
    	rows = 600 / self.cellSize
    	for i in range(cols * rows):
    		self.cells.append([])
    
    def clearCells(self):
		self.cells = []
		cols = 600 / self.cellSize
		rows = 600 / self.cellSize
		for i in range(cols * rows):
			self.cells.append([])
    
    def addObjectToCells(self, object):
    	inCells = self.getCellsForObject(object)
    	for c in inCells:
    		if c < len(self.cells):
				self.cells[c].append(object)
    				
    def getCellsForObject(self, object):
    	inCells = []
    	min = Vec(	object.p.x - object.boundRadius, 
    				object.p.y - object.boundRadius)
    	max = Vec(	object.p.x + object.boundRadius, 
    				object.p.y + object.boundRadius)
    	
    	self.addCell(min, inCells)
    	self.addCell(Vec(max.x, min.y), inCells)
    	self.addCell(Vec(min.x, max.y), inCells)
    	self.addCell(max, inCells)
    	
    	return inCells
    	
    def addCell(self, p, inCells):
    	width = 600 / self.cellSize
    	cellPosition = int( math.floor(p.x / self.cellSize) +
    						math.floor(p.y / self.cellSize) * width)
    	if cellPosition not in inCells:
    		inCells.append(cellPosition)
    	
    def getNearby(self, object):
    	objects = []
    	inCells = self.getCellsForObject(object)
    	for c in inCells:
    		objects.extend(self.cells[c])
    	return objects
    	
    	
    	
            
            
    