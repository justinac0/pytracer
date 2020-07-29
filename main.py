import sys
import math
import random
import time

from hitable import hit_record, Hitable, HitableList
from primitives import *
from camera import Camera

def color(ray: Ray, world: "HitableList", depth):
    isHit, rec = world.hit(ray, 0.01, sys.float_info.max)
    if (isHit):
        attenuation = Vector3(0.0, 0.0, 0.0)
        should_scatter, scattered, attenuation = rec.material.scatter(ray, rec)
        if (depth < 50 and should_scatter):
            if (scattered.direction().x == 0 and scattered.direction().y == 0 and scattered.direction().z == 0):
                print(rec.material.what_type())
            return attenuation * color(scattered, world, depth + 1)
        else:
            return Vector3(0, 0, 0)
    else:
        unit_direction = ray.direction().normalize()
        t = 0.5 * (unit_direction.y + 1.0)
        return Vector3(1.0, 1.0, 1.0).scalar_mul((1.0 - t)) + Vector3(0.5, 0.7, 1.0).scalar_mul(t)

def file_pixel_write(file, vector):
    file.write(str(int(vector.x)) + " ")
    file.write(str(int(vector.y)) + " ")
    file.write(str(int(vector.z)) + "\n")

def file_ppm_write(file_name, width, height, samples):
    file = open(file_name, "wt")

    file_header = "P3\n" + str(width) + " " + str(height) + "\n255\n"
    file.write(file_header)

    # SCENE
    scene = []
    scene.append(Sphere(Vector3(0, -1000.5, 0), 1000, Lambertian(Vector3(0.5, 0.5, 0.5))))

    for a in range(-4, 4):
        for b in range(-4, 4):
            choose_mat = random.uniform(0, 1)
            center = Vector3(a + 0.9 * random.uniform(0,1), -0.3, b + 0.9 * random.uniform(0,1))
            if ((center - Vector3(4, 0.0, 0)).length() > 0.9):
                if (choose_mat < 0.8):
                    scene.append(Sphere(center, 0.2, Lambertian(Vector3(random.uniform(0,1) * random.uniform(0,1), random.uniform(0,1) * random.uniform(0,1), random.uniform(0,1) * random.uniform(0,1)))))
                elif (choose_mat < 0.95):
                    scene.append(Sphere(center, 0.2, Metal(Vector3(0.5 * (1 + random.uniform(0, 1)), 0.5 * (1 + random.uniform(0, 1)), 0.5 * random.uniform(0,1)))))
                else:
                    scene.append(Sphere(center, 0.2, Dielectric(1.5)))

    scene.append(Sphere(Vector3(0, 0.5, 0), 1.0, Dielectric(1.5)))
    scene.append(Sphere(Vector3(0, 0.5, 0), 0.9, Dielectric(1.5)))

    world = HitableList(scene, len(scene))

    lookform      = Vector3(5, 3, 15)
    lookat        = Vector3(-5, 0, -1)
    dist_to_focus = (lookform - lookat).length()
    aperture      = 2.0
    camera        = Camera(lookform, lookat, Vector3(0, 1, 0), 20, 16/9, aperture, dist_to_focus)

    print("Calculating Render...")

    for y in range(height-1, -1, -1):
        if (y%2 == 0):
            print(str(round(100-(y/height * 100), 2)) + "% done")
        for x in range(0, width):
            col = Vector3(0.0, 0.0, 0.0)
            u,v = 0,0
            if (samples == 0):
                u = float(x) / width
                v = float(y) / height

                ray = camera.get_ray(u, v)
                
                col += color(ray, world, 0)
            else:
                for s in range(samples):
                    u = float(x + random.uniform(0.0, 1.0)) / width
                    v = float(y + random.uniform(0.0, 1.0)) / height

                    ray = camera.get_ray(u, v)

                    col += color(ray, world, 0)

                col = col.scalar_div(samples)

            col = Vector3(math.sqrt(col.x), math.sqrt(col.y), math.sqrt(col.z))
            rgb = Vector3(col.x * 255.99, col.y * 255.99, col.z * 255.99)

            file_pixel_write(file, rgb)

    file.close()

def main():
    width = 2000 # nice 4k render bro
    height = int(width/2)
    samples = 0

    start = time.perf_counter()
    file_ppm_write("output.ppm", width, height, samples)
    end = time.perf_counter()

    time_elapsed = end-start

    if (samples < 1):
        samples = 1

    print("\nRender Complete in", round(time_elapsed, 3), "seconds.")
    print("Dimensions:", str(width) + "x" + str(height), "(" + str(width * height), "pixels)")
    print("Sampling Quality:", str(samples), "samples/pixel")
    print("Sampling Rate:", round( width * height * samples / time_elapsed, 2), "samples/second.")

if __name__ == "__main__":
    main()
