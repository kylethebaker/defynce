#!/usr/bin/python2

import pygame
import yaml

"""
    def load_tile_table(filename, width, height):
        image = pygame.image.load(filename).convert()
        image_width, image_height = image.get_size()
        tile_table = []
        for tile_x in range(0, image_width / width):
            line = []
            tile_table.append(line)
            for tile_y in range(0, image_height / height):
                rect = (tile_x * width, tile_y * height, width, height)
                line.append(image.subsurface(rect))
        return tile_table
"""

""" start Map object """


class Map(object):

    """ loads the .map data """

    def __init__(self, map_data):

        # read which sprite to use from the .map
        self.tileset = map_data['tileset']

        # creates a list with lines from the map attribute
        self.map = map_data['layout'].split("\n")
        self.map.pop()

        # for each map identifier section, create a dict of attributes
        self.key = {}

        for tile in map_data['tilemap']:
            tile_key = ''
            tile_def = {}
            for key, val in tile.items():
                if key == 'key':
                    tile_key = val
                else:
                    tile_def[key] = val
            self.key[tile_key] = tile_def

        # width/height in number of chars/lines from map attr
        self.width = len(self.map[0])
        self.height = len(self.map)

        # load the tiles from the sprite
        self.tile_table = []
        image = pygame.image.load('levels/' + self.tileset).convert()
        image_width, image_height = image.get_size()
        for tile_x in range(0, image_width / 30):
            line = []
            self.tile_table.append(line)
            for tile_y in range(0, image_height / 30):
                rect = (tile_x * 30, tile_y * 30, 30, 30)
                line.append(image.subsurface(rect))

    """ get attributes from a tile """

    def get_tile(self, x, y):
        try:
            char = self.map[y][x]
        except IndexError:
            return {}
        try:
            return self.key[char]
        except KeyError:
            return {}

    """ get bool value of attribute """
    """ TODO: need to update to new tile data layout """

    def get_bool(self, x, y, name):
        value = self.get_tile(x, y).get(name)
        return value in (True, 'true', 'yes', 'on')

    """ check if area is blocked (not placeable) """

    def is_blocked(self, x, y):
        return self.get_bool(x, y, 'blocked')

    """ render the map """

    def render(self):
        image = pygame.Surface((self.width * 30,
                                self.height * 30))
        overlays = {}
        for map_y, line in enumerate(self.map):
            for map_x, c in enumerate(line):
                try:
                    tile = self.key[c]['tile'].split(',')
                    tile = int(tile[0]), int(tile[1])
                except (ValueError, KeyError):
                    # Default to ground tile
                    tile = 0, 1
                tile_image = self.tile_table[tile[0]][tile[1]]
                image.blit(tile_image, (map_x * 30,
                                        map_y * 30))
        return image, overlays
