"""
This is the game file! initiates the game
runs the scenes
"""

import pygame

from ponggame.game_scenes.game_scene import GameScene
from ponggame.game_scenes.title_scene import TitleScene
from ponggame.game_scenes.credits_scene import CreditScene


class VideoGame:
    """
    This class controls the flow of the pong game
    """
    def __init__(self,
                 window_width=2000,
                 window_height=1150,
                 window_title='ADVERSARIAL PONG'):
        """
        initializes the video game
        """

        pygame.init()
        # control window size:
        self._window_size = (window_width, window_height)
        percent_window = .5

        perc_size = (window_width * percent_window, window_height * percent_window)
        self._window_size = perc_size

        # set background
        self.game_screen = pygame.image.load('ponggame/data/backgrounds/Pong Background.png')
        self.game_screen = pygame.transform.scale(self.game_screen, self._window_size)

        # set background
        self.title_screen = pygame.image.load('ponggame/data/backgrounds/Pong_Title_Screen.png')
        self.title_screen = pygame.transform.scale(self.title_screen, self._window_size)

        self.credits_screen = pygame.image.load('ponggame/data/backgrounds/pong_credits.png')
        self.credits_screen = pygame.transform.scale(self.credits_screen, self._window_size)

        self._scene_graph = None

        # set frame_rate
        self._clock = pygame.time.Clock()
        self._screen = pygame.display.set_mode(self._window_size)

        # define window info
        self._title = window_title
        pygame.display.set_caption(self._title)

        # prime game over while loop
        self._game_is_over = False

        # set up fonts and sounds
        if not pygame.font:
            print('Warning: fonts are disabled.')
        if not pygame.mixer:
            print('Warning: sound is disabled.')

    def build_scenegraph(self):
        """
        sets up the flow of scenes in the game
        :return:
        """
        self._scene_graph = [
            TitleScene("POWER PONG", self._screen, self.title_screen, soundtrack="LOZ57.mp3"),
            GameScene(self._screen, self.game_screen, soundtrack="68 Gerudo Valley.mp3"),
            CreditScene("CREDITS", self._screen, self.credits_screen, soundtrack="LOZ57.mp3")
        ]

    def run(self):
        """
        this is the run loop
        decides when a scene is active
        :return:
        """
        # while not self._game_is_over:
        for scene in self._scene_graph:
            # start the game
            scene.start()
            # while the game is running
            while scene.is_valid:
                # running the clock
                self._clock.tick(scene.frame_rate)
                for event in pygame.event.get():
                    scene.handle_event(event)
                scene.update()
                scene.draw()
                pygame.display.update()
            # stop the game
            scene.stop()
        # close the program
        pygame.quit()
        return 0
