import pygame
import pygame.locals

from Map import *


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


""" SceneManager object """


class SceneManager(object):

    def __init__(self):
        self.go_to(TitleScene())

    def go_to(self, scene):
        self.scene = scene
        self.scene.manager = self


""" Level Scene object """


class LevelScene(Scene):

    def __init__(self, level_name):
        super(LevelScene, self).__init__()

        yaml_file = open('levels/' + level_name + '.lvl.yaml')
        level_data = yaml.safe_load(yaml_file)
        yaml_file.close()

        map_data = level_data.get('level')['map']
        self.map = Map(map_data)

    def render(self, screen):
        background, overlay_dict = self.map.render()
        overlays = pygame.sprite.RenderUpdates()

        for (x, y), image in overlay_dict.iteritems():
            overlay = pygame.sprite.Sprite(overlays)
            overlay.image = image
            overlay.rect = image.get_rect().move(x * 10, y * 10)

        screen.fill((230, 230, 230))
        screen.blit(background, (0, 0))
        overlays.draw(screen)
        pygame.display.flip()

    def update(self):
        pass

    def handle_events(self, events):
        for e in events:
            if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                pass


""" Title Screen Scene object """


class TitleScene(object):

    def __init__(self):
        super(TitleScene, self).__init__()
        self.title_font = pygame.font.SysFont('Open Sans', 60)
        self.sub_font = pygame.font.SysFont('Open Sans', 20)

    def render(self, screen):
        screen.fill((108, 192, 78))
        title_text = self.title_font.render('def[Y]nce', True,
                                            (255, 255, 255))
        sub_text = self.sub_font.render('press [space] to start', True,
                                        (255, 255, 255))
        screen.blit(title_text, (260, 200))
        screen.blit(sub_text, (290, 300))

    def update(self):
        pass

    def handle_events(self, events):
        for e in events:
            if e.type == pygame.KEYDOWN and e.key == pygame.K_SPACE:
                self.manager.go_to(LevelScene('1'))
