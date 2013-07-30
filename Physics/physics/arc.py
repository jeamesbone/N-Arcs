import math

class Arc:
    def __init__(self, pos, radius, start, end):
        self.pos = pos
        self.radius = radius
        self.start = start
        self.end = end
        
        self.startAngle = math.atan2(self.start.y, self.start.x)
        self.endAngle = math.atan2(self.end.y, self.end.x)
        
    def inArc(self, point):
        transPoint = point - self.pos
        return self.start.cross(transPoint) > 0 and self.end.cross(transPoint) < 0
    
    def copy(self):
        return Arc(self.pos.copy(), self.radius, self.start.copy(), self.end.copy())
    
    def getStart(self):
        return self.startAngle
    
    def getEnd(self):
        return self.endAngle