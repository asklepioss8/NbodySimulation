import numpy as np
from math import sqrt

from settings import *


class Sphere:

    def __init__(self, screen, *args):
        self.screen = screen
        self.radius = args[0]
        self.mass = args[1]
        self.pos = np.array(args[2])
        self.vel = np.array(args[3])
        self.acc = np.array(args[4])


    def energy(self):
        return sqrt(self.vel[0]**2+self.vel[0]**2+self.vel[0]**2)

    def get_color(self):
        e = int(self.energy() * 100)
        r = 0 + e
        g = 0
        b = 255 - e
        return "#{:02x}{:02x}{:02x}".format(r, g, b)

