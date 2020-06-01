from OpenGL.GLUT import *
import DrawShapes as ds
import Camera
import numpy as np
import math
import Planet
import Scene

class SolarSystemScene(Scene.Scene):
    def __init__(self):
        super(Scene.Scene, self).__init__()
        self.camera = Camera.Camera()
        self.camera.pos = np.array([0, 10, 10])
        self.planets = []
        self.mat_spec= [1.0, 1.0, 1.0, 1.0]
        self.mat_shin = [50.0]
        self.light_pos = [0.0, 0.0, 0.0, 1.0]

        self.sun = Planet.Planet()
        self.sun.size = 2.0
        self.planets.append(self.sun)

        self.planet1 = Planet.Planet()
        self.planet1.distance = 2.0
        self.planet1.speed = 10.0
        self.planet1.size = 0.25
        self.planet1.axis = np.array([0,0,1])
        self.planet1.rotation_speed = 30.0
        self.planets.append(self.planet1)

        self.planet2 = Planet.Planet()
        self.planet2.distance = 5.0
        self.planet2.speed = 20.0
        self.planet2.orbit_angle = 180.0
        self.planet2.size = 0.5
        self.planet2.axis = np.array([0,math.sqrt(2)/2,math.sqrt(2)/2])
        self.planet2.relative_angle = 230.0
        self.planet2.rotation_speed = 10.0
        self.planets.append(self.planet2)

        self.planet3 = Planet.Planet()
        self.planet3.distance = 3.0
        self.planet3.speed = 40.0
        self.planet3.orbit_angle = 45.0
        self.planet3.size = 0.5
        self.planet3.axis = np.array([math.sqrt(2)/2,0,math.sqrt(2)/2])
        self.planet3.relative_angle = 50.0
        self.planet3.rotation_speed = 5.0
        self.planets.append(self.planet3)

    def update(self, delta_t):
        for planet in self.planets:
            planet.update(delta_t)

    def mouse_move(self, x, y):
        if(self.mouse_move_valid):
            cam = self.camera
            dx = x - self.mouse_last_x
            dy = y - self.mouse_last_y
            angle_horizontal = -dx/100
            angle_vertical = dy/100

            cam.rotate_around_origin(angle_horizontal, angle_vertical)
            self.mouse_last_x = x
            self.mouse_last_y = y

    def mouse_input(self, button, state, x, y):
        if(button == GLUT_LEFT_BUTTON):
            self.mouse_move_valid = (state == GLUT_DOWN)
            self.mouse_last_x = x
            self.mouse_last_y = y
            return

        if(button == 3):
            self.camera.change_distance(-0.1)
            return

        if(button == 4):
            self.camera.change_distance(0.1)
            return
