import json
import pygame
from pygame.locals import *
import objects
import os


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

    all_sprites = pygame.sprite.Group()
    movable_sprites = pygame.sprite.Group()

    global platforms
    platforms = pygame.sprite.Group()
    platforms.add(objects.Platform(400, 600, 800, 100, '0x2c5160'))
    platforms.add(objects.MovingPlatform(
        825, 200, 825, 350, 100, 300, 25, '0x2c5160'))
    platforms.add(objects.MovingPlatform(
        300, 350, 500, 350, 100, 300, 25, '0x2c5160'))
    all_sprites.add(platforms)

    player = objects.Player(400, 500, 75, 75, '0xf0e4d2')
    movable_sprites.add(player)
    all_sprites.add(player)

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                quit()
            if event.type == KEYUP:
                if event.key == K_UP:
                    player.stop_jump()

                if event.key == K_ESCAPE:
                    pygame.quit()
                    quit()

        displaysurface.fill((0, 0, 0))

        player.update(platforms)

        for entity in all_sprites:
            if entity in platforms:
                entity.update(movable_sprites)
            displaysurface.blit(entity.surf, entity.rect)

        player.move(platforms)

        pygame.display.update()
        FramePerSec.tick(config['FPS'])


if __name__ == "__main__":
    main()
