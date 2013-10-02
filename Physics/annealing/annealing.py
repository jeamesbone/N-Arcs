'''
Created on 21/09/2012

@author: Jeames Bone
'''

import random
import math
from physics.arc import Arc
from physics.collider import Narc, Polygon
from physics.particle import Particle
from physics.mathUtils.vec import Vec
from PIL import Image

def getImage(imagePath):
    image = Image.open(imagePath)
    return image

def acceptanceProbability(energy, newEnergy, temperature):
    if (newEnergy < energy):
        return 1.0
	
    return math.exp((energy - newEnergy) / temperature)

def getBest(temp, coolingRate, n, image):
    currentSolution = Narc(Particle(), n)
    best = currentSolution

    while temp > 1:
        newSolution = Narc(Particle(), n)
        '''try: 
            newSolution = newSolution.altered(currentSolution)
        except ValueError:
            print "Error"
            continue'''
        
        newEnergy = getCoverage(newSolution, image)
        currentEnergy = getCoverage(currentSolution, image)
        print "Old: " + str(currentEnergy)
        print "New: " + str(newEnergy)	     
        
        if acceptanceProbability(currentEnergy, newEnergy, temp) > random.random():
            currentSolution = newSolution
            print "Accepted solution"
        else:
            print "Did not accept solution"
			
        if getCoverage(currentSolution, image) < getCoverage(best, image):
            best = Narc(currentSolution)
		
        temp *= 1-coolingRate

    return best
	
def getCoverage(narc, image):
    width, height = image.size
    coverage = 0
    
    print "Width" + str(width)
    print "Height" + str(height)
    
    pixels = image.load()
    
    narcPoly = narc.getPoly()
    
    for x in range(width):
        for y in range(height):
            pixel = pixels[x, y]
            pos = Vec(x, y)
            inside = False
            inside = pointinpolygon(pos, narcPoly)
            r, g, b, a = pixel
            
            # if pixel is in the image
            if inside:
                print "alpha: " + str(a)
                print "indside: " + str(inside)
            if a > 0:
                if inside:
                    coverage += 1
                else:
                    coverage -= 1
            else:
                if inside:
                    coverage -= 1
    print "Coverage:" + str(coverage)
    return coverage

def pointinpolygon(point,poly):
    points = poly.points
    n = len(poly.points)
    inside = False
    
    p1x,p1y = points[0].x, points[0].y
    for i in range(n+1):
        p2x,p2y = points[i % n].x, points[i % n].y
        if point.y > min(p1y,p2y):
            if point.y <= max(p1y,p2y):
                if point.x <= max(p1x,p2x):
                    if p1y != p2y:
                        xinters = (point.y-p1y)*(p2x-p1x)/(p2y-p1y)+p1x
                    if p1x == p2x or point.x <= xinters:
                        inside = not inside
        p1x,p1y = p2x,p2y
    return inside
	
