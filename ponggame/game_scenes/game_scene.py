"""
This is the game scene
the Pong game occurs in this scene
"""
# standard libraries
import os.path
from math import floor

# other libraries
import pygame

# user defined files
from ponggame.scene import Scene
from ponggame.game_scenes.game_objects.ball import Ball
from ponggame.game_scenes.game_objects.pongmeister import Pongmeister
from ponggame.game_scenes.game_objects.paddle import Paddle


class GameScene(Scene):
    """
    sets up the game
    directories hold images and sounds
    """

    main_dir = os.path.split(os.path.abspath(__file__))[0]
    data_dir = os.path.join(main_dir, r'data')
    plr_paddle_img = os.path.join(data_dir, r'paddle/player_paddle.png')
    ai_paddle_img = os.path.join(data_dir, r'paddle/ai_paddle.png')

    def __init__(self, screen, bg_image, soundtrack):
        """
        initialize the Pong Game
        create ball paddles scores
        :param screen:
        :param bg_image:
        :param soundtrack:
        """
        super().__init__(screen, bg_image, soundtrack)

        # variables for the screen
        self.width, self.height = self._screen.get_size()
        self._frame_rate = 120

        # sets up the ball
        self.the_ball = Ball(self._background_image)
        self.paddle_speed = self.height / 60

        # the face in the middle
        self.pongmeister = Pongmeister(self._screen)

        # the paddle objects
        plr_paddle_x = self.width * .065
        ai_paddle_x = self.width - self.width * .08

        self.plr_paddle = Paddle(self._screen, GameScene.plr_paddle_img, plr_paddle_x)
        self.ai_paddle = Paddle(self._screen, GameScene.ai_paddle_img, ai_paddle_x)

        try:
            self.win_sound = pygame.mixer.Sound(
                "ponggame/data/soundtracks/52 Horse Race Goal.mp3")
            self._bounce_channel = pygame.mixer.Channel(2)
        except pygame.error as pygame_error:
            print(f'Cannot open '
                  f'{"ponggame/data/soundtracks/52 Horse Race Goal.mp3"}.')
            raise SystemExit(1) from pygame_error

        try:
            self.fail_sound = pygame.mixer.Sound(
                "ponggame/data/soundtracks/73 Game Over.mp3")
            self._bounce_channel = pygame.mixer.Channel(2)
        except pygame.error as pygame_error:
            print(f'Cannot open '
                  f'{"ponggame/data/soundtracks/73 Game Over.mp3"}.')
            raise SystemExit(1) from pygame_error

        # sound is on
        self.sfx_on = True

        # set up score/game state
        self.pl_score = 0
        self.ai_score = 0

        self.winner = ' '
        self.game_over = False

        # control the paddles
        self.pl_paddle_vel = 0
        self.ai_paddle_vel = 0
        self.player_paddle_pos = self.height / 2
        self.ai_paddle_pos = self.height / 2

    def begin(self):
        """
        starts motion int he paddle
        also starts music if it had been paused
        or if stoped due to game win/loose
        :return:
        """
        if self._soundtrack_on:
            self.toggle_soundtrack(False)

        if self.game_over:
            self.ai_score = 0
            self.pl_score = 0
        self.game_over = False
        self.winner = ' '

        self.the_ball.start()

    def clamp(self, num, minn, maxn):
        """
        creates a value restriction
        :param num:
        :param minn:
        :param maxn:
        :return:
        """
        return max(min(maxn, num), minn)

    def bounce(self):
        """
        defines when the ball bounces
        ball has a bounce
        this defines interaction betwwen ball and paddles
        :return:
        """
        edge_buffer = 33

        # if ball hits left/right
        if self.the_ball.ball_loc[0] >= self.width - edge_buffer:
            self.scoreright()

        if self.the_ball.ball_loc[0] <= edge_buffer:
            self.scoreleft()

    def scoreleft(self):
        """
        scores on the left side (ai score)
        :return:
        """
        self.ai_score += 1
        self.the_ball.kill_ball()
        if self.ai_score >= 3:
            self.game_over = True
            self.winner = "YOU LOOSE!!!"
            self.toggle_soundtrack(True)
            if self.sfx_on:
                self.fail_sound.play()

    def scoreright(self):
        """
        scores on the right side (player score)
        :return:
        """
        self.pl_score += 1
        self.the_ball.kill_ball()
        if self.pl_score >= 3:
            self.game_over = True
            self.winner = "YOU WIN!!!"
            self.toggle_soundtrack(True)
            if self.sfx_on:
                self.win_sound.play()

    def handle_event(self, event):
        """"
        defines control scheme
        """
        super().handle_event(event)

        # used to start the ball
        if (event.type == pygame.KEYUP and (event.key == pygame.K_SPACE) or
            (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1)) and \
                self.the_ball.velocity == [0, 0]:
            self.begin()

        # move paddle up
        if event.type == pygame.KEYDOWN and event.key == pygame.K_w:
            self.plr_paddle.set_velocity(-self.paddle_speed)
        # move paddle down
        if event.type == pygame.KEYDOWN and event.key == pygame.K_s:
            self.plr_paddle.set_velocity(self.paddle_speed)
        # stop paddle movement
        if event.type == pygame.KEYUP and event.key == pygame.K_w:
            self.plr_paddle.set_velocity(0)
        # stop paddle movement
        if event.type == pygame.KEYUP and event.key == pygame.K_s:
            self.plr_paddle.set_velocity(0)

    def update(self):
        """
        updates the game screen
        paddles, ball, score and pongmeister
        :return:
        """
        self.ai_update()
        self.ai_paddle.update()
        self.plr_paddle.update()

        if self.the_ball.ball.colliderect(self.ai_paddle.rect):
            self.the_ball.bounce_right()

        if self.the_ball.ball.colliderect(self.plr_paddle.rect):
            self.the_ball.bounce_left()

        self.pongmeister.get_loc(self.the_ball)
        self.pongmeister.update()

        self.draw()

        self.the_ball.update()
        self.bounce()

    def ai_update(self):
        """
        defines the AI's actions
        :return:
        """

        # AI paddle only moves when ball is on AI side
        if self.the_ball.ball_loc[0] < self.width / 2:
            self.ai_paddle.set_velocity(0)
        else:
            self.ai_paddle.set_velocity((self.the_ball.ball_loc[
                                             1] - self.ai_paddle.y_loc) * .27)
        # limits AI paddle velocity
        # makes game winnable
        self.ai_paddle.set_velocity(
            self.clamp(self.ai_paddle.vel,
                       -self.height / 60,
                       self.height / 60))

        self.ai_paddle_pos = (self.clamp(self.ai_paddle_pos + self.ai_paddle_vel, 7, self.height))

    def draw(self):
        """
        draws all objects
        :return:
        """
        super().draw()

        self._screen.blit(self.pongmeister.pm, self.pongmeister.rect)

        self.the_ball.ball.center = self.the_ball.ball_loc[0], \
                                    self.the_ball.ball_loc[1]
        self._screen.blit(self.the_ball.bll, self.the_ball.ball)

        self.player_paddle_pos = (self.clamp(
            self.player_paddle_pos + self.pl_paddle_vel,
            7,
            self.height - self.height * .18))

        self._screen.blit(self.plr_paddle.paddle, self.plr_paddle.rect)
        self._screen.blit(self.ai_paddle.paddle, self.ai_paddle.rect)

        # defines score font
        score_font_size = floor(self.height * .05)
        _score_font = pygame.font.Font(pygame.font.get_default_font(),
                                       score_font_size)

        # player scoreboard
        player_score = _score_font.render(str(self.pl_score), True, (0, 0, 0))
        pl_score_pos = player_score.get_rect(center=(self.width * (73 / 192),
                                                     self.height * (12 / 192),))
        self._screen.blit(player_score, pl_score_pos)

        # ai scoreboard
        ai_score = _score_font.render(str(self.ai_score), True, (0, 0, 0))
        ai_score_pos = ai_score.get_rect(center=(self.width * (118 / 191),
                                                 self.height * (12 / 192)))
        self._screen.blit(ai_score, ai_score_pos)

        # font shows a win state
        winner_font_size = floor(self.height * .2)
        _winner_font = pygame.font.Font(
            pygame.font.get_default_font(), winner_font_size)
        winner = _winner_font.render(f"{self.winner}", True, (200, 0, 0))
        winner_pos = winner.get_rect(center=(self.width / 2,
                                             self.height / 2))
        self._screen.blit(winner, winner_pos)
