#!/usr/bin/python2

import pygame
import ConfigParser


""" load the tiles from the sprite """


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


""" start Level object """


class Level(object):

    """ loads the .map data """

    def load_file(self, filename):

        parser = ConfigParser.ConfigParser()
        parser.read(filename)

        # read which sprite to use from the .map
        self.tileset = parser.get("level", "tileset")

        # creates a list with lines from the map attribute
        self.map = []
        self.map = parser.get("level", "map").split("\n")

        # for each map identifier section, create a dict of attributes
        self.key = {}
        for section in parser.sections():
            if len(section) == 1:
                desc = dict(parser.items(section))
                self.key[section] = desc

        # width/height in number of chars/lines from map attr
        self.width = len(self.map[0])
        self.height = len(self.map)

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

    def get_bool(self, x, y, name):
        value = self.get_tile(x, y).get(name)
        return value in (True, 'true', 'yes', 'on')

    """ check if area is blocked (not placeable) """

    def is_blocked(self, x, y):
        return self.get_bool(x, y, 'blocked')

    """ render the map """

    def render(self, tile_width, tile_height, map_cache):
        tiles = map_cache[self.tileset]
        image = pygame.Surface((self.width * tile_width,
                                self.height * tile_height))
        overlays = {}
        for map_y, line in enumerate(self.map):
            for map_x, c in enumerate(line):
                try:
                    tile = self.key[c]['tile'].split(',')
                    tile = int(tile[0]), int(tile[1])
                except (ValueError, KeyError):
                    # Default to ground tile
                    tile = 0, 1
                tile_image = tiles[tile[0]][tile[1]]
                image.blit(tile_image, (map_x * tile_width,
                                        map_y * tile_height))
        return image, overlays
