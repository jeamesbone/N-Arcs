'''
Created on 21/09/2012

@author: Jeames Bone
'''

import math
from arc import Arc
from collider import Narc
from PIL import Image

def run:
    image = getImage("testRect.jpg")


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
    return 0


	
	

	
