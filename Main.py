# from OpenGL import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import sys
import time
import DrawShapes as ds
import Camera
import SolarSystemScene

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
        self.scene = SolarSystemScene.SolarSystemScene()

        # Culling type. GL_BACK is the default.
        # glCullFace(GL_BACK)
        # glCullFace(GL_FRONT_AND_BACK)
        glEnable(GL_CULL_FACE)
        glEnable(GL_DEPTH_TEST)
        # glDisable(GL_CULL_FACE)
        glMatrixMode(GL_MODELVIEW)

        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)

        self.lastFrameTime = time.time()

        # Drawing initializations.
        red = (0.8, 0.1, 0.0, 1.0)

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

    def main_loop(self):
        delta_t = time.time() - self.lastFrameTime
        self.lastFrameTime = time.time()
        self.runTime = self.runTime + delta_t

        self.scene.update(delta_t)

        self.draw()
        # self.draw_cube_test()

    def draw(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glColor3f(1.0, 1.0, 1.0)

        # self.scene.draw()
        glLoadIdentity()
        cam = self.scene.camera
        gluLookAt(cam.pos[0], cam.pos[1], cam.pos[2],
                  cam.target[0], cam.target[1], cam.target[2],
                  cam.up[0], cam.up[1], cam.up[2])

        glLightfv(GL_LIGHT0, GL_POSITION, self.scene.light_pos)
        glLightfv(GL_LIGHT0, GL_DIFFUSE, [0.5, 0.5, 0.5])
        glLightfv(GL_LIGHT0, GL_AMBIENT, [0.0, 0.0, 0.0])
        glLightfv(GL_LIGHT0, GL_SPECULAR, [0.5, 0.5, 0.5])

        self.draw_planets()

        glFlush()
        glutSwapBuffers()

    def draw_planets(self):
        for planet in self.scene.planets:
            glPushMatrix()
            glRotatef(planet.orbit_angle, 0.0, 1.0, 0.0)
            glTranslatef(planet.distance, 0.0, 0.0)
            if(planet.axis is not None):
                x, y, z = planet.axis
                glRotatef(planet.relative_angle, x, y, z)
            glScalef(planet.size, planet.size, planet.size)

            if(planet.shape is None):
                glCallList(self.cube1)

            glPopMatrix()

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
