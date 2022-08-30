import os
import json
import pygame
from pygame.locals import *
import objects


class Sub_Level():
    """
    A class that represents a sublevel.

    Used to contain details about a sublevel, such as the objects, groups, etc.
    """

    def __init__(self, level_name, sub_level_name):
        """
        Sub_Level constructor.

        Parameters:
            level_name (str): The name of the level.
            sub_level_name (str): The name of the sublevel.
        """
        self.level_name = level_name
        self.sub_level_name = sub_level_name
        self.all_sprites = pygame.sprite.Group()
        self.platforms = pygame.sprite.Group()
        self.moving_platforms = pygame.sprite.Group()
        self.buttons = pygame.sprite.Group()
        self.cubes = pygame.sprite.Group()
        self.switching_panels = pygame.sprite.Group()
        self.movable_sprites = pygame.sprite.Group()
        self.bg_color = "0x000000"

        with open(os.path.join(os.path.dirname(__file__), 'levels', str(self.level_name) + ".json")) as level_file:
            level_file = json.load(level_file)

        level_properties = level_file[self.sub_level_name]

        # Goes through the level properties and creates the objects and adds them to the appropriate groups.
        for data in level_properties:

            if (data == "BG_COLOR"):
                self.bg_color = level_properties["BG_COLOR"]

            if (data == "PLATFORMS"):

                for platform in level_properties["PLATFORMS"]:

                    new_platform = objects.Platform(platform["POS_X"], platform["POS_Y"], platform["WIDTH"],
                                                    platform["HEIGHT"], platform["COLOR"], platform["ID"], platform["DRAW_LAYER"])

                    self.all_sprites.add(new_platform)
                    self.platforms.add(new_platform)

            if (data == "MOVING_PLATFORMS"):

                for platform in level_properties["MOVING_PLATFORMS"]:

                    new_platform = objects.MovingPlatform(platform["X1"], platform["Y1"], platform["X2"], platform["Y2"], platform["SPEED"], platform["WIDTH"],
                                                          platform["HEIGHT"], platform["COLOR"], platform["ID"], platform["DRAW_LAYER"], platform["IS_ACTIVE"])

                    self.all_sprites.add(new_platform)
                    self.platforms.add(new_platform)
                    self.moving_platforms.add(new_platform)

            if (data == "BUTTONS"):
                for button in level_properties["BUTTONS"]:
                    new_button = objects.Button(button["POS_X"], button["POS_Y"], button["WIDTH"],
                                                button["HEIGHT"], button["COLOR"], button["ACTIVATE_COLOR"], button["ACTIVATE_ACTION"], button["DEACTIVATE_ACTION"], button["MODE"], button["ID"], button["DRAW_LAYER"], button["IS_ACTIVE"])

                    self.all_sprites.add(new_button)
                    self.buttons.add(new_button)

                    if new_button.mode == "BUTTON":
                        self.platforms.add(new_button)

            if (data == "SWITCHING_PANELS"):

                for panel in level_properties["SWITCHING_PANELS"]:

                    new_panel = objects.SwitchingPanel(panel["POS_X"], panel["POS_Y"], panel["WIDTH"],
                                                       panel["HEIGHT"], panel["COLOR"], panel["LEVEL_ID"], panel["ID"], panel["DRAW_LAYER"])

                    self.all_sprites.add(new_panel)
                    self.switching_panels.add(new_panel)

            if (data == "CUBES"):
                for cube in level_properties["CUBES"]:
                    new_cube = objects.Cube(cube["POS_X"], cube["POS_Y"], cube["WIDTH"],
                                            cube["HEIGHT"], cube["COLOR"], cube["ID"], cube["DRAW_LAYER"])

                    self.all_sprites.add(new_cube)
                    self.cubes.add(new_cube)
                    self.movable_sprites.add(new_cube)

            if (data == "PLAYER"):

                player_properties = level_properties["PLAYER"]

                self.player = objects.Player(player_properties["POS_X"], player_properties["POS_Y"], player_properties["WIDTH"],
                                             player_properties["HEIGHT"], player_properties["COLOR"], player_properties["ID"], player_properties["DRAW_LAYER"])

                self.all_sprites.add(self.player)
                self.movable_sprites.add(self.player)


def Load(level_name) -> dict:
    """
    Reads the level file and returns a dictionary of all the sublevels in the level.

    Parameters:
        level_name (str): The name of the level file.
    """
    sub_levels = []

    with open(os.path.join(os.path.dirname(__file__), 'levels', str(level_name) + ".json")) as level_file:
        level_file = json.load(level_file)

    # Runs through a lookup table of all the sublevel's names so the sub_level constructor can find their properties.
    for sub_level in level_file["SUB_LEVELS"]:
        sub_levels.append(Sub_Level(level_name, sub_level))

    sub_levels.append(0)

    return sub_levels
