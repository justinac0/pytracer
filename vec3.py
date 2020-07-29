import math

class Vector3:
    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        return "({0},{1},{2})".format(self.x, self.y, self.z)

    def __add__(self, v2: "Vector3"):
        return Vector3(self.x + v2.x, self.y + v2.y, self.z + v2.z)

    def __sub__(self, v2: "Vector3"):
        return Vector3(self.x - v2.x, self.y - v2.y, self.z - v2.z)

    def __mul__(self, v2: "Vector3"):
        return Vector3(self.x * v2.x, self.y * v2.y, self.z * v2.z)

    def __truediv__(self, v2: "Vector3"):
        return Vector3(self.x * v2.x, self.y * v2.y, self.z * v2.z)

    def scalar_div(self, value):
        if (value != 0):
            return Vector3(self.x / value, self.y / value, self.z / value)
        else:
            return self

    def scalar_mul(self, value):
        return Vector3(self.x * value, self.y * value, self.z * value)

    def length(self):
        return math.sqrt(self.squared_length())
    
    def squared_length(self):
        return self.x * self.x + self.y * self.y + self.z * self.z

    def dot(self, v2: "Vector3"):
        return self.x * v2.x + self.y * v2.y + self.z * v2.z

    def cross(self, v2: "Vector3"):
        return Vector3( self.y * v2.z - self.z * v2.y,
                        self.z * v2.x - self.x * v2.z,
                        self.x * v2.y - self.y * v2.x )

    def normalize(self):
        return self.scalar_div(self.length())

    def reflect(self, n):
        return self - n.scalar_mul(self.dot(n) * 2.0)

