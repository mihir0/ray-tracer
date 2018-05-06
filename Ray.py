from operator import itemgetter
from Hit import Hit
class Ray:
    dx = 0.0
    dy = 0.0
    dz = 0.0
    origin = [0.0, 0.0, 0.0]
    def __init__(self, direction_vector, origin=[0.0, 0.0, 0.0]):
        self.dx = direction_vector[0]
        self.dy = direction_vector[1]
        self.dz = direction_vector[2]
        self.origin = origin
    '''
    takes in an object (sphere or cylinder), and returns a hit if it intersects
    returns None if it hits nothing
    '''
    def getIntersectionHit(self, obj):
        if obj[0] == 'sphere':
            hit = self.getSphereHit(obj)
        elif obj[0] == 'cylinder':
            hit = self.getCylinderHit(obj)
        return hit
    def getSphereHit(self, obj):
        #Part A: generate implicit sphere eq. (plug in ray info)
        a = self.dx ** 2 + self.dy ** 2 + self.dz ** 2
        #b = 2 * ((0 * self.dx - obj[1] * self.dx) + (0 * self.dy - obj[2] * self.dy) + (0 * self.dz - obj[3] * self.dz))
        b = 2 * ((self.origin[0] * self.dx - obj[1] * self.dx) + (self.origin[1] * self.dy - obj[2] * self.dy) + (self.origin[2] * self.dz - obj[3] * self.dz))
        #c = (0 - obj[1]) ** 2 + (0 - obj[2]) ** 2 + (0 - obj[3]) ** 2 - obj[4] ** 2
        c = ((self.origin[0] - obj[1]) ** 2) + ((self.origin[1] - obj[2]) ** 2) + ((self.origin[2] - obj[3]) ** 2) - (obj[4] ** 2)
        
        #Part B: is there an intersection?
        if (b**2 - 4 * a * c < 0): #no intersection
            return None
        else:
            #Part C: find t, position, surface normal, and surface material where intersection occurs
            t_pos = (-1 * b + sqrt(b**2 - 4 * a * c))/(2 * a)
            t_neg = (-1 * b - sqrt(b**2 - 4 * a * c))/(2 * a)
            if (t_pos > t_neg and t_neg > 0):
                t = t_neg
            else:
                t = t_pos
            if t <= 0:
                return None
            #print("t_pos:", t_pos, "t_neg:", t_neg)
            intersection_point = (self.origin[0] + self.dx * t, self.origin[1] + self.dy * t, self.origin[2] + self.dz * t)
            #intersection_point = (self.dx * t, self.dy * t, self.dz * t)

            n = PVector(intersection_point[0] - obj[1], intersection_point[1] - obj[2], intersection_point[2] - obj[3])
            n.normalize()
            hit = Hit(intersection_point, obj[5], n, t)
            return hit
        
    def getCylinderHit(self, obj):
        t_body = -10000
        t_min_end = -10000
        t_max_end = -10000
        #BODY intersection
        #same as sphere implicit eq. WITHOUT y terms
        a = self.dx ** 2 + self.dz ** 2
        #b = 2 * ((0 * self.dx - obj[2] * self.dx) + (0 * self.dz - obj[3] * self.dz)) #cylinder's x, z
        b = 2 * ((self.origin[0] * self.dx - obj[2] * self.dx) + (self.origin[2] * self.dz - obj[3] * self.dz)) #cylinder's x, z
        #c = (0 - obj[2]) ** 2 + (0 - obj[3]) ** 2 - obj[1] ** 2 #cylinder's x, y, radius 
        c = (self.origin[0] - obj[2]) ** 2 + (self.origin[1] - obj[3]) ** 2 - obj[1] ** 2 #cylinder's x, y, radius        
        if (b**2 - 4 * a * c >= 0):
            t_pos = (-1 * b + sqrt(b**2 - 4 * a * c))/(2 * a)
            t_neg = (-1 * b - sqrt(b**2 - 4 * a * c))/(2 * a)
            if (t_pos > t_neg and t_neg > 0):
                t = t_neg
            else:
                t = t_pos
            #if t > 0 and (self.dy * t >= obj[4] and self.dy * t <= obj[5]): #Check that the y-value at t is within cylinder bounds...
            if t > 0 and (self.dy * t + self.origin[1] >= obj[4] and self.dy * t + self.origin[1] <= obj[5]): #Check that the y-value at t is within cylinder bounds...
                t_body = t
        #ENDCAP intersections
        if self.dy != 0:
            #YMIN endcap
            #t = obj[4]/self.dy
            t = (obj[4] - self.origin[1])/self.dy
            #x = self.dx * t
            x = self.dx * t + self.origin[0]
            #z = self.dz * t
            z = self.dz * t + self.origin[2]
            if sqrt((obj[2] - x) ** 2 + (obj[3] - z) ** 2) <= obj[1]: #if (x, z) is within circle
                t_min_end = t
            #YMAX endcap
            #t = obj[5]/self.dy
            t = (obj[5] - self.origin[1])/self.dy
            #x = self.dx * t
            x = self.dx * t + self.origin[0]
            #z = self.dz * t
            z = self.dz * t + self.origin[2]
            if sqrt((obj[2] - x) ** 2 + (obj[3] - z) ** 2) <= obj[1]: #if (x, z) is within circle
                #print "WITHIN CIRCLE, t_max_end:", t, "t_body", t_body
                t_max_end = t
        
        #Sort by minimum t distance
        t_vals = [(t_body, 'body'), (t_min_end, 'min_end'), (t_max_end, 'max_end')]
        t_vals = sorted(t_vals, key=itemgetter(0), reverse=False)
        for i in range(0, 3):
            if t_vals[i][0] > 0: # if t is valid (> 0)
                #intersection_point = (self.dx * t_vals[i][0], self.dy * t_vals[i][0], self.dz * t_vals[i][0])
                intersection_point = (self.dx * t_vals[i][0] + self.origin[0], self.dy * t_vals[i][0]  + self.origin[1], self.dz * t_vals[i][0] + self.origin[2])
                if t_vals[i][1] == 'body':        
                    n = PVector(intersection_point[0] - obj[2], 0, intersection_point[2] - obj[3])
                elif t_vals[i][1] == 'min_end':
                    #print "min_end"
                    n = PVector(0, -1, 0)
                elif t_vals[i][1] == 'max_end':
                    #print "max_end"
                    n = PVector(0, 1, 0)
                n.normalize()
                hit = Hit(intersection_point, obj[6], n, t)
                return hit
        return None