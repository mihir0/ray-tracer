from PVector import PVector
class Hit:
    intersection_point = (0.0, 0.0, 0.0)
    surface = (0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
    surface_normal = PVector(0, 0, 0)
    t = 0.0
    def __init__(self, intersection_point, surface, surface_normal, t):
        self.intersection_point = intersection_point
        self.surface = surface
        self.surface_normal = surface_normal
        self.t = t
    def getPosition(self):
        return self.intersection_point
    def getSurface(self):
        return self.surface
    def getSurfaceNormal(self):
        return self.surface_normal