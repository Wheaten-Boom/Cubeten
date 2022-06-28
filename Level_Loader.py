import json
import pygame
from pygame.locals import *
import objects
import os


class Sub_Level():

    def __init__(self, level_number, sub_level_number) -> None:
        self.level_number = level_number
        self.sub_level_number = sub_level_number
        self.default_color = 0
        self.all_sprites = pygame.sprite.Group()
        self.platforms = pygame.sprite.Group()
        self.moving_platforms = pygame.sprite.Group()
        self.movable_sprites = pygame.sprite.Group()

        with open(os.path.join(os.path.dirname(__file__), 'levels', str(self.level_number) + ".json")) as level_file:
            level_file = json.load(level_file)

        level_properties = level_file[self.sub_level_number]

        for data in level_properties:

            if (data == "PLATFORMS"):

                for platform in level_properties["PLATFORMS"]:

                    new_platform = objects.Platform(platform["POS_X"], platform["POS_Y"], platform["WIDTH"],
                                                    platform["HEIGHT"], platform["COLOR"])

                    self.all_sprites.add(new_platform)
                    self.platforms.add(new_platform)

            if (data == "MOVING_PLATFORMS"):

                for platform in level_properties["MOVING_PLATFORMS"]:

                    new_platform = objects.MovingPlatform(platform["X1"], platform["Y1"], platform["X2"], platform["Y2"], platform["SPEED"], platform["WIDTH"],
                                                          platform["HEIGHT"], platform["COLOR"], platform["IS_ACTIVE"])

                    self.all_sprites.add(new_platform)
                    self.platforms.add(new_platform)
                    self.moving_platforms.add(new_platform)

            if (data == "PLAYER"):

                player_properties = level_properties["PLAYER"]

                self.player = objects.Player(player_properties["POS_X"], player_properties["POS_Y"], player_properties["WIDTH"],
                                             player_properties["HEIGHT"], player_properties["COLOR"])

                self.all_sprites.add(self.player)
                self.movable_sprites.add(self.player)


def Load(level_number):

    level_number = level_number
    sub_levels = []

    with open(os.path.join(os.path.dirname(__file__), 'levels', str(level_number) + ".json")) as level_file:
        level_file = json.load(level_file)

    for sub_level in level_file["SUB_LEVELS"]:
        sub_levels.append(Sub_Level(level_number, sub_level))

    return sub_levels
