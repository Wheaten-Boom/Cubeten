import json
import pygame
import objects
import os


def Create_Level_File(data, filename):
    with open(os.path.join(os.path.dirname(__file__), 'levels', filename), "w") as file:
        json.dump(data, file, indent=4)


def Data_Assembler(all_sprites):
    data = {"SUB_LEVELS": ["SUBLEVEL_0"], "SUBLEVEL_0": {"PLATFORMS": []}}
    for sprite in all_sprites:
        if type(sprite) == objects.Platform:
            new_platform = {"POS_X": int(sprite.pos.x), "POS_Y": int(sprite.pos.y), "WIDTH": int(sprite.width),
                            "HEIGHT": int(sprite.height), "COLOR": sprite.color, "ID": sprite.ID, "DRAW_LAYER": sprite.draw_layer}

            data["SUBLEVEL_0"]["PLATFORMS"].append(new_platform)

    return data
