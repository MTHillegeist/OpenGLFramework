from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import DrawShapes as ds
import Camera

class Scene():
    def __init__(self):
        super(Scene, self).__init__()


    def update(self):
        pass

    def draw(self):
        pass

    def mouse_move(self, x, y):
        pass

    def mouse_input(self, x, y):
        pass

class Scene1(Scene):
    def __init__(self):
        super(Scene, self).__init__()
        self.camera = Camera.Camera()

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

    def draw(self):
        glLoadIdentity()
        cam = self.camera
        gluLookAt(cam.pos[0], cam.pos[1], cam.pos[2],
                   cam.target[0], cam.target[1], cam.target[2],
                   cam.up[0], cam.up[1], cam.up[2])
        glPushMatrix()
        glCallList(self.cube1)
        glFlush()
        glPopMatrix()

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
