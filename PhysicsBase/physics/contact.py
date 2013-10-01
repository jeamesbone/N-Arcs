'''
Created on 22/09/2012

@author: Robert
'''

from collider import Circle, Union, Arena, Polygon, Narc
from mathUtils.vec import Vec
import sys

class Contact(object):
    def __init__(self,p1,p2,worldpos,n,penetration,restitution):
        self.p1 = p1
        self.p2 = p2
        self.worldpos = worldpos
        self.normal = n
        self.penetration = penetration
        self.restitution = restitution
        
    def resolve(self):
        self.resolveVelocity()
        self.resolvePenetration()
    
    def resolveVelocity(self):
        relV = (self.p1.worldVelocity(self.worldpos) - self.p2.worldVelocity(self.worldpos)).dot(self.normal)
        
        deltaV = -relV - relV * self.restitution
        deltaVperImpulse = self.p1.deltaVperImpulse(self.worldpos, self.normal) + self.p2.deltaVperImpulse(self.worldpos, self.normal)
        impulse = deltaV / deltaVperImpulse
        
        impulseVec = impulse * self.normal
        
        self.p1.applyImpulse(self.worldpos,impulseVec)
        self.p2.applyImpulse(self.worldpos,-impulseVec)
        
    def resolvePenetration(self):
        if self.penetration<0:
            return
        
        totalIMass = self.p1.invmass + self.p2.invmass
            
        delta = self.normal * self.penetration / totalIMass * 0.75
        self.p1.p -= delta * self.p1.invmass
        self.p2.p += delta * self.p2.invmass
            
            
def collide(a,b):
    if isinstance(a,Circle) and isinstance(b,Circle):
        return collideCircleCircle(a,b)
    if isinstance(a,Polygon) and isinstance(b,Polygon):
        return collidePolyPoly(a,b)
    if isinstance(a,Narc) and isinstance(b,Narc):
        return collideNarcNarc(a,b)
    if isinstance(a,Circle) and isinstance(b,Arena):
        return collideCircleArena(a,b)
    if isinstance(a,Polygon) and isinstance(b,Arena):
        return collidePolyArena(a,b)
    if isinstance(a,Narc) and isinstance(b,Arena):
        return collideNarcArena(a,b)
    if isinstance(a,Union):
        return collideUnionCollider(a,b)
    if isinstance(b,Union):
        return collideColliderUnion(a,b)
    return []
        
        
def collideCircleCircle(c1,c2):
    wp1 = c1.particle.worldPosition(c1.p)
    wp2 = c2.particle.worldPosition(c2.p)
    
    separation = wp2 - wp1
    distance = separation.magnitude()
    penetration = c1.r + c2.r - distance
    if penetration>0:
        normal = separation.normalized()
        return [Contact(c1.particle,c2.particle,wp1+normal*c1.r,normal,penetration,(c1.restitution + c2.restitution)/2)]
    return []

def collideCircleArena(c,arena):
    contacts = []
    
    wpc = c.particle.worldPosition(c.p)
    
    if wpc.x<arena.left+c.r:
        contacts += [Contact(c.particle,arena.particle,Vec(arena.left,wpc.y),Vec(-1,0),(arena.left + c.r) - wpc.x,(c.restitution + arena.restitution)/2)]
    if wpc.x>arena.right-c.r:
        contacts += [Contact(c.particle,arena.particle,Vec(arena.right,wpc.y),Vec(1,0), wpc.x - (arena.right - c.r),(c.restitution + arena.restitution)/2)]
    if wpc.y<arena.top+c.r:
        contacts += [Contact(c.particle,arena.particle,Vec(wpc.x,arena.top),Vec(0,-1), (arena.top + c.r) - wpc.y,(c.restitution + arena.restitution)/2)]
    if wpc.y>arena.bottom-c.r:
        contacts += [Contact(c.particle,arena.particle,Vec(wpc.x,arena.bottom),Vec(0,1), wpc.y - (arena.bottom - c.r),(c.restitution + arena.restitution)/2)]
    
    return contacts

def collideColliderUnion(c1,u):
    contacts = []
    for c2 in u.colliders:
        contacts += collide(c1,c2)
    
    return contacts

def collideUnionCollider(u,c2):
    contacts = []
    for c1 in u.colliders:
        contacts += collide(c1,c2)
    
    return contacts

def collidePolyPoly(p1,p2):
    contacts = []
    
    points1 = [p1.particle.worldPosition(p) for p in p1.points]
    points2 = [p2.particle.worldPosition(p) for p in p2.points]
    
    p1len = len(points1)
    p2len = len(points2)
    
    edge1 = [(points1[(i+1)%p1len] - points1[i]) for i in range(p1len)]
    edge2 = [(points2[(i+1)%p2len] - points2[i]) for i in range(p2len)]
    perp1 = [Vec(-p.y,p.x).normalized() for p in edge1]
    perp2 = [Vec(-p.y,p.x).normalized() for p in edge2]
        
    minpen = sys.float_info.max
    minnorm = Vec(0,0)    
    minpoint = Vec(0,0)
    
    i=0    
    while minpen>0 and i<p2len:
        maxpen = 0
        maxpoint = Vec(0,0)
        maxnorm = Vec(0,0)    
        for j in range(p1len):
            pen = (points1[j]-points2[i]).dot(perp2[i])
            if pen>maxpen:
                maxpen = pen
                maxpoint = points1[j]
                maxnorm = perp2[i]  
                
        if maxpen<minpen:
            minpen = maxpen
            minnorm = maxnorm
            minpoint = maxpoint
            
        i += 1 
            
    i=0      
    while minpen>0 and i<p1len:
        maxpen = 0
        maxpoint = Vec(0,0)
        maxnorm = Vec(0,0)    
        for j in range(p2len):
            pen = (points2[j]-points1[i]).dot(perp1[i])
            if pen>maxpen:
                maxpen = pen
                maxpoint = points2[j]
                maxnorm = -perp1[i]  
                
        if maxpen<minpen:
            minpen = maxpen
            minnorm = maxnorm
            minpoint = maxpoint
        i += 1 
          
    if minpen>0:
        return [Contact(p1.particle,p2.particle,minpoint,minnorm,minpen,(p1.restitution + p2.restitution)/2)]
    else:
        return []
    

def collidePolyArena(p,arena):
    points = [p.particle.worldPosition(point) for point in p.points]
    contacts = []
    
    minx = Vec(sys.float_info.max,0)
    maxx = Vec(-sys.float_info.max,0)
    miny = Vec(0,sys.float_info.max)
    maxy = Vec(0,-sys.float_info.max)
    
    for i in range(len(points)):
        if points[i].x<minx.x: 
            minx = points[i]
        if points[i].x>maxx.x: 
            maxx = points[i]
        if points[i].y<miny.y: 
            miny = points[i]
        if points[i].y>maxy.y: 
            maxy = points[i]
        
    if minx.x<arena.left:
        contacts += [Contact(p.particle,arena.particle,minx,Vec(-1,0),arena.left-minx.x,(p.restitution + arena.restitution)/2)]
    if maxx.x>arena.right:
        contacts += [Contact(p.particle,arena.particle,maxx,Vec(1,0), maxx.x-arena.right,(p.restitution + arena.restitution)/2)]
    if miny.y<arena.top:
        contacts += [Contact(p.particle,arena.particle,miny,Vec(0,-1), arena.top - miny.y,(p.restitution + arena.restitution)/2)]
    if maxy.y>arena.bottom:
        contacts += [Contact(p.particle,arena.particle,maxy,Vec(0,1), maxy.y-arena.bottom,(p.restitution + arena.restitution)/2)]
    
    return contacts

def collideNarcNarc(n1, n2):
    contacts = []
    
    for a1 in n1.arcs:
        a1 = worldArc(a1, n1.particle)
        for a2 in n2.arcs:
            a2 = worldArc(a2, n2.particle)
            sep = a1.pos - a2.pos
            if a1.inArc(a2.pos) and a2.inArc(a1.pos):
                length = sep.magnitude()
                penetration = a1.radius + a2.radius - length
                sep /= length
                contacts += [Contact(n1.particle, n2.particle, a2.pos + sep * (a2.radius - penetration / 2), -sep, penetration, (n1.restitution + n2.restitution) / 2)]
    if len(contacts) == 0:
        return []
    else:
        minContact = contacts[0]
        for i in range(1, len(contacts)):
            if contacts[i].penetration < minContact.penetration:
                minContact = contacts[i]
        if minContact.penetration > 0:
            return [minContact]
        else:
            return []
        
def collideNarcArena(narc, arena):
    for arc in narc.arcs:
        arc = worldArc(arc, narc.particle)
        
        if arc.inArc(arc.pos + Vec(-1, 0)):
            if arc.pos.x - arc.radius < arena.left:
                return [Contact(narc.particle, arena.particle, Vec(arena.left, arc.pos.y), Vec(-1, 0), arena.left + arc.radius - arc.pos.x, (narc.restitution + arena.restitution) / 2)]
        if arc.inArc(arc.pos + Vec(1, 0)):
            if arc.pos.x + arc.radius > arena.right:
                return [Contact(narc.particle, arena.particle, Vec(arena.right, arc.pos.y), Vec(1, 0), arc.pos.x - (arena.right - arc.radius), (narc.restitution + arena.restitution) / 2)]
        if arc.inArc(arc.pos + Vec(0, -1)):
            if arc.pos.y - arc.radius < arena.top:
                return [Contact(narc.particle, arena.particle, Vec(arc.pos.x, arena.top), Vec(0, -1), arena.top + arc.radius - arc.pos.y, (narc.restitution + arena.restitution) / 2)]
        if arc.inArc(arc.pos + Vec(0, 1)):
            if arc.pos.y + arc.radius > arena.bottom:
                return [Contact(narc.particle, arena.particle, Vec(arc.pos.x, arena.bottom), Vec(0, 1), arc.pos.y - (arena.bottom - arc.radius), (narc.restitution + arena.restitution) / 2)]
    return []

def worldArc(arc, particle):
    position = particle.getPosition()
    rotation = particle.getRotationMatrix()
    
    arc = arc.copy()
    
    arc.pos = position + rotation.rotatePoint(arc.pos)
    arc.start = rotation.rotatePoint(arc.start)
    arc.end = rotation.rotatePoint(arc.end)
    
    return arc