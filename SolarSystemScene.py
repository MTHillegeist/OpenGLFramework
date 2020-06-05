import OpenGL.GLUT as GLUT
import numpy as np
import math
import Scene as sc


class SolarSystemScene(sc.Scene):
    def __init__(self):
        super(SolarSystemScene, self).__init__()
        # self.camera = Camera.Camera()
        self.camera.pos = np.array([0, 7, 7])
        self.mat_spec = [1.0, 1.0, 1.0, 1.0]
        self.mat_shin = [50.0]
        self.light_pos = [0.0, 0.0, 0.0, 1.0]
        self.global_ambient = [0.0, 0.0, 0.0, 1.0]

        self.sun = sc.Planet()
        self.sun.size = 1.5
        self.sun.material.emmissive = [1.0, 1.0, 1.0]
        self.planets.append(self.sun)

        self.planet1 = sc.Planet()
        self.planet1.distance = 2.0
        self.planet1.speed = 10.0
        self.planet1.size = 0.25
        self.planet1.axis = np.array([0, 0, 1])
        self.planet1.rotation_speed = 30.0
        self.planets.append(self.planet1)

        self.planet2 = sc.Planet()
        self.planet2.distance = 5.0
        self.planet2.speed = 20.0
        self.planet2.orbit_angle = 180.0
        self.planet2.size = 0.5
        self.planet2.axis = np.array([0, math.sqrt(2) / 2, math.sqrt(2) / 2])
        self.planet2.relative_angle = 230.0
        self.planet2.rotation_speed = 10.0
        self.planets.append(self.planet2)

        self.moon0 = sc.Planet()
        self.moon0.distance = 0.6
        self.moon0.speed = 40.0
        self.moon0.orbit_angle = 45.0
        self.moon0.size = 0.1
        self.moon0.axis = np.array([math.sqrt(2) / 2, 0, math.sqrt(2) / 2])
        self.moon0.relative_angle = 50.0
        self.moon0.rotation_speed = 5.0

        self.planet3 = sc.Planet()
        self.planet3.distance = 3.0
        self.planet3.speed = 40.0
        self.planet3.orbit_angle = 45.0
        self.planet3.size = 0.5
        self.planet3.axis = np.array([math.sqrt(2) / 2, 0, math.sqrt(2) / 2])
        self.planet3.relative_angle = 50.0
        self.planet3.rotation_speed = 5.0
        self.planet3.moons.append(self.moon0)
        self.planets.append(self.planet3)

        self.light0 = sc.Light()
        self.light0.diffuse = [1.0, 1.0, 1.0] # [0.5, 0.5, 0.5]
        self.light0.ambient = [0.0, 0.0, 0.0]
        self.light0.specular = [0.0, 0.0, 0.0]
        self.lights.append(self.light0)

        # self.light1 = sc.Light()
        # self.light1.pos = np.array([0.0, 3.0, 0.0, 1.0])
        # self.light1.diffuse = [0.5, 0.5, 0.5]
        # self.light1.ambient = [0.0, 0.0, 0.0]
        # self.light1.specular = [0.5, 0.5, 0.5]
        # self.lights.append(self.light1)

    def update(self, delta_t):
        for planet in self.planets:
            planet.update(delta_t)

    def mouse_move(self, x, y):
        if(self.mouse_move_valid):
            cam = self.camera
            dx = x - self.mouse_last_x
            dy = y - self.mouse_last_y
            angle_horizontal = -dx / 100
            angle_vertical = dy / 100

            cam.rotate_around_origin(angle_horizontal, angle_vertical)
            self.mouse_last_x = x
            self.mouse_last_y = y

    def mouse_input(self, button, state, x, y):
        if(button == GLUT.GLUT_LEFT_BUTTON):
            self.mouse_move_valid = (state == GLUT.GLUT_DOWN)
            self.mouse_last_x = x
            self.mouse_last_y = y
            return

        if(button == 3):
            self.camera.change_distance(-0.1)
            return

        if(button == 4):
            self.camera.change_distance(0.1)
            return
