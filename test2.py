import numpy as np
from math import sqrt

def collision_timing_v2(pos1, vel1, rad1, pos2, vel2, rad2):
    rel_pos = pos2 - pos1
    rel_vel = vel2 - vel1
    rad_sum = rad1 + rad2

    a = np.dot(rel_vel, rel_vel)
    b = 2 * (rel_pos[0]*rel_vel[0] + rel_pos[1]*rel_vel[1] + rel_pos[2]*rel_vel[2])
    c = np.dot(rel_pos, rel_pos) - rad_sum**2

    print(a)
    print(b)
    print(c)

if __name__ == "__main__":
    collision_timing_v2(np.array((0, 0, 0), "f8"),
                        np.array((0, 0, 0), "f8"),
                        10,
                        np.array((100, 100, 100), "f8"),
                        np.array((-1, -1, -1), "f8"),
                        10)
