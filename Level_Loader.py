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
        self.buttons = pygame.sprite.Group()
        self.switching_panels = pygame.sprite.Group()
        self.movable_sprites = pygame.sprite.Group()

        with open(os.path.join(os.path.dirname(__file__), 'levels', str(self.level_number) + ".json")) as level_file:
            level_file = json.load(level_file)

        level_properties = level_file[self.sub_level_number]

        for data in level_properties:

            if (data == "PLATFORMS"):

                for platform in level_properties["PLATFORMS"]:

                    new_platform = objects.Platform(platform["POS_X"], platform["POS_Y"], platform["WIDTH"],
                                                    platform["HEIGHT"], platform["COLOR"], platform["ID"])

                    self.all_sprites.add(new_platform)
                    self.platforms.add(new_platform)

            if (data == "MOVING_PLATFORMS"):

                for platform in level_properties["MOVING_PLATFORMS"]:

                    new_platform = objects.MovingPlatform(platform["X1"], platform["Y1"], platform["X2"], platform["Y2"], platform["SPEED"], platform["WIDTH"],
                                                          platform["HEIGHT"], platform["COLOR"], platform["ID"], platform["IS_ACTIVE"])

                    self.all_sprites.add(new_platform)
                    self.platforms.add(new_platform)
                    self.moving_platforms.add(new_platform)

            if (data == "BUTTONS"):
                for button in level_properties["BUTTONS"]:
                    new_button = objects.Button(button["POS_X"], button["POS_Y"], button["WIDTH"],
                                                button["HEIGHT"], button["COLOR"], button["ACTIVATE_ACTION"], button["DEACTIVATE_ACTION"], button["ID"], button["MODE"], button["IS_ACTIVE"])

                    self.all_sprites.add(new_button)
                    self.buttons.add(new_button)

                    if new_button.mode == "BUTTON":
                        self.platforms.add(new_button)

            if (data == "SWITCHING_PANELS"):

                for panel in level_properties["SWITCHING_PANELS"]:

                    new_panel = objects.Switching_Panel(panel["POS_X"], panel["POS_Y"], panel["WIDTH"],
                                                    panel["HEIGHT"], panel["COLOR"], panel["ID"], panel["LEVEL_ID"])

                    self.all_sprites.add(new_panel)
                    self.switching_panels.add(new_panel)

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

    sub_levels.append(0)

    return sub_levels
