from ray import Ray
from vec3 import Vector3

class Material: # ewwww chuuuuuuupiiiiid
    def scatter(self, ray_in: Ray, rec):
        return (False, Ray(Vector3(0,0,0), Vector3(0,0,0)))

    def what_type(self):
        return "None"

class hit_record:
    def __init__(self, t: float, p: Vector3, normal: Vector3, material: Material):
        self.t        = t
        self.p        = p
        self.normal   = normal
        self.material = material

class Hitable:
    def hit(self, ray: Ray, t_min: float, t_max: float):
        return False

class HitableList(Hitable):
    def __init__(self, list: "Hitable list", n: "List size"):
        self.list       = list
        self.list_size  = n

    def hit(self, ray: Ray, t_min: float, t_max: float):
        temp_rec = hit_record(0, Vector3(0,0,0), Vector3(0,0,0), Material())
        hit_anything = False
        closest_so_far = t_max

        for item in self.list:
            if (item.hit(ray, t_min, closest_so_far, temp_rec)):
                hit_anything = True
                closest_so_far = temp_rec.t
                temp_rec.material = item.material

        return (hit_anything, temp_rec)
