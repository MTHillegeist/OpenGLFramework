#from OpenGL import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import sys, time
import math
from math import sin,cos,sqrt,pi
import DrawShapes as ds
import numpy as np
import Camera

print(sys.version)
print("Testing of Main.py")

class Application(object):

    def __init__(self):
        super(Application, self).__init__()
        self.lastFrameTime = time.time()
        self.runTime = 0
        self.angle = 0
        self.camera = Camera.Camera()
        self.mouse_move_valid = False
        self.mouse_last_x = None
        self.mouse_last_y = None

        #Culling type. GL_BACK is the default.
        #glCullFace(GL_BACK)
        #glCullFace(GL_FRONT_AND_BACK)
        glEnable(GL_CULL_FACE)
        glEnable(GL_DEPTH_TEST)
        # glDisable(GL_CULL_FACE)
        glMatrixMode(GL_MODELVIEW)

        red = (0.8, 0.1, 0.0, 1.0)
        blue = (0.0, 0.0, 1.0, 1.0)

        self.triangle1 = glGenLists(1)
        glNewList(self.triangle1, GL_COMPILE)
        glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, red)
        ds.TriangleEquil()
        glEndList()

        self.cube1 = glGenLists(1)
        glNewList(self.cube1, GL_COMPILE)
        glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, red)
        glColor3f(red[0], red[1], red[2])
        glPolygonMode(GL_FRONT, GL_FILL)
        ds.DrawCube()
        glEndList()

        self.lastFrameTime = time.time()

    def main_loop(self):
        delta_t = time.time() - self.lastFrameTime
        self.lastFrameTime = time.time()
        self.runTime = self.runTime + delta_t

        #self.angle += 20.0 * delta_t % 360

        self.draw()
        #self.draw_cube_test()

    def draw(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glColor3f(1.0, 1.0, 1.0)

        glLoadIdentity()
        cam = self.camera
        gluLookAt(cam.pos[0], cam.pos[1], cam.pos[2],
                   cam.target[0], cam.target[1], cam.target[2],
                   cam.up[0], cam.up[1], cam.up[2])
        glPushMatrix()
        glRotatef(self.angle, 1.0, 1.0, 0.0)
        glCallList(self.cube1)
        glFlush()
        glPopMatrix()

        glutSwapBuffers()

    def reshape(self, w, h):
        glViewport(0, 0, w, h)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glFrustum(-1.0, 1.0, -1.0, 1.0, 1.5, 20.0)
        glMatrixMode(GL_MODELVIEW)

    def keyboard_input(self, key, x, y):
        pass

    def mouse_move(self, x, y):
        if(self.mouse_move_valid):
            cam = self.camera
            dx = x - self.mouse_last_x
            dy = y - self.mouse_last_y
            angle_horizontal = -dx/100
            angle_vertical = dy/100

            cam.rotate_around_origin(angle_horizontal, angle_vertical)
            #self.angle += dx / 2.0
            self.mouse_last_x = x
            self.mouse_last_y = y

    def mouse_input(self, button, state, x, y):
        if(button == 0):
            self.mouse_move_valid = (state == GLUT_DOWN)
            self.mouse_last_x = x
            self.mouse_last_y = y

        if(button == 3):
            print(self.camera.pos)
            self.camera.pos[1] += 0.1
            self.camera.pos[2] += 0.1
        if(button == 4):
            self.camera.pos[1] -= 0.1
            self.camera.pos[2] -= 0.1
            print(self.camera.pos)


glutInit()
glutInitDisplayMode(GLUT_DEPTH | GLUT_RGBA)
glutInitWindowSize(500, 500)
glutInitWindowPosition(0, 0)
glutCreateWindow(b"OpenGL Testing")
app = Application()
glutDisplayFunc(app.main_loop)
glutReshapeFunc(app.reshape)
glutKeyboardFunc(app.keyboard_input)
glutMotionFunc(app.mouse_move)
glutMouseFunc(app.mouse_input)
glutIdleFunc(app.main_loop)
glutMainLoop()
