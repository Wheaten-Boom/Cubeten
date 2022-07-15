import json
import pygame
from pygame.locals import *
import os
import Level_Loader


def load_configuration():
    with open(os.path.join(os.path.dirname(__file__), 'settings.json')) as config_file:
        config = json.load(config_file)
    return config


def main():
    config = load_configuration()

    pygame.init()
    FramePerSec = pygame.time.Clock()

    displaysurface = pygame.display.set_mode(
        (config['WIDTH'], config['HEIGHT']))
    pygame.display.set_caption(config['TITLE'])

    level = Level_Loader.Load("LEVEL_1")

    while True:
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_UP]:
            level[0].player.jump(level[0].all_sprites)

        if pressed_keys[K_ESCAPE]:
            pygame.quit()
            quit()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                quit()

            if event.type == KEYUP:
                if event.key == K_UP:
                    level[0].player.stop_jump()
            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    success = level[0].player.hold_object(
                        level[0].all_sprites, level[0].movable_sprites)
                    if success == True:
                        if level[0].player.is_holding:
                            groups = level[0].player.held_object.groups()
                            level[0].player.held_object.kill()
                            level[0].player.held_object.add(
                                level[0].all_sprites)
                        else:
                            level[0].player.held_object.add(groups)
                            level[0].player.held_object = None

        displaysurface.fill((0, 0, 0))

        level[0].player.move()
        for entity in level[0].cubes:
            entity.move(level[0].movable_sprites)

        for entity in sorted(level[0].all_sprites, key=lambda x: x.ID):
            if entity.__class__.__name__ == "MovingPlatform":
                entity.update(level[0].movable_sprites)

            if entity.__class__.__name__ == "Button":
                entity.update(level[0].movable_sprites, level[0].all_sprites)

            if entity.__class__.__name__ == "Cube":
                entity.update(level[0].movable_sprites)
                entity.update(level[0].platforms)

            if entity.__class__.__name__ == "Player":
                entity.update(level[0].movable_sprites)
                entity.update(level[0].platforms)

        for entity in sorted(level[0].all_sprites, key=lambda x: x.draw_layer):
            displaysurface.blit(entity.surf, entity.rect)

        pygame.display.update()
        FramePerSec.tick(config['FPS'])


if __name__ == "__main__":
    main()
