import math as math
class PVector:
    x = 0.0
    y = 0.0
    z = 0.0
    def __init__(self, x, y, z):
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)
    def normalize(self):
        length  = math.sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)
        self.x = self.x / length
        self.y = self.y / length
        self.z = self.z / length
    def add(self, n):
        self.x = self.x + n.x
        self.y = self.y + n.y
        self.z = self.z + n.z
        return self
    def mult(self, scalar):
        self.x = self.x * scalar
        self.y = self.y * scalar
        self.z = self.z * scalar
        return self
    def dot(self, n):
        return self.x * n.x + self.y * n.y + self.z * n.z
    def array(self):
        return [self.x, self.y, self.z]
    