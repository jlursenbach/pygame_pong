import os.path
import pygame
from random import uniform, random


# class Ball(pygame.sprite.Sprite):
class Ball:
    main_dir = os.path.split(os.path.abspath(__file__))[0]
    ball_dir = os.path.join(main_dir, r'data/ball')
    wall_bounce_file = os.path.join(ball_dir, 'ball-tap.wav')
    paddle_bounce_file = os.path.join(ball_dir, 'paddle_tap.wav')
    ball_img = os.path.join(ball_dir, 'ball.png')

    def __init__(self, screen, position=None, velocity=None):

        self._screen = screen
        self.width, self.height = self._screen.get_size()

        self.radius = None
        self.bll = None
        self.ball = None

        self.starting_pos = [self.width * .5, self.height * .55]

        if position:
            self.ball_loc = position
        else:
            self.ball_loc = [self.width * .5, self.height * .55]

        self.x_speed = 0
        self.y_speed = 0

        self.speed_iterator = 1.05

        if velocity:
            self.velocity = velocity
        else:
            self.velocity = [0, 0]

        self.min_speed = -50
        self.max_speed = 50

        self.create_ball()

        self.bumper_bounce = None
        self.wall_bounce = None
        self._bounce_channel = pygame.mixer.Channel(2)
        self.get_sounds()
        self.sfx_on = True

    def clamp(self, n, minn, maxn):
        return max(min(maxn, n), minn)

    def create_ball(self):
        self.radius = self.height * .05
        self.bll = pygame.image.load(Ball.ball_img).convert_alpha()
        self.bll = pygame.transform.scale(self.bll, (self.radius, self.radius))
        self.ball = self.bll.get_rect()

    def start(self):
        self.x_speed = uniform(self.width * .008, self.width * .01)
        self.y_speed = uniform(self.height * .012, self.height * .018)

        x_direction = 1 if random() < 0.5 else -1
        y_direction = 1 if random() < 0.5 else -1
        self.velocity = [self.x_speed * x_direction,
                         self.y_speed * y_direction]

    def get_sounds(self):

        try:
            self.bumper_bounce = pygame.mixer.Sound(Ball.paddle_bounce_file)
        except pygame.error as pygame_error:
            print(f'Cannot open {Ball.paddle_bounce_file}.')
            raise SystemExit(1) from pygame_error

        try:
            self.wall_bounce = pygame.mixer.Sound(Ball.paddle_bounce_file)
        except pygame.error as pygame_error:
            print(f'Cannot open {Ball.paddle_bounce_file}.')
            raise SystemExit(1) from pygame_error

        self._bounce_channel = pygame.mixer.Channel(2)

    def toggle_sfx(self):
        self.sfx_on = not self.sfx_on

    def update(self):
        self.ball_loc[0] += self.velocity[0]
        self.ball_loc[1] += self.velocity[1]
        self.bounce_wall()
        # self.draw()

    # def draw(self):
    #     self.ball.center = self.ball_loc[0], self.ball_loc[1]
    #     self._screen.blit(self.bll, self.ball)

    def loc(self):
        return self.ball_loc

    def kill_ball(self):
        self.velocity = [0, 0]
        self.ball_loc = [self.width * .5, self.height * .55]

    def bounce_wall(self):

        edge_buffer = self.height * .03

        # insert code here to add bounce sound
        bounce_sound = False

        # ball hits bottom
        if self.ball_loc[1] >= self.height - edge_buffer:
            self.velocity[1] = self.clamp(self.velocity[1] * -1, self.min_speed, self.max_speed)
            bounce_sound = True

        # ball hits top
        if self.ball_loc[1] <= edge_buffer + 55:
            self.velocity[1] = self.clamp(self.velocity[1] * -1, self.min_speed, self.max_speed)
            bounce_sound = True

        if bounce_sound and self.sfx_on:
            self.wall_bounce.play()

    def bounce_left(self):
        self.x_speed = abs(self.x_speed * self.speed_iterator)
        self.velocity[0] = self.x_speed
        if self.sfx_on:
            self.bumper_bounce.play()

    def bounce_right(self):
        self.x_speed = abs(self.x_speed * self.speed_iterator)
        self.velocity[0] = -self.x_speed

        if self.sfx_on:
            self.bumper_bounce.play()

