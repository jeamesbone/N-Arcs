'''
Created on 21/09/2012

@author: Jeames Bone
'''

import math
from physics.arc import Arc
from physics.collider import Narc, Polygon
from physics.particle import Particle
from PIL import Image

import mahotas
from scipy import ndimage

def run():
    image = getImage("annealing/testRect.jpg")
    #imread('annealing/testRect.png')
    getCoverage(Narc(Particle(), 4), image)

def getImage(imagePath):
    image = Image.open(imagePath)
    return image

def acceptanceProbibility(energy, newEnergy, temperature):
	if (newEnergy < energy):
		return 1.0
	
	return math.exp((energy - newEnergy) / temperature)

def getBest(temp, coolingRate, nArcs, image):
	currentSolution = Narc(n)
	best = currentSolution
	
	while temp > 1:
		newSolution = Narc(currentSolution)
		# Make change to solution
		
		newEnergy = getCoverage(newSolution, image)
		currentEnergy = getCoverage(currentSolution, image)
	
		if acceptanceProbability(currentEnergy, newEnergy, temp) > math.random:
			currentSolution = Narc(newSolution)
			
		if getCoverage(currentSolution) < getCoverage(best):
			best = Narc(currentSolution)
		
		temp *= 1-coolingRate
		
	return best
	
def getCoverage(narc, image):
    width, height = image.size
    coverage = 0
    
    pixels = image.load()
    
    for x in range(width):
        for y in range(height):
            pixel = pixels[x, y]
            pos = Vec(x, y)
            print pixel
            inside = False
            for arc in narc:
                if arc.inArc(pos):
                    inside = True
                    break
        
            # if pixel is in the image
            if pixel[3] != 0:
                if inside:
                    coverage += 1
                else:
                    coverage -= 1
            else:
                if inside:
                    coverage -= 1

    if coveragecount == 0:
        return 0
    else:
        return pixelcount / coveragecount

def pointinpolygon(point,poly):
    points = poly.points
    n = len(poly.points)
    inside = False
    
    p1x,p1y = points[0].x, poly[0].y
    for i in range(n+1):
        p2x,p2y = poly[i % n].x, poly[i % n].y
        if y > min(p1y,p2y):
            if y <= max(p1y,p2y):
                if x <= max(p1x,p2x):
                    if p1y != p2y:
                        xinters = (y-p1y)*(p2x-p1x)/(p2y-p1y)+p1x
                    if p1x == p2x or x <= xinters:
                        inside = not inside
        p1x,p1y = p2x,p2y
    return inside
	
	

	
