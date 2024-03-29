import pygame
from pygame.locals import *

from settings import config


def run_level(level, screen):
    pygame.init()
    FramePerSec = pygame.time.Clock()

    # current_sublevel is the index of the sublevel being played in the sublevel list.
    current_sublevel = 0

    while True:
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_UP]:
            level[current_sublevel].player.jump(
                level[current_sublevel].all_sprites)

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
                if event.type == KEYDOWN:
                    if event.key == K_SPACE:
                        # Hold an object
                        success = level[current_sublevel].player.hold_object(
                            level[current_sublevel].all_sprites, level[current_sublevel].movable_sprites)
                        if success == True:
                            if level[current_sublevel].player.is_holding:
                                groups = level[current_sublevel].player.held_object.groups(
                                )
                                level[current_sublevel].player.held_object.kill()
                                level[current_sublevel].player.held_object.add(
                                    level[current_sublevel].all_sprites)
                            else:
                                level[current_sublevel].player.held_object.add(
                                    groups)
                                level[current_sublevel].player.held_object = None

                        # Switch a sublevel
                        for switching_panel in level[current_sublevel].switching_panels:
                            switching_panel.switch_level(
                                level[current_sublevel].player, level)

                        # Activate a switch
                        for button in level[current_sublevel].buttons:
                            button.update(
                                level[current_sublevel].movable_sprites, level[current_sublevel].player, level)

        screen.fill(level[current_sublevel].bg_color)

        level[current_sublevel].player.move()
        for entity in level[current_sublevel].cubes:
            entity.move(level[current_sublevel].movable_sprites)

        for entity in sorted(level[current_sublevel].all_sprites, key=lambda x: x.ID):
            if entity.__class__.__name__ == "MovingPlatform":
                entity.update(level[current_sublevel].movable_sprites)

            elif entity.__class__.__name__ == "Button":
                if entity.mode == "BUTTON":
                    entity.update(
                        level[current_sublevel].movable_sprites, level[current_sublevel].player, level)

            elif entity.__class__.__name__ == "Cube":
                entity.update(level[current_sublevel].movable_sprites)
                entity.update(level[current_sublevel].platforms)

            elif entity.__class__.__name__ == "Player":
                entity.update(level[current_sublevel].movable_sprites)
                entity.update(level[current_sublevel].platforms)

        for entity in sorted(level[current_sublevel].all_sprites, key=lambda x: x.draw_layer):
            screen.blit(entity.surf, entity.rect)

        pygame.display.update()
        FramePerSec.tick(config['FPS'])
        current_sublevel = level[-1]
