import math

class Arc:
    def __init__(self, pos, radius, start, end):
        self.pos = pos
        self.radius = radius
        self.start = start
        self.end = end
    
    def inArc(self, point):
        transPoint = point - self.pos
        return self.start.cross(transPoint) > 0 and self.end.cross(transPoint) < 0
    
    def copy(self):
        return Arc(self.pos.copy(), self.radius, self.start.copy(), self.end.copy())
    
    def getStart(self):
        return math.atan2(self.start.y, self.start.x)
    
    def getEnd(self):
        return math.atan2(self.end.y, self.end.x)