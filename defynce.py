#!/usr/bin/python2

import pygame
import pygame.locals

from Map import *
from Scenes import *

if __name__ == "__main__":

    screen = pygame.display.set_mode((800, 600))

    """ all of this needs to be dynamic for different levels """

    map_tile_width = 30
    map_tile_height = 30
    map_cache = {
        'map-tiles.png': load_tile_table('levels/map-tiles.png',
                                         map_tile_width,
                                         map_tile_height),
    }

    level = Map()
    level.load_file('levels/1.lvl.yaml')

    clock = pygame.time.Clock()

    background, overlay_dict = level.render(map_tile_width,
                                            map_tile_height,
                                            map_cache)
    overlays = pygame.sprite.RenderUpdates()

    for (x, y), image in overlay_dict.iteritems():
        overlay = pygame.sprite.Sprite(overlays)
        overlay.image = image
        overlay.rect = image.get_rect().move(x * 10, y * 10)

    screen.fill((230, 230, 230))
    screen.blit(background, (0, 0))
    overlays.draw(screen)
    pygame.display.flip()

    """ start main loop """

    game_over = False
    while not game_over:

        # draw the map
        overlays.draw(screen)
        pygame.display.flip()

        clock.tick(75)

        """ start events """

        for event in pygame.event.get():
            if event.type == pygame.locals.QUIT:
                game_over = True
            elif event.type == pygame.locals.KEYDOWN:
                pressed_key = event.key
