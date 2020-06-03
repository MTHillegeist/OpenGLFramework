import Camera
# import Planet
import numpy as np


class Light():
    def __init__(self):
        self.pos = np.array([0.0, 0.0, 0.0])
        self.diffuse = [1.0, 1.0, 1.0]
        self.ambient = [1.0, 1.0, 1.0]
        self.specular = [1.0, 1.0, 1.0]


class Planet():
    def __init__(self):
        self.distance = 0.0
        self.orbit_angle = 0.0
        self.speed = 0.0

        self.relative_angle = 0.0
        self.axis = None
        self.rotation_speed = 0.0

        self.size = 1.0
        self.shape = None

    def update(self, delta_t):
        self.orbit_angle += delta_t * self.speed
        self.relative_angle += delta_t * self.rotation_speed


class Scene():
    def __init__(self):
        super(Scene, self).__init__()
        self.planets = []
        self.lights = []
        self.camera = Camera.Camera()

    def update(self, delta_t):
        pass

    def mouse_move(self, x, y):
        pass

    def mouse_input(self, x, y):
        pass
