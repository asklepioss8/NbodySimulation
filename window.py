import random
import sys
import pygame as pg
from numpy.random import rand

from settings import *
from space import Space



class Window:

    def __init__(self):

        # initialize pygame
        pg.init()

        self.screen = pg.display.set_mode(RES, pg.DOUBLEBUF)

        # handle time
        self.clock = pg.time.Clock()
        self.running = True

        ##############################

        ################
        # intialize the space
        self.space = Space(self.screen)
        self.fps_boost = 0





    def check_event(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
        keypress = pg.key.get_pressed()
        if keypress[pg.K_7]:
            self.space.keypress(1)
        if keypress[pg.K_4]:
            self.space.keypress(2)
        if keypress[pg.K_8]:
            self.space.keypress(3)
        if keypress[pg.K_5]:
            self.space.keypress(4)
        if keypress[pg.K_9]:
            self.space.keypress(5)
        if keypress[pg.K_6]:
            self.space.keypress(6)



    def update(self):
        self.clock.tick(FPS + self.fps_boost)


        ############################
        self.space.update()



        ############################

    def draw(self):
        self.screen.fill(NULL_SCREEN)

        ############################
        self.space.draw()

        ############################

        pg.display.update()
        pg.display.set_caption(f"FPS:{self.clock.get_fps():.1f}")

    def run(self):
        while self.running:
            self.check_event()
            self.update()
            self.draw()
        else:
            pg.quit()
            sys.exit()


if __name__ == "__main__":
    Window().run()
