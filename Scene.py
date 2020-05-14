from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import DrawShapes as ds
import Camera
import numpy as np
import math

class Scene():
    def __init__(self):
        super(Scene, self).__init__()


    def update(self, delta_t):
        pass

    def draw(self):
        pass

    def mouse_move(self, x, y):
        pass

    def mouse_input(self, x, y):
        pass

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


class Scene1(Scene):
    def __init__(self):
        super(Scene, self).__init__()
        self.camera = Camera.Camera()
        self.camera.pos = np.array([0, 10, 10])
        self.planets = []
        self.mat_spec= [1.0, 1.0, 1.0, 1.0]
        self.mat_shin = [50.0]
        self.light_pos = [0.0, 0.0, 0.0, 1.0]




        red = (0.8, 0.1, 0.0, 1.0)
        blue = (0.0, 0.0, 1.0, 1.0)

        self.triangle1 = glGenLists(1)
        glNewList(self.triangle1, GL_COMPILE)
        glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, red)
        ds.TriangleEquil()
        glEndList()

        self.cube1 = glGenLists(1)
        glNewList(self.cube1, GL_COMPILE)
        glPolygonMode(GL_FRONT, GL_FILL)
        ds.DrawCube()
        glEndList()

        self.sun = Planet()
        self.sun.size = 2.0
        self.planets.append(self.sun)

        self.planet1 = Planet()
        self.planet1.distance = 2.0
        self.planet1.speed = 10.0
        self.planet1.size = 0.25
        self.planet1.axis = np.array([0,0,1])
        self.planet1.rotation_speed = 30.0
        self.planets.append(self.planet1)

        self.planet2 = Planet()
        self.planet2.distance = 5.0
        self.planet2.speed = 20.0
        self.planet2.orbit_angle = 180.0
        self.planet2.size = 0.5
        self.planet2.axis = np.array([0,math.sqrt(2)/2,math.sqrt(2)/2])
        self.planet2.relative_angle = 230.0
        self.planet2.rotation_speed = 10.0
        self.planets.append(self.planet2)

        self.planet3 = Planet()
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

    def draw(self):
        glLoadIdentity()
        cam = self.camera
        gluLookAt(cam.pos[0], cam.pos[1], cam.pos[2],
                   cam.target[0], cam.target[1], cam.target[2],
                   cam.up[0], cam.up[1], cam.up[2])
        glLightfv(GL_LIGHT0, GL_POSITION, self.light_pos)
        glLightfv(GL_LIGHT0, GL_DIFFUSE, [0.5, 0.5, 0.5])
        glLightfv(GL_LIGHT0, GL_AMBIENT, [0.0, 0.0, 0.0])
        glLightfv(GL_LIGHT0, GL_SPECULAR, [0.5, 0.5, 0.5])

        for planet in self.planets:
            glPushMatrix()
            glRotatef(planet.orbit_angle, 0.0, 1.0, 0.0)
            glTranslatef(planet.distance, 0.0, 0.0)
            if(planet.axis is not None):
                x, y, z = planet.axis
                glRotatef(planet.relative_angle, x, y, z)
            glScalef(planet.size, planet.size, planet.size)

            if(planet.shape == None):
                glCallList(self.cube1)

            glPopMatrix()
        glFlush()

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
