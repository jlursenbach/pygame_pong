#!/usr/bin/env python3
# Jacob Ursenbach
# CPSC 386-01
# 2022-07-10
# jlursenbach@csu.fullerton.edu
# @jlursenbach
#
# Lab 03-00
#
# This file is a pong game
#

"""This is a Pong game for a game design class"""

from ponggame import game


def main():
    """
    starts the Pong game. returns -1 once complete
    :return: -1
    """
    the_game_obj = game.VideoGame()
    the_game_obj.build_scenegraph()
    return the_game_obj.run()


if __name__ == "__main__":
    main()
