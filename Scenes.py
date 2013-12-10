import pygame
import pygame.locals


""" base Scene object """


class Scene(object):

    def __init__(self):
        pass

    def render(self, screen):
        raise NotImplementedError

    def update(self):
        raise NotImplementedError

    def handle_events(self, events):
        raise NotImplementedError


""" Level Scene object """


class LevelScene(Scene):

    def __init__(self):
        super(LevelScene, self).__init__()
