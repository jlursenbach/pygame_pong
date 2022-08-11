"""
Credits scene
displays the credits page
"""
import pygame
from ponggame.scene import Scene


class CreditScene(Scene):
    """
    uses mostly default scene object
    will display credits scene image
    """

    def __init__(self, title, screen, bg_img, soundtrack):
        """
        initilializes object.
        sets the background image
        :param title:
        :param screen:
        :param bg_img:
        :param soundtrack:
        """
        super().__init__(screen, bg_img, soundtrack)
        self._title = title

    def handle_event(self, event):
        """
        quits the scene
        :param event:
        :return:
        """
        super(CreditScene, self).handle_event(event)
        if event.type == pygame.KEYUP and \
                event.key == pygame.K_SPACE:
            self._is_valid = False
