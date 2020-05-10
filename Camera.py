import math
from math import sin,cos,sqrt,pi
import numpy as np

class Camera:
    def __init__(self):
        super(Camera, self).__init__()
        self.target = [0, 0, 0]
        self.pos = [0, 2, 2]
        self.up = [0, 1, 0]

    def rotate_around_origin(self, horizontal_angle, vertical_angle):
        pos_vec = np.array(self.pos)
        up_vec = np.array(self.up)
        cross_vec = np.cross( pos_vec, up_vec)
        #Normalize the vector.
        cross_vec = cross_vec / math.sqrt(np.dot(cross_vec, cross_vec))

        rot_matrix_x = np.array([[cos(horizontal_angle), 0, sin(horizontal_angle)],
                                [0, 1, 0],
                                [-sin(horizontal_angle), 0, cos(horizontal_angle)]])

        rot_matrix_cross = Camera.rotation_matrix(cross_vec, vertical_angle)

        rot_res = rot_matrix_cross @ rot_matrix_x @ pos_vec
        self.pos[0] = rot_res[0]
        self.pos[1] = rot_res[1]
        self.pos[2] = rot_res[2]

    def change_distance(self, delta_distance):
        pos_vec = np.array(self.pos)
        curr_distance = sqrt(np.dot(pos_vec, pos_vec))
        norm_pos = pos_vec / curr_distance
        new_dist = curr_distance + delta_distance

        if(new_dist < 0.1):
            new_dist = 0.1

        new_pos = norm_pos * new_dist

        self.pos[0] = new_pos[0]
        self.pos[1] = new_pos[1]
        self.pos[2] = new_pos[2]

    #Pulled from stackoverflow.
    def rotation_matrix(axis, theta):
        """
        Return the rotation matrix associated with counterclockwise rotation about
        the given axis by theta radians.
        """
        axis = np.asarray(axis)
        axis = axis / sqrt(np.dot(axis, axis))
        a = cos(theta / 2.0)
        b, c, d = -axis * sin(theta / 2.0)
        aa, bb, cc, dd = a * a, b * b, c * c, d * d
        bc, ad, ac, ab, bd, cd = b * c, a * d, a * c, a * b, b * d, c * d
        return np.array([[aa + bb - cc - dd, 2 * (bc + ad), 2 * (bd - ac)],
                         [2 * (bc - ad), aa + cc - bb - dd, 2 * (cd + ab)],
                         [2 * (bd + ac), 2 * (cd - ab), aa + dd - bb - cc]])
