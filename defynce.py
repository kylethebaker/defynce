#!/usr/bin/python2

import pygame
import pygame.locals

from Map import *
from Scenes import *

if __name__ == "__main__":

    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()

    scene = LevelScene('1')

    """ start main loop """

    game_over = False
    while not game_over:

        clock.tick(75)

        if pygame.event.get(pygame.QUIT):
            game_over = True
            pass

        scene.handle_events(pygame.event.get())
        scene.render(screen)

        pygame.display.flip()
