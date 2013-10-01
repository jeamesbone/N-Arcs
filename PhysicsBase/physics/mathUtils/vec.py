import math
import operator

class Vec:
    __slots__ = ['x', 'y']
    __hash__ = None

    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __copy__(self):
        return self.__class__(self.x, self.y)

    copy = __copy__

    def __repr__(self):
        return 'Vec(%.2f, %.2f)' % (self.x, self.y)

    def __eq__(self, other):
        return self.x == other[0] and self.y == other[1]

    def __ne__(self, other):
        return not self.__eq__(other)

    def __nonzero__(self):
        return self.x != 0 or self.y != 0

    def __len__(self):
        return 2

    def __getitem__(self, key):
        return (self.x, self.y)[key]

    def __setitem__(self, key, value):
        l = [self.x, self.y]
        l[key] = value
        self.x, self.y = l

    def __iter__(self):
        return iter((self.x, self.y))

    def __add__(self, other):
        return Vec(self.x + other[0],self.y + other[1])
    __radd__ = __add__

    def __iadd__(self, other):
        self.x += other[0]
        self.y += other[1]
        return self

    def __sub__(self, other):
        return Vec(self.x - other[0],self.y - other[1])

    def __rsub__(self, other):
        return Vec(other.x - self[0],other.y - self[1])

    def __mul__(self, other):
        return Vec(self.x * other, self.y * other)
    __rmul__ = __mul__

    def __imul__(self, other):
        self.x *= other
        self.y *= other
        return self

    def __div__(self, other):
        return Vec(operator.div(self.x, other),operator.div(self.y, other))

    def __rdiv__(self, other):
        return Vec(operator.div(other, self.x),operator.div(other, self.y))

    def __floordiv__(self, other):
        return Vec(operator.floordiv(self.x, other),operator.floordiv(self.y, other))

    def __rfloordiv__(self, other):
        return Vec(operator.floordiv(other, self.x), operator.floordiv(other, self.y))

    def __truediv__(self, other):
        return Vec(operator.truediv(self.x, other), operator.truediv(self.y, other))

    def __rtruediv__(self, other):
        return Vec(operator.truediv(other, self.x),operator.truediv(other, self.y))
    
    def __neg__(self):
        return Vec(-self.x,-self.y)

    __pos__ = __copy__
    
    def __abs__(self):
        return math.sqrt(self.x ** 2 +  self.y ** 2)

    magnitude = __abs__

    def magnitude_squared(self):
        return self.x ** 2 + self.y ** 2

    def normalize(self):
        d = math.sqrt(self.x ** 2 +  self.y ** 2)
        if d:
            self.x /= d
            self.y /= d
        return self

    def normalized(self):
        d = math.sqrt(self.x ** 2 +  self.y ** 2)
        if d:
            return Vec(self.x / d, self.y / d)
        return self.copy()

    def dot(self, other):
        return self.x * other.x + self.y * other.y

    def cross(self, other):
        return self.x*other.y - self.y*other.x

    def reflect(self, normal):
        d = 2 * (self.x * normal.x + self.y * normal.y)
        return Vec(self.x - d * normal.x, self.y - d * normal.y)

    def angle(self, other):
        """Return the angle to the vector other"""
        return math.acos(self.dot(other) / (self.magnitude()*other.magnitude()))

    def project(self, other):
        """Return one vector projected on the vector other"""
        n = other.normalized()
        return self.dot(n)*n
