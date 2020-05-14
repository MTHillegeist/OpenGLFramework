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
import Scene

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
        self.scene = Scene.Scene1()

        #Culling type. GL_BACK is the default.
        #glCullFace(GL_BACK)
        #glCullFace(GL_FRONT_AND_BACK)
        glEnable(GL_CULL_FACE)
        glEnable(GL_DEPTH_TEST)
        # glDisable(GL_CULL_FACE)
        glMatrixMode(GL_MODELVIEW)

        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)

        self.lastFrameTime = time.time()

    def main_loop(self):
        delta_t = time.time() - self.lastFrameTime
        self.lastFrameTime = time.time()
        self.runTime = self.runTime + delta_t

        self.scene.update(delta_t)

        self.draw()
        #self.draw_cube_test()

    def draw(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glColor3f(1.0, 1.0, 1.0)
        self.scene.draw()
        glutSwapBuffers()

    def reshape(self, w, h):
        ratio = w / h
        glViewport(0, 0, w, h)

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(60.0, ratio, 1.5, 20.0)
        glMatrixMode(GL_MODELVIEW)

    def keyboard_input(self, key, x, y):
        pass

    def mouse_move(self, x, y):
        self.scene.mouse_move(x, y)

    def mouse_input(self, button, state, x, y):
        self.scene.mouse_input(button, state, x, y)

glutInit()
glutInitDisplayMode(GLUT_DEPTH | GLUT_RGBA)
glutInitWindowSize(800, 800)
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
