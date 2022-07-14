from distutils.command.build import build
import json
import pygame
from pygame.locals import *
import objects
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
    current_sublevel = 0

    while True:
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_UP]:
            level[current_sublevel].player.jump(level[current_sublevel].platforms)

        if pressed_keys[K_ESCAPE]:
            pygame.quit()
            quit()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                quit()

            if event.type == KEYUP:
                if event.key == K_UP:
                    level[current_sublevel].player.stop_jump()

            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    for switching_panel in level[current_sublevel].switching_panels:
                        switching_panel.Switch_Level(level[current_sublevel].player, level)
                    
                    for button in level[current_sublevel].buttons:
                        button.update(level[current_sublevel].movable_sprites, level[current_sublevel].all_sprites, level[current_sublevel].player)


        displaysurface.fill((0, 0, 0))

        level[current_sublevel].player.move(level[current_sublevel].platforms)

        for entity in level[current_sublevel].all_sprites:
            if entity.__class__.__name__ == "Button":
                if entity.mode == "BUTTON":
                    entity.update(
                        level[current_sublevel].movable_sprites, level[current_sublevel].all_sprites,level[current_sublevel].player)

            if entity.__class__.__name__ == "MovingPlatform":  
                entity.update(level[current_sublevel].movable_sprites)

            if entity.__class__.__name__ == "Player":
                entity.update(level[current_sublevel].platforms)

            displaysurface.blit(entity.surf, entity.rect)

        pygame.display.update()
        FramePerSec.tick(config['FPS'])
        current_sublevel = level[-1]


if __name__ == "__main__":
    main()
