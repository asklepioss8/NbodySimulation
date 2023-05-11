import pygame as pg
import random

from settings import *
from functions import *
from objects import Sphere

class Space:

    def __init__(self, screen):

        self.screen = screen
        self.proj_points = None
        self.rotated_reg = []
        self.points = []
        self.points_rot = []
        self.cube_euler = [0, 0, 0]
        self.rotation_check = False

        self.obj_list = []
        self.obj_list_pair = None

        self.object_buffer = []
        self.rot_buffer_x = 0
        self.rot_buffer_y = 0
        self.rot_buffer_z = 0

        self.rate = 1

        # CUBE LIMIT POINTS
        scale = HALF_MARGIN
        self.points.append(np.array([CUBE_CENTER[0] - scale, CUBE_CENTER[1] - scale, CUBE_CENTER[2] - scale]))
        self.points.append(np.array([CUBE_CENTER[0] - scale, CUBE_CENTER[1] - scale, CUBE_CENTER[2] + scale]))
        self.points.append(np.array([CUBE_CENTER[0] - scale, CUBE_CENTER[1] + scale, CUBE_CENTER[2] + scale]))
        self.points.append(np.array([CUBE_CENTER[0] - scale, CUBE_CENTER[1] + scale, CUBE_CENTER[2] - scale]))
        self.points.append(np.array([CUBE_CENTER[0] + scale, CUBE_CENTER[1] - scale, CUBE_CENTER[2] - scale]))
        self.points.append(np.array([CUBE_CENTER[0] + scale, CUBE_CENTER[1] - scale, CUBE_CENTER[2] + scale]))
        self.points.append(np.array([CUBE_CENTER[0] + scale, CUBE_CENTER[1] + scale, CUBE_CENTER[2] + scale]))
        self.points.append(np.array([CUBE_CENTER[0] + scale, CUBE_CENTER[1] + scale, CUBE_CENTER[2] - scale]))
        self.points_rot = self.points

        self.initialize_obj()

    def initialize_obj(self):

        rand_arr = uniform_position_3d_v1(OBJ_COUNT, INIT_LIMITS, OBJ_RADIUS)
        random.seed = 123344

        for i in range(OBJ_COUNT):
            obj = Sphere(self.screen,
                         OBJ_RADIUS,
                         OBJ_MASS,
                         rand_arr[i],
                         (random.random(),random.random(),random.random()),
                         (0.,0.,0.))
            self.obj_list.append(obj)
        self.obj_list_pair = binary_combiner(self.obj_list)




    def update(self):
        """ In update method we are going to try to find the next closest event
         This event can be either collision to object or wall.
         So let's consider our time is a big number like 1000"""
        t = 100000
        lucky_guys = []
        lucky_pairs = []
        test_flag = "None"

        ##############
        for obj_pair in self.obj_list_pair:
            regt = collision_timing(obj_pair[0].pos, obj_pair[0].vel, obj_pair[0].radius,
                                    obj_pair[1].pos, obj_pair[1].vel, obj_pair[1].radius)
            if regt < t and regt > 0:
                t = regt
                lucky_pairs.append(obj_pair)
                test_flag = "Collision Happend"
            if t < 0:
                print("ERROR NO 1", t)


        for obj in self.obj_list:
            regt = wall_collision_time(obj, CUBIC_LIMITS)
            if 0 < regt < t:
                t = regt
                lucky_guys.append(obj)
                test_flag = "Wall collision Happend"
            if t < 0:
                print("ERROR NO 2", regt)


        for obj in self.obj_list:
            obj.pos += obj.vel * t
            print(obj.pos)

        for obj in lucky_guys:
            wall_collision(obj)

        for pair in lucky_pairs:
            collision_3d_v1(pair[0], pair[1])

        # We have 2 types of objects to be rendered
        # The first one is the points for the cube margins and the other one is central points of the objects
        # On each loop we have to refresh the data that taken from calculation (object_list the main source of data)
        # And the self.points the data source of cube corners
        # On each loop we rotate both with proper angles
        self.object_buffer = []
        self.points_rot = []
        for i in range(len(self.obj_list)):
            reg = self.obj_list[i].pos
            self.object_buffer.append(reg)
        for i in range(len(self.object_buffer)):
            self.object_buffer[i] = rotx(self.object_buffer[i], self.rot_buffer_x)
            self.object_buffer[i] = roty(self.object_buffer[i], self.rot_buffer_y)
            self.object_buffer[i] = rotz(self.object_buffer[i], self.rot_buffer_z)
        for i in range(len(self.points)):
            reg = rotx(self.points[i], self.rot_buffer_x)
            reg = roty(reg, self.rot_buffer_y)
            reg = rotz(reg, self.rot_buffer_z)
            self.points_rot.append(reg)
        ###########################



    def keypress(self, flag):
        angle = 0.01
        if flag == 1:
            self.rot_buffer_x += angle
            if self.rot_buffer_x > 360:
                self.rot_buffer_x -= 360

        if flag == 4:
            self.rot_buffer_x -= angle
            if self.rot_buffer_x < -360:
                self.rot_buffer_x += 360

        if flag == 2:
            self.rot_buffer_y += angle
            if self.rot_buffer_y > 360:
                self.rot_buffer_y -= 360

        if flag == 5:
            self.rot_buffer_y -= angle
            if self.rot_buffer_y < -360:
                self.rot_buffer_y += 360

        if flag == 3:
            self.rot_buffer_z += angle
            if self.rot_buffer_z > 360:
                self.rot_buffer_z -= 360

        if flag == 6:
            self.rot_buffer_z -= angle
            if self.rot_buffer_z < -360:
                self.rot_buffer_z += 360




    def pipeline(self, points):
        ############################
        # BOTH ROTATION, TRANSLATION, SCALING and PROJECTIONS ARE POSTCALCULATIONAL OPERATIONS!!!
        #############################
        reg = []
        output = []

        # Calculations
        # THe rotational movements can be stored for the next iterations
        # This may be helpful for if in next iteration there is any rotation this can save time
        for point in points:


            # (if) ROTATION
            # The rotational movements can be handled by either interactively or automatically

            # SCALING
            reg = point * RATIO * self.rate

            # TRANSLATION
            reg = translation3d_v1(reg, (HALF_WIDTH, HALF_HEIGHT, 0))

            # PROJECTION
            reg1 = reg.item(2) + CUBE_MARGIN * RATIO
            reg1 = reg1 * MAX_DISPLAY_RADIUS
            relative_rad = DEPTH * self.rate / reg1
            proj_point = (reg.item(0), reg.item(1), relative_rad)
            output.append(proj_point)

            # RADIUS WITH USING Z AXIS

        return output


    def draw(self):
        """AFTER MAKING ALL THE PROPER CALCULATION WE HAVE TO TRANSLATE THE CUBE TO THE CENTER OF SCREEN
        AND THEN DO THE PROJECTION"""


        # objects

        proc_point_body = self.pipeline(self.object_buffer)
        for i in range(len(self.object_buffer)):
            pos = proc_point_body[i]
            pg.draw.circle(self.screen, self.obj_list[i].get_color(), (pos[0], pos[1]), pos[2])


        # Draw As Lines
        proc_points_cube = self.pipeline(self.points_rot)
        reg2 = ((0, 1), (0, 3), (0, 4), (1, 2), (1, 5), (2, 3), (2, 6), (3, 7), (4, 5), (4, 7), (5, 6), (6, 7))
        for i in reg2:
            pg.draw.line(self.screen, "blue",
                         (proc_points_cube[i[0]][0], proc_points_cube[i[0]][1]),
                         (proc_points_cube[i[1]][0], proc_points_cube[i[1]][1]))

        self.rotation_check = False  # RESET ROTATION FLAG

