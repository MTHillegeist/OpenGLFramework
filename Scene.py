import Camera
# import Planet
import numpy as np


class Light():
    def __init__(self):
        self.pos = np.array([0.0, 0.0, 0.0, 1.0])
        self.diffuse = [1.0, 1.0, 1.0]
        self.ambient = [0.0, 0.0, 0.0]
        self.specular = [1.0, 1.0, 1.0]

class Material():
    def __init__(self):
        self.diffuse = [1.0, 1.0, 1.0]
        self.ambient = [1.0, 1.0, 1.0]
        self.specular = [0.3, 0.3, 0.3]
        self.emission = [0.0, 0.0, 0.0]
        self.shininess = 0.5

class Planet():
    def __init__(self):
        self.distance = 0.0
        self.orbit_angle = 0.0
        self.speed = 0.0
        self.barycenter = np.array([0.0, 0.0, 0.0, 1.0])

        self.relative_angle = 0.0
        self.axis = None
        self.rotation_speed = 0.0

        self.size = 1.0
        self.shape = None
        self.material = Material()
        # Planets are completely diffuse in space, so default them to 0.
        self.material.specular = [0.0, 0.0, 0.0]
        self.material.shininess = 0.0

        self.moons = []

    def update(self, delta_t):
        self.orbit_angle += delta_t * self.speed
        self.relative_angle += delta_t * self.rotation_speed
        for moon in self.moons:
            moon.update(delta_t)


class Scene():
    def __init__(self):
        super(Scene, self).__init__()
        self.planets = []
        self.lights = []
        self.camera = Camera.Camera()
        self.global_ambient = [0.1, 0.1, 0.1, 1.0]

    def update(self, delta_t):
        pass

    def mouse_move(self, x, y):
        pass

    def mouse_input(self, x, y):
        pass
