"""
This is teh Pong title scene
"""
import pygame
from ponggame.scene import Scene


class TitleScene(Scene):
    """
    The title scene for Pong
    """

    def __init__(self, title, screen, bg_img, soundtrack):
        """
        initializes the scene.
        Sets the image and soundtrack.
        :param title:
        :param screen:
        :param bg_img:
        :param soundtrack:
        """
        super().__init__(screen, bg_img, soundtrack)
        self._title = title

    def handle_event(self, event):
        """
        sets up the user controls
        space or excape takes user to the next scene
        :param event:
        :return:
        """
        super(TitleScene, self).handle_event(event)
        if event.type == pygame.KEYUP and \
                event.key == pygame.K_SPACE:
            self._is_valid = False
        if event.type == pygame.MOUSEMOTION:
            self.mouse_pos = pygame.mouse.get_pos()
            print(self.mouse_pos)
