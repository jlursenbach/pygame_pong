import os.path
import pygame
from random import uniform, random
from math import floor


class Pongmeister:

    main_dir = os.path.split(os.path.abspath(__file__))[0]
    print(main_dir)
    pm_dir = os.path.join(main_dir, r'data/pongmeister/the_pongmeister.png')
    print(pm_dir)

    def __init__(self, screen):

        self._screen = screen
        self.width, self.height = self._screen.get_size()

        self.pm = pygame.image.load(Pongmeister.pm_dir).convert_alpha()
        self.pm = pygame.transform.scale(self.pm, (floor(self.width / 10), floor(self.height / 10)))
        self.rect = self.pm.get_rect()

        self.pm_x_min = self.width / 2.1
        self.pm_x_max = self.width / 1.93
        self.pm_y_min = self.height / 1.8
        self.pm_y_max = self.height / 2.3

        self.pm_loc = [self.width * 2,
                       self.height * 2]

    def get_loc(self, the_ball):

        x_perc = the_ball.ball_loc[0] / self.width
        y_perc = the_ball.ball_loc[1] / self.height

        x_size = (self.pm_x_max - self.pm_x_min) * x_perc
        y_size = (self.pm_y_max - self.pm_y_min) * y_perc
        self.pm_loc[0] = x_size + self.pm_x_min
        self.pm_loc[1] = self.pm_y_max - y_size

    def update(self):
        self.rect.center = self.pm_loc
        pass




