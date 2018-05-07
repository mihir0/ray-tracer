# Author: Mihir Parshionikar
from Ray import Ray
from Hit import Hit
from operator import itemgetter
import numpy as np
import math as math
from PIL import Image
from PVector import PVector
import sys #for progress bar printing
import time
def setup():
    size(300, 300)
    noStroke()
    colorMode(RGB, 1.0)  # Processing color values will be in [0, 1]  (not 255)
    background(0, 0, 0)

# read and interpret the appropriate scene description .cli file based on key press
def keyPressed(key):
    if key == '1':
        interpreter("i1.cli")
    elif key == '2':
        interpreter("i2.cli")
    elif key == '3':
        interpreter("i3.cli")
    elif key == '4':
        interpreter("i4.cli")
    elif key == '5':
        interpreter("i5.cli")
    elif key == '6':
        interpreter("i6.cli")
    elif key == '7':
        interpreter("i7.cli")
    elif key == '8':
        interpreter("i8.cli")
    elif key == '9':
        interpreter("i9.cli")
    elif key == '0':
        interpreter("i10.cli")
    else:
        exit()

def interpreter(fname):
    global light_list, sphere_list, cylinder_list, object_list, bgcolor,surface, fov
    light_list = []
    sphere_list = []
    cylinder_list = []
    object_list = []
    bgcolor = (0,0,0)
    fname = "data/" + fname
    # read in the lines of a file
    with open(fname) as f:
        lines = f.readlines()

    for line in lines:
        words = line.split()  # split the line into individual tokens
        if len(words) == 0:   # skip empty lines
            continue
        if words[0] == 'sphere':
            x = float(words[1])
            y = float(words[2])
            z = float(words[3])
            radius = float(words[4])
            object_list.append(('sphere', x, y, z, radius, surface))
        elif words[0] == 'fov':
            fov = float(words[1])
        elif words[0] == 'background':
            bgcolor = (float(words[1]), float(words[2]), float(words[3]))
        elif words[0] == 'light':
            light_list.append((float(words[1]), float(words[2]), float(words[3]), float(words[4]), float(words[5]), float(words[6])))
        elif words[0] == 'surface':
            surface = (float(words[1]), float(words[2]), float(words[3]), float(words[4]),
                       float(words[5]), float(words[6]), float(words[7]), float(words[8]),
                       float(words[9]), float(words[10]), float(words[11]))
        elif words[0] == 'cylinder':
            radius = float(words[1])
            x = float(words[2])
            z = float(words[3])
            ymin = float(words[4])
            ymax = float(words[5])
            object_list.append(('cylinder', radius, x, z, ymin, ymax, surface))
            
        elif words[0] == 'write':
            render_scene()    # render the scene
            
def getHitShadingColor(hit):
    global light_list
    intersection_point = hit.getPosition()
    surface = hit.getSurface()
    n = hit.getSurfaceNormal()
    
    r_diffuse = 0.0
    g_diffuse = 0.0
    b_diffuse = 0.0
    
    r_specular = 0.0
    g_specular = 0.0
    b_specular = 0.0

    s_ambient_color = (surface[0], surface[1], surface[2])
    s_diffuse_color = (surface[3], surface[4], surface[5])
    s_specular_color = (surface[6], surface[7], surface[8])
    s_phong_exp = surface[9]
    s_refl_coef = surface[10]
    for light in light_list:
        l_vec = PVector(light[3] - intersection_point[0], light[4] - intersection_point[1], light[5] - intersection_point[2])
        l_vec.normalize()
        
        shadow_vec = PVector(light[3] - intersection_point[0], light[4] - intersection_point[1], light[5] - intersection_point[2])
        shadow_vec.normalize()
        offset = 1E-6
        shadow_ray = Ray((shadow_vec.x, shadow_vec.y, shadow_vec.z), origin = [intersection_point[0] + n.x * offset, intersection_point[1] + n.y * offset, intersection_point[2] + n.z * offset])
        shadow_hit = intersect_scene(shadow_ray)
        
        #find max t-value for when shadow_ray hits light source
        light_t = 0
        if (shadow_vec.x != 0):
            light_t = (light[3] - intersection_point[0])/shadow_vec.x
        elif (shadow_vec.y != 0):
            light_t = (light[4] - intersection_point[1])/shadow_vec.y
        elif (shadow_vec.z != 0):
            light_t = (light[5] - intersection_point[2])/shadow_vec.z
        
        if (shadow_hit is None) or (shadow_hit.t >= light_t):
            l_color = (light[0], light[1], light[2])
            #diffuse term==============================
            intensity = l_vec.dot(n)
            r_diffuse += l_color[0] * max(0, intensity)
            g_diffuse += l_color[1] * max(0, intensity)
            b_diffuse += l_color[2] * max(0, intensity)
            
            #specular term =============================
            #part 1: create halfway_vec
            half_vec = PVector(0 - intersection_point[0], 0 - intersection_point[1], 0 - intersection_point[2])
            half_vec.normalize() #must normalize before addition!
            half_vec.add(l_vec)
            half_vec.normalize()
            #part 2: dot product and multiplication
            dot_prod = half_vec.dot(n) ** s_phong_exp
            r_specular += l_color[0] * s_specular_color[0] * dot_prod
            g_specular += l_color[1] * s_specular_color[1] * dot_prod
            b_specular += l_color[2] * s_specular_color[2] * dot_prod
    return (s_diffuse_color[0] * (r_diffuse) + r_specular + s_ambient_color[0], s_diffuse_color[1] *  (g_diffuse) + g_specular + s_ambient_color[1], s_diffuse_color[2] * (b_diffuse) + b_specular + s_ambient_color[2])

def shade(ray, depth):
    global bgcolor
    if (depth > 10):
        return bgcolor
    hit = intersect_scene(ray)
    if (hit is not None):
        pixel_color = getHitShadingColor(hit)
        s_refl_coef = hit.getSurface()[10]
        if (s_refl_coef > 0):
            pos = hit.getPosition()

            v = PVector(ray.dx, ray.dy, ray.dz)
            v.normalize()
            n = hit.getSurfaceNormal()
            n.normalize()
            dot_prod = n.dot(v)
            refl_vec = n.mult(dot_prod)
            refl_vec = n.mult(-2)
            refl_vec.add(v)
            refl_vec.normalize()
            
            offset = 1E-6
            refl_ray = Ray(refl_vec.array(), origin = [pos[0] + n.x * offset, pos[1] + n.y * offset, pos[2] + n.z * offset])
            shade_color = shade(refl_ray, depth + 1)
            return (pixel_color[0] + s_refl_coef * shade_color[0], pixel_color[1] + s_refl_coef * shade_color[1], pixel_color[2] + s_refl_coef * shade_color[2])
        return pixel_color
    else:
        return bgcolor

'''takes in a ray and indicates whether it intersects with an object.
@returns nearest hit if it does, or None if no intersection
note: returns the hit with the smallest positive t-value'''
def intersect_scene(ray):
    global object_list
    min_hit = None
    for obj in object_list:
        hit = ray.getIntersectionHit(obj)
        if hit is not None:
            if (min_hit is None) or (hit.t < min_hit.t):
                min_hit = hit
    return min_hit
def render_scene():
    global fov
    global sphere_list
    global light_list
    global bgcolor
    t0 = time.time()
    height = 600
    width = 600
    buffer = np.zeros((width, height, 3), dtype = np.uint8)

    for j in range(height):
        for i in range(width):
            # create an eye ray for pixel (i,j) and cast it into the scene
            #map screen point to viewplane
            x = i
            y = j
            k = math.tan(math.radians(fov)/2)
            x_vp = (x - width/2) * (2*k/width)
            y_vp = -1 * (y - height/2) * (2*k/height)
            z_vp = -1
            direction_vector = (x_vp - 0, y_vp - 0, z_vp - 0)
            eye_ray = Ray(direction_vector, origin=[0.0,0.0,0.0])
            pixel_color = shade(eye_ray, 0)
            buffer[j, i] = [min(255, int(255 * pixel_color[0])),
                min(255, int(255 * pixel_color[1])),
                min(255, int(255 * pixel_color[2]))]
            percentage = (float(j * width + i) / float(width * height)) * 100
            if percentage % 1 == 0:
                sys.stdout.flush()
                sys.stdout.write("\r%d%%" % (percentage))
    sys.stdout.write("\r%d ms\n" % ((time.time() - t0) * 1000))
    image = Image.fromarray(buffer) #PIL image
    image.show()

global fov
global bgcolor
global sphere_list
global cylinder_list
global object_list
global light_list
global surface

sphere_list = []
cylinder_list = []
object_list = []
light_list = []
bgcolor = (0.0, 0.0, 0.0)

while True:
    key = raw_input("Enter input:")
    keyPressed(key)