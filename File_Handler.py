import json
import pygame
import objects


def Create_Level_File(data, filename):
    with open(filename, "w") as file:
        json.dump(data, file, indent=4)


def Data_Assembler(all_sprites):
    data = {"PLATFORMS": []}
    for sprite in all_sprites:
        if type(sprite) == objects.Platform:
            new_platform = {"POS_X": sprite.pos.x, "POS_Y": sprite.pos.y, "WIDTH": sprite.width,
                            "HEIGHT": sprite.height, "COLOR": sprite.color, "ID": sprite.ID, "DRAW_LAYER": sprite.draw_layer}

            data["PLATFORMS"].append(new_platform)

    return data
