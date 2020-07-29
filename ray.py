from vec3 import Vector3

class Ray:
    def __init__(self, a: Vector3, b: Vector3):
        self.A = a
        self.B = b

    def origin(self):
        return self.A
    
    def direction(self):
        return self.B

    def point_at_parameter(self, t):
        return self.A + self.B.scalar_mul(t)
