import os.path
import pygame
from random import uniform, random
from math import floor


class Paddle:

    def __init__(self, screen, paddle_img, x_loc):
        self._screen = screen
        self.width, self.height = self._screen.get_size()

        self.paddle = pygame.image.load(paddle_img).convert_alpha()
        self.paddle = pygame.transform.scale(self.paddle,
                                             (floor(self.width * .012),
                                              floor(self.height * .15)))

        self.rect = self.paddle.get_rect()

        self.x_loc = x_loc
        self.y_loc = self.height/2
        self.vel = 0

    def clamp(self, n, minn, maxn):
        return max(min(maxn, n), minn)

    def update(self):
        self.y_loc = self.clamp(self.y_loc + self.vel, self.height*.1, self.height-(self.height * .1))
        self.rect.topleft = self.x_loc, self.y_loc - (self.height * .075)

    def set_velocity(self, vel):
        self.vel = vel

