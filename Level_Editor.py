import os
import json
import pygame
from pygame.locals import *
from objects import *


def Create_Level_File(data, filename):
    with open(os.path.join(os.path.dirname(__file__), 'levels', filename), "w") as file:
        json.dump(data, file, indent=4)


def Data_Assembler(all_sprites):
    data = {"SUB_LEVELS": ["SUBLEVEL_0"], "SUBLEVEL_0": {"PLATFORMS": []}}
    for sprite in all_sprites:
        if type(sprite) == Platform:
            new_platform = {"POS_X": int(sprite.pos.x), "POS_Y": int(sprite.pos.y), "WIDTH": int(sprite.width),
                            "HEIGHT": int(sprite.height), "COLOR": sprite.color, "ID": sprite.ID, "DRAW_LAYER": sprite.draw_layer}

            data["SUBLEVEL_0"]["PLATFORMS"].append(new_platform)

    return data


def update_sprite(mouse_x, mouse_y, original_x, original_y, sprite):
    sprite.surf = pygame.Surface(
        (abs(mouse_x - sprite.pos.x), abs(mouse_y - sprite.pos.y)))
    sprite.surf.fill(sprite.color)
    sprite.rect.topleft = (min(original_x, mouse_x), min(original_y, mouse_y))
    sprite.width = abs(mouse_x - sprite.pos.x)
    sprite.height = abs(mouse_y - sprite.pos.y)


def main():

    pygame.init()
    FramePerSec = pygame.time.Clock()

    displaysurface = pygame.display.set_mode((1000, 1000))
    all_sprits = pygame.sprite.Group()
    recent_sprites = []
    create_new_sprite = True

    while True:

        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_ESCAPE]:
            pygame.quit()
            quit()

        if pressed_keys[K_e]:
            data = Data_Assembler(all_sprits)
            Create_Level_File(data, "TEST.json")

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                quit()

        if pygame.mouse.get_pressed(num_buttons=3)[0] == True:

            if create_new_sprite == True:

                new_sprite = Platform(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[
                                      1], 0, 0, "0x2c5160", 2, 1)
                all_sprits.add(new_sprite)
                recent_sprites.append(
                    (pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]))
                recent_sprites.append(new_sprite)
                create_new_sprite = False

            else:
                update_sprite(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[
                              1], recent_sprites[-2][0], recent_sprites[-2][1], recent_sprites[-1])

        else:
            create_new_sprite = True

        displaysurface.fill((0, 0, 0))
        for entity in all_sprits:
            displaysurface.blit(entity.surf, entity.rect)

        pygame.display.update()
        FramePerSec.tick(60)


if __name__ == "__main__":
    main()
