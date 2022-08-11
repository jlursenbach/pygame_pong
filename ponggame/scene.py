"""This is the default Scene object. Scenes are derived from teh Scene object"""

import sys
import os
import pygame


class Scene:

    """
    A default scene object that games can be built from
    includes functionality four soundtracks
    """

    main_dir = os.path.split(os.path.abspath(__file__))[0]
    data_dir = os.path.join(main_dir, 'data')
    data_dir += '/soundtracks'

    def __init__(self, screen, background_image, soundtrack=None):
        """
        initiates the class
        :param screen: a pygame screen
        :param background_image: a background image for the scene
        :param soundtrack: the soundtrack file to use
        """

        self._screen = screen
        self._background = pygame.Surface(self._screen.get_size())
        self._background_image = background_image
        self._soundtrack = soundtrack
        self._is_valid = True
        self._frame_rate = 60
        self.mouse_pos = [0, 0]

        if soundtrack:
            self._soundtrack = os.path.join(Scene.data_dir, soundtrack)
        else:
            self._soundtrack = None
        self._soundtrack_vol = .2
        self._soundtrack_on = False

    def start(self):
        """
        begins the music
        :return:
        """
        if self._soundtrack:
            try:
                pygame.mixer.music.load(self._soundtrack)
                pygame.mixer.music.set_volume(self._soundtrack_vol)
                pygame.mixer.music.play(-1, fade_ms=500)
                self._soundtrack_on = True
            except pygame.error as pygame_error:
                print(pygame_error)

    def stop(self):
        """
        stops the music
        :return:
        """
        pygame.mixer.music.fadeout(500)
        pygame.mixer.music.stop()
        self._soundtrack_on = False

    def toggle_soundtrack(self, st_bool=None):
        """
        starts and pauses the soundtrack
        takes an optional variable
        :param st_bool:
        :return:
        """
        if st_bool:
            self._soundtrack_on = st_bool
        else:
            self._soundtrack_on = not self._soundtrack_on

        if self._soundtrack_on:
            pygame.mixer.music.pause()
        else:
            pygame.mixer.music.unpause()

    def update(self):
        """
        default update function.
        to be overwritten in child classes
        :return:
        """
        return None

    def draw(self):
        """
        draws the pygame scene
        :return:
        """
        self._screen.blit(self._background_image, (0, 0))
        return None

    @property
    def is_valid(self):
        """
        returns a False bool when the scene is over
        :return:
        """
        return self._is_valid

    @property
    def frame_rate(self):
        """
        sets the game frame rate
        :return:
        """
        return self._frame_rate

    def handle_event(self, event):
        """
        reads and parses user input
        :param event:
        :return:
        """
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN and \
                event.key == pygame.K_ESCAPE:
            self._is_valid = False
