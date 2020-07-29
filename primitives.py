import math
import random

from ray import Ray
from hitable import hit_record, Hitable, Material
from vec3 import Vector3

def refract(v: Vector3, n: Vector3, ni_over_nt: float):
    uv = v.normalize()
    dt = uv.dot(n)
    discriminant = 1.0 - ni_over_nt * ni_over_nt * (1 - dt * dt)
    if (discriminant > 0):
        refracted = (uv - n.scalar_mul(dt)).scalar_mul(ni_over_nt) - n.scalar_mul(math.sqrt(discriminant))
        return (True, refracted)

    return (False, Vector3(0,0,0))

class Lambertian(Material):
    def __init__(self, albedo: Vector3):
        self.albedo = albedo

    def what_type(self):
        return "Lambertian"

    def scatter(self, ray: Ray, rec: hit_record):
        target = rec.p + rec.normal + random_in_unit_sphere()
        scattered = Ray(rec.p, target - rec.p)
        attenuation = self.albedo
        return (True, scattered, attenuation) # has a scatter occurered?, return the scatter data

class Metal(Material):
    def __init__(self, albedo: Vector3):
        self.albedo = albedo

    def what_type(self):
        return "Metal"

    def scatter(self, ray_in: Ray, hit_record: hit_record):
        reflected = ray_in.direction().normalize().reflect(hit_record.normal)
        scattered = Ray(hit_record.p, reflected)
        attenuation = self.albedo
        should_scatter = scattered.direction().dot(hit_record.normal) > 0
        return (should_scatter, scattered, attenuation)

def schlick(cosine, ref_idx):
    r0 = (1 - ref_idx) / (1 + ref_idx)
    r0 *= r0
    return r0 + (1 - r0) * math.pow((1 - cosine), 5)

class Dielectric(Material):
    def __init__(self, ref_idx):
        self.ref_idx = ref_idx

    def what_type(self):
        return "Metal"

    def scatter(self, ray_in: Ray, hit_record: hit_record):
        outward_normal = Vector3(1, 1, 1)
        reflected      = ray_in.direction().reflect(hit_record.normal)
        ni_over_nt     = 0
        attenuation    = Vector3(1, 1, 1)
        scattered      = Vector3(0, 0, 0)
        reflect_prob   = 0
        cosine         = 0

        if (ray_in.direction().dot(hit_record.normal) > 0):
            outward_normal = Vector3(0,0,0) - hit_record.normal
            ni_over_nt     = self.ref_idx
            cosine         = self.ref_idx * ray_in.direction().dot(hit_record.normal) / ray_in.direction().length()
        else:
            outward_normal = hit_record.normal
            ni_over_nt     = 1 / self.ref_idx
            cosine         = -ray_in.direction().dot(hit_record.normal) / ray_in.direction().length()

        is_scattered, refracted = refract(ray_in.direction(), outward_normal, ni_over_nt)
        if (is_scattered):
            reflect_prob = schlick(cosine, self.ref_idx)
        else:
            scattered = Ray(hit_record.p, reflected)
            reflect_prob = 1.0
        
        if (random.uniform(0,1) < reflect_prob):
            scattered = Ray(hit_record.p, reflected)
        else:
            scattered = Ray(hit_record.p, refracted)

        return (True, scattered, attenuation)

def random_in_unit_sphere():
    p = Vector3(random.uniform(0,1), random.uniform(0,1), random.uniform(0,1)).scalar_mul(2.0) - Vector3(1,1,1)

    while (p.squared_length() >= 1.0):
        p = Vector3(random.uniform(0,1), random.uniform(0,1), random.uniform(0,1)).scalar_mul(2.0) - Vector3(1,1,1)

    return p

class Sphere(Hitable):
    def __init__(self, center: Vector3, radius: float, mat: Material):
        self.center = center
        self.radius = radius
        self.material = mat

    def hit(self, ray: Ray, t_min: float, t_max: float, rec: hit_record):
        oc = ray.origin() - self.center
        a = Vector3.dot(ray.direction(), ray.direction())
        b = Vector3.dot(oc, ray.direction())
        c = Vector3.dot(oc, oc) - self.radius * self.radius
        discriminant = b * b - a * c

        if (discriminant > 0):
            temp = (-b - math.sqrt(discriminant)) / a
            if (temp < t_max and temp > t_min):
                rec.t = temp
                rec.p = ray.point_at_parameter(rec.t)
                rec.normal = (rec.p - self.center).scalar_div(self.radius)
                return True
            temp = (-b + math.sqrt(discriminant)) / a
            if (temp < t_max and temp > t_min):
                rec.t = temp
                rec.p = ray.point_at_parameter(rec.t)
                rec.normal = (rec.p - self.center).scalar_div(self.radius)
                return True

        return False
