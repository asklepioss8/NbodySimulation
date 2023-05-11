from math import sqrt

import numpy as np
from objects import Sphere
from settings import *


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


###################YANLIŞŞŞŞŞŞŞŞŞŞŞŞŞ


def collision_3d_v1(obj1, obj2):
    m1 = obj1.mass
    m2 = obj2.mass
    pos1 = obj1.pos
    pos2 = obj2.pos
    vel1 = obj1.vel
    vel2 = obj2.vel

    reg = pos2 - pos1
    reg1 = np.linalg.norm(reg)
    normal = reg / reg1
    print(normal)

    reg = m1 * m2
    reg1 = m1 + m2
    red_mass = reg / reg1

    reg = vel1 - vel2
    v_imp = np.dot(normal, reg) # impact speed

    J = (COR + 1) * red_mass * v_imp # may (1 + COR)

    reg = -J / m1
    dv1 = reg * normal
    reg = J / m2
    dv2 = reg * normal
    obj1.vel += dv1
    obj2.vel += dv2
    return obj1.vel, obj2.vel


if __name__ == "__main__":
    # t = collision_timing(np.array([0, 0, 0]),
    #                      np.array([1, 1, 1]),
    #                      1000,
    #                      np.array([1000, 1000, 1000]),
    #                      np.array([-1, -1, -1]),
    #                      0)
    # print(t)
    s1 = Sphere("self.screen",
                OBJ_RADIUS,
                OBJ_MASS,
                (0, 0, 0),
                (1., 1., 1.),
                (0, 0, 0))
    s2 = Sphere("self.screen",
                OBJ_RADIUS,
                OBJ_MASS,
                (100, 100, 100),
                (-1, -1, -1),
                (0, 0, 0))
    v = collision_3d_v1(s1, s2)
    print(v)





































