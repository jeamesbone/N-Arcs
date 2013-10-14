import pyglet
import math
import random

from pyglet.gl import *
from physics.arc import Arc
from physics.collider import Narc, Polygon

def drawObject(obj):
    if isinstance(obj, Narc):
        drawNarc(obj)
    #elif isinstance(obj, Polygon):
        #drawPolygon(obj)

def drawRect(x, y, width, height):
    pyglet.graphics.draw(4, pyglet.gl.GL_LINE_LOOP, 
        ('v2i', (x, y, x + width, y, x + width, y + height, x, y + height))
    ) 

def drawNarc(narc):
    glTranslatef(narc.particle.p.x, narc.particle.p.y, 0.0)
    #r = narc.particle.getRotation()
    #if r: 
    #    glRotatef(math.degrees(r), narc.particle.p.x, narc.particle.p.y, 0.0) 
    for arc in narc.arcs:
        drawArc(arc)

def drawArc(arc, segments=10):
    glColor3f(0.0, 0.0, 0.0)
    glBegin(GL_LINE_STRIP)
    for i in range(segments + 1):
        end = arc.endAngle
        if arc.endAngle < arc.startAngle:
            end += 2 * math.pi
        
        theta = (end - arc.startAngle) * i / segments
        x = arc.radius * math.cos(theta + arc.startAngle)
        y = arc.radius * math.sin(theta + arc.startAngle)
        
        glVertex2f(x + arc.pos.x, y + arc.pos.y)
    glEnd()
    
def drawCircle(cx, cy, radius, segments):
    glBegin(GL_LINE_STRIP)
    for i in range(segments):
        theta = 2 * math.pi * i / segments
        x = r * math.cos(theta)
        y = r * math.sin(theta)
        
        glVertex2f(x + cx, y + cy)
    glEnd()
    