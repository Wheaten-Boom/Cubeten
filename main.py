import json
import pygame
from pygame.locals import *
import objects
import os
import Level_Loader


class configuration():
    def __init__(self):
        with open(os.path.join(os.path.dirname(__file__), 'settings.json')) as config_file:
            self.config = json.load(config_file)

    def get(self, key):
        return self.config[key]


def main():
    config = configuration().config

    pygame.init()
    FramePerSec = pygame.time.Clock()

    displaysurface = pygame.display.set_mode(
        (config['WIDTH'], config['HEIGHT']))
    pygame.display.set_caption(config['TITLE'])

    level = Level_Loader.Load("LEVEL_1")

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                quit()
            if event.type == KEYUP:
                if event.key == K_UP:
                    level[0].player.stop_jump()

                if event.key == K_ESCAPE:
                    pygame.quit()
                    quit()

        displaysurface.fill((0, 0, 0))

        level[0].player.update(level[0].platforms)

        for entity in level[0].all_sprites:
            displaysurface.blit(entity.surf, entity.rect)

            for platform in level[0].moving_platforms:
                platform.update(level[0].movable_sprites)

        level[0].player.move(level[0].platforms)

        pygame.display.update()
        FramePerSec.tick(config['FPS'])


if __name__ == "__main__":
    main()
