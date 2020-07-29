from ray import Ray
from vec3 import Vector3
import math
import random

def random_in_unit_disk():
    p = Vector3(0,0,0)

    while (p.dot(p) >= 1.0):
        p = Vector3(random.uniform(0,1), random.uniform(0,1), 0).scalar_mul(2.0) - Vector3(1,1,0)

    return p

class Camera:
    def __init__(self, lookfrom: Vector3, lookat: Vector3, vup: Vector3, fov, aspect, aperture, focus_dist):
        theta = fov * (3.145 / 180.0)
        half_height = math.tan(theta/2.0)
        half_width = aspect * half_height
        self.origin = lookfrom
        self.w = (lookfrom - lookat).normalize()
        self.u = vup.cross(self.w).normalize()
        self.v = self.w.cross(self.u)
        self.lower_left_corner = self.origin - self.u.scalar_mul(half_width) - self.v.scalar_mul(half_height * focus_dist) - self.w.scalar_mul(focus_dist)
        self.horizontal  = self.u.scalar_mul(2 * half_width * focus_dist)
        self.vertical    = self.v.scalar_mul(2 * half_height * focus_dist)
        self.lens_radius = 0.0

    def get_ray(self, s, t):
        rd = random_in_unit_disk().scalar_mul(self.lens_radius)
        offset = self.u.scalar_mul(rd.x) + self.v.scalar_mul(rd.y)
        return Ray(self.origin + offset, self.lower_left_corner + self.horizontal.scalar_mul(s) + self.vertical.scalar_mul(t) - self.origin - offset)
