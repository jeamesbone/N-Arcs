'''
Created on 22/09/2012

@author: Robert
'''
import math

from OpenGLContext import testingcontext
BaseContext = testingcontext.getInteractive()

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

class View(BaseContext):
    # OpenGLContext
    objects = []
    initialPosition = (0,0,0)
    
    def setup(self):
        # Constructor
        self.objects = []
        self.ViewPort(800, 600)
    
    def Render(self, mode = 0):
        # Renders geometry in the scene
        BaseContext.Render(self, mode)
        glDisable(GL_CULL_FACE)
        
        for o in self.objects:
            o.draw()

            
        