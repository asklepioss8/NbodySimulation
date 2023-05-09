from itertools import  combinations
import numpy as np
from math import cos, sin, sqrt
import random
from numba import jit

from settings import *




def binary_combiner(arr):
    pairs = combinations(arr, 2)
    pairs = list(pairs)
    return pairs


def rotx(point, angle):
    rotation_x = np.array([
        [1, 0, 0],
        [0, cos(angle), -sin(angle)],
        [0, sin(angle), cos(angle)],
    ])
    rotated = np.dot(rotation_x, point.reshape((3, 1)))
    return rotated

def roty(point, angle):
    rotation_y = np.array([
        [cos(angle), 0, sin(angle)],
        [0, 1, 0],
        [-sin(angle), 0, cos(angle)],
    ])
    rotated = np.dot(rotation_y, point.reshape((3, 1)))
    return rotated

def rotz(point, angle):
    rotation_z = np.array([
        [cos(angle), -sin(angle), 0],
        [sin(angle), cos(angle), 0],
        [0, 0, 1],
    ])
    rotated = np.dot(rotation_z, point.reshape((3, 1)))
    return rotated

def translation3d_v1(arr1, arr2):
    dx = arr2[0]
    dy = arr2[1]
    dz = arr2[2]

    x = arr1[0]
    y = arr1[1]
    z = arr1[2]
    reg = np.array((x + dx, y + dy, z + dz))
    return reg


@jit(nopython=True)
def dist(p1, p2):
    return sqrt((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2 + (p2[2] - p1[2]) ** 2)

def check_coll_v1(point, point_list, radius):
    dub_rad = radius * 2
    for i in point_list:
        if dist(point, i) < dub_rad:
            return 0
        else:
            return 1


def uniform_position_3d_v1(obj_count, volume, radius):
    pos_list = []
    random.seed = 123

    minx = volume[0][0]
    miny = volume[0][1]
    minz = volume[0][2]
    maxx = volume[1][0]
    maxy = volume[1][1]
    maxz = volume[1][2]
    # normalize = sqrt((maxx-minx)**2+(maxy-miny)**2+(maxz-minz)**2)

    while obj_count > 0:
        x = random.randint(int(minx/radius), int(maxx/radius))
        y = random.randint(int(minx/radius), int(maxx/radius))
        z = random.randint(int(minx/radius), int(maxx/radius))

        if not pos_list:
            # If list is empty, just add
            pos_list.append((x*radius, y*radius, z*radius))
            obj_count -= 1
        elif check_coll_v1((x*radius, y*radius, z*radius), pos_list, radius):
            pos_list.append((x*radius, y*radius, z*radius))
            obj_count -= 1
    return pos_list



@jit(nopython=True)
def collision_timing(pos1, vec1, rad1, pos2, vec2, rad2):
    rad_sum = rad1 + rad2
    dc = pos2 - pos1
    dv = vec2 - vec1

    dcx = dc[0]
    dcy = dc[1]
    dcz = dc[2]
    dvx = dv[0]
    dvy = dv[1]
    dvz = dv[2]

    reg1 = dcx * dvx
    reg1 += dcy * dvy
    reg1 += dcz * dvz
    reg1 = -reg1
    reg2 = dvx * dvx
    reg2 += dvy * dvy
    reg2 += dvz * dvz

    # if total velocity vector is 0 they never collide

    if reg2 == 0:
        return 1000

    reg31 = rad_sum * rad_sum * reg2
    reg32 = (dcx * dvy) - (dcy * dvx)
    reg32 = reg32 * reg32
    reg33 = (dcx * dvz) - (dcz * dvx)
    reg33 = reg33 * reg33
    reg34 = (dcy * dvz) - (dcz * dvy)
    reg34 = reg34 * reg34

    delta = reg31
    delta -= reg32
    delta -= reg33
    delta -= reg34

    if delta >= 0:
        delta_root = sqrt(delta)
    elif delta < 0:
        return 1000

    reg_total = reg1 + delta_root
    time = reg_total / reg2

    return time

def wall_collision_time(obj, wall_coord):
    lwdx = obj.pos[0] - wall_coord[0][0]
    lwdy = obj.pos[1] - wall_coord[0][1]
    lwdz = obj.pos[2] - wall_coord[0][2]

    rwdx = obj.pos[0] - wall_coord[1][0]
    rwdy = obj.pos[1] - wall_coord[1][1]
    rwdz = obj.pos[2] - wall_coord[1][2]

    lwdx /= obj.vel[0] + 0.0000001
    lwdy /= obj.vel[1] + 0.0000001
    lwdz /= obj.vel[2] + 0.0000001
    rwdx /= obj.vel[0] + 0.0000001
    rwdy /= obj.vel[1] + 0.0000001
    rwdz /= obj.vel[2] + 0.0000001

    if lwdx >= 0:
        reg = lwdx
    else:
        reg = 1000
    if reg > lwdy and lwdy >= 0:
        reg = lwdy
    if reg > lwdz and lwdz >= 0:
        reg = lwdz
    if reg > rwdx and rwdx >= 0:
        reg = rwdx
    if reg > rwdy and rwdy >= 0:
        reg = rwdy
    if reg > rwdz and rwdz >= 0:
        reg = rwdz

    if reg < 0:
        print("ERROR HAPPENS")
    return reg


def collision_v1(obj1, obj2):
    reg1 = obj1.vel[0]
    reg2 = obj1.vel[1]
    reg3 = obj1.vel[2]

    obj1.vel[0] = obj2.vel[0]
    obj1.vel[1] = obj2.vel[1]
    obj1.vel[2] = obj2.vel[2]

    obj2.vel[0] = reg1
    obj2.vel[1] = reg2
    obj2.vel[2] = reg3
    print("collision")

def wall_collision(obj):
    obj.vel[0] = -obj.vel[0]
    obj.vel[1] = -obj.vel[1]
    obj.vel[2] = -obj.vel[2]






























