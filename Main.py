# Normally, import * is a bad idea, but for these modules every function is
# is prefixed with gl, glu, or glut so there is almost no chance of a namespace
# issue.
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


def get_light_enum(index):
    if(index == 0):
        return GL_LIGHT0
    if(index == 1):
        return GL_LIGHT1
    if(index == 2):
        return GL_LIGHT2
    if(index == 3):
        return GL_LIGHT3
    if(index == 4):
        return GL_LIGHT4
    if(index == 5):
        return GL_LIGHT5
    if(index == 6):
        return GL_LIGHT6
    if(index == 7):
        return GL_LIGHT7


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
        # glEnable(GL_BLEND)
        # glBlendFunc(GL_SRC_ALPHA_SATURATE, GL_ONE)
        # glEnable(GL_POLYGON_SMOOTH)
        # glHint (GL_LINE_SMOOTH_HINT, GL_DONT_CARE)
        glLineWidth (1.5)
        # glDisable(GL_CULL_FACE)
        glMatrixMode(GL_MODELVIEW)

        glEnable(GL_LIGHTING)
        glShadeModel(GL_SMOOTH)

        # Open GL only supports up to 8 lights.
        num_lights = len(self.scene.lights)

        for light_num in range(min(num_lights, 8)):
            print("Setting light " + str(light_num))
            glEnable(get_light_enum(light_num))

        if(num_lights > 8):
            print("Warning: More than 8 lights detected in scene.")

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

        self.skybox = glGenLists(1)
        glNewList(self.skybox, GL_COMPILE)
        glPolygonMode(GL_FRONT, GL_FILL)
        ds.DrawSkybox()
        glEndList()

    def main_loop(self):
        delta_t = time.time() - self.lastFrameTime
        self.lastFrameTime = time.time()
        self.runTime = self.runTime + delta_t

        self.scene.update(delta_t)

        self.draw()
        # self.draw_cube_test()

    def draw(self):
        cam = self.scene.camera

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glColor3f(1.0, 1.0, 1.0)

        glLoadIdentity()

        # Draw Skybox

        glPushMatrix()

        glScalef(8.0, 8.0, 8.0)

        cam_direction = cam.target - cam.pos

        gluLookAt(0.0, 0.0, 0.0,
                  cam_direction[0], cam_direction[1], cam_direction[2],
                  cam.up[0], cam.up[1], cam.up[2])

        glCallList(self.skybox)
        #
        glPopMatrix()

        # End Skybox

        gluLookAt(cam.pos[0], cam.pos[1], cam.pos[2],
                  cam.target[0], cam.target[1], cam.target[2],
                  cam.up[0], cam.up[1], cam.up[2])

        # glLightModelfv(GL_LIGHT_MODEL_AMBIENT, self.scene.global_ambient)

        # Set lighting
        for index, light in enumerate(self.scene.lights):
            glLightfv(get_light_enum(index), GL_POSITION, light.pos)
            glLightfv(get_light_enum(index), GL_DIFFUSE, light.diffuse)
            glLightfv(get_light_enum(index), GL_AMBIENT, light.ambient)
            glLightfv(get_light_enum(index), GL_SPECULAR, light.specular)

        # self.draw_planets()
        # glScalef(8.0, 8.0, 8.0)
        # glCallList(self.skybox)

        glFlush()
        glutSwapBuffers()

    def draw_planet_list(self, planets):
        for planet in planets:
            glPushMatrix()
            glRotatef(planet.orbit_angle, 0.0, 1.0, 0.0)
            glTranslatef(planet.distance, 0.0, 0.0)
            glTranslatef(*planet.barycenter[:3])
            glPushMatrix()
            if(planet.axis is not None):
                x, y, z = planet.axis
                glRotatef(planet.relative_angle, x, y, z)

            glScalef(planet.size, planet.size, planet.size)

            if(planet.shape is None):
                mat = planet.material
                glMaterialfv(GL_FRONT, GL_DIFFUSE, mat.diffuse)
                glMaterialfv(GL_FRONT, GL_AMBIENT, mat.ambient)
                glMaterialfv(GL_FRONT, GL_SPECULAR, mat.specular)
                glMaterialfv(GL_FRONT, GL_EMISSION, mat.emission)
                glMaterialfv(GL_FRONT, GL_SHININESS, [mat.shininess])
                # glutSolidSphere(1.0, 50, 50)
                glCallList(self.skybox)


            glPopMatrix()
            self.draw_planet_list(planet.moons)

            glPopMatrix()

    def draw_planets(self):
        self.draw_planet_list(self.scene.planets)

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
