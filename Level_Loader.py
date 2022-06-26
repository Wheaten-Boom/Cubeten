import json
import pygame
from pygame.locals import *
import objects
import os


class Level():

    def __init__(self, level_number, sub_level_number) -> None:
        self.level_number = level_number
        self.sub_level_number = sub_level_number
        self.all_sprites = pygame.sprite.Group()
        self.platforms = pygame.sprite.Group()

        with open(os.path.join(os.path.dirname(__file__), 'levels', str(self.level_number) + ".json")) as level_file:
            level = json.load(level_file)

        level_properties = level[self.sub_level_number]

        for sprite in level_properties:
            if (sprite == "PLATFORM"):
                sprite_properties = level_properties[sprite]
                new_platform = objects.Platform(sprite_properties["POS_X"], sprite_properties["POS_Y"], sprite_properties["WIDTH"],
                                                    sprite_properties["HEIGHT"], 0xFF0000)

                self.all_sprites.add(new_platform)
                self.platforms.add(new_platform)
