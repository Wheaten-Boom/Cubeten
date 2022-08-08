import os
import json
import pygame
from pygame.locals import *
import pygame_gui
from pygame_gui import *
from objects import *


class SubLevel():
    def __init__(self, sublevel_number):
        self.sublevel_number = sublevel_number
        self.all_sprites = pygame.sprite.Group()
        self.id_count = 0
        self.current_sprite = None
        self.original_draw_pos = None
        self.creating_sprite = False
        self.selected_sprite = None
        self.creation_type = None
        self.bg_color = "0xAFDEEF"


def Create_Level_File(data, filename):
    with open(os.path.join(os.path.dirname(__file__), "levels", filename), "w") as file:
        json.dump(data, file, indent=4)


def Data_Assembler(levels):
    level_count = 0
    # A copy of levels but without empty sublevels
    clean_levels = [level for level in levels if level.all_sprites]
    data = {"SUB_LEVELS": []}
    for level in clean_levels:
        data["SUB_LEVELS"].append("SUB_LEVEL_" + str(level_count))
        level_count += 1

    for index, sub_level in enumerate(data["SUB_LEVELS"]):
        data[sub_level] = {"BG_COLOR": "0xAFDEEF",
                           "PLATFORMS": [], "MOVING_PLATFORMS": [], "PLAYER": {}}

        for sprite in clean_levels[index].all_sprites:
            if type(sprite) == Platform:
                new_platform = {"POS_X": int(sprite.rect.left) - 300,
                                "POS_Y": int(sprite.rect.top),
                                "WIDTH": int(sprite.rect.width),
                                "HEIGHT": int(sprite.rect.height),
                                "COLOR": "0x" + rgb_to_hex(sprite.color),
                                "ID": sprite.ID,
                                "DRAW_LAYER": sprite.draw_layer}

                data[sub_level]["PLATFORMS"].append(new_platform)

            elif type(sprite) == MovingPlatform:
                new_moving_platform = {"X1": int(sprite.start_pos[0]) - 300,
                                       "Y1": int(sprite.start_pos[1]),
                                       "X2": int(sprite.end_pos[0]) - 300,
                                       "Y2": int(sprite.end_pos[1]),
                                       "SPEED": int(sprite.speed),
                                       "WIDTH": int(sprite.rect.width),
                                       "HEIGHT": int(sprite.rect.height),
                                       "COLOR": "0x" + rgb_to_hex(sprite.color),
                                       "IS_ACTIVE": sprite.isActive,
                                       "ID": sprite.ID,
                                       "DRAW_LAYER": sprite.draw_layer}

                data[sub_level]["MOVING_PLATFORMS"].append(new_moving_platform)

            elif type(sprite) == Player:
                new_player = {"POS_X": int(sprite.rect.left) - 300,
                              "POS_Y": int(sprite.rect.top),
                              "WIDTH": int(sprite.rect.width),
                              "HEIGHT": int(sprite.rect.height),
                              "COLOR": "0x" + rgb_to_hex(sprite.color),
                              "ID": sprite.ID,
                              "DRAW_LAYER": sprite.draw_layer}

                data[sub_level]["PLAYER"] = new_player

    return data


def is_mouse_on_sprite(sprite_list, mouse_pos):
    for sprite in sprite_list:
        if sprite.rect.collidepoint(mouse_pos):
            return True
    return False


def draw_outline(sprite, color):
    outline_rect = sprite.rect.copy()
    outline_rect.inflate_ip((outline_rect.width + outline_rect.height) / 25,
                            (outline_rect.width + outline_rect.height) / 25)
    pygame.draw.rect(displaysurface, color, outline_rect, int(
        (outline_rect.width + outline_rect.height) / 50))


def rgb_to_hex(rgb):
    return "%02x%02x%02x" % rgb


# !: This currently doesn't allow changing the text entrys manually, since it overwrites our input with the set_text().
# !: Fix this future me please. ;-;
def update_selected_sprite(sprite, color):
    # If we do have a sprite selected, draw an outline around it
    if sprite is not None:
        sprite.color = color
        sprite.surf.fill(sprite.color)

        if type(sprite) is MovingPlatform:
            selection_sprite = Platform(sprite.end_pos[0],
                                        sprite.end_pos[1],
                                        sprite.rect.width,
                                        sprite.rect.height,
                                        sprite.color,
                                        sprite.ID,
                                        sprite.draw_layer)

            update_selected_sprite(selection_sprite, "0xFFFFFF")

            if sprite.end_pos != selection_sprite.rect.topleft:
                sprite.end_pos = selection_sprite.rect.topleft
                pos_x2_text_entry.set_text(str(sprite.end_pos[0] - 300))
                pos_y2_text_entry.set_text(str(sprite.end_pos[1]))
                speed_text_entry.set_text(str(sprite.speed))

            pos_x2_text.visible = True
            pos_x2_text_entry.visible = True
            pos_y2_text.visible = True
            pos_y2_text_entry.visible = True
            speed_text.visible = True
            speed_text_entry.visible = True

        else:
            pos_x2_text.visible = False
            pos_x2_text_entry.visible = False
            pos_y2_text.visible = False
            pos_y2_text_entry.visible = False
            speed_text.visible = False
            speed_text_entry.visible = False

        if (pygame.mouse.get_pressed()[0]
                and sprite.rect.collidepoint(pygame.mouse.get_pos())):
            # Adds pygame.mouse.get_rel() to the sprite's position (drags it)
            new_pos = tuple(map(lambda i, j: i + j,
                                sprite.rect.topleft,
                                pygame.mouse.get_rel()))
            # If the sprite didn't move we don't want to update the position, this is to allow us to type new values in the text entry boxes
            if sprite.rect.topleft != new_pos:
                # Checks we aren't dragging it outside of the screen
                if new_pos[0] >= 300 and new_pos[0] + sprite.rect.width <= 1300:
                    sprite.rect.left = new_pos[0]
                if new_pos[1] >= 0 and new_pos[1] + sprite.rect.height <= 1000:
                    sprite.rect.top = new_pos[1]

        # Updates the text box with the sprite's position
        pos_x_text_entry.set_text(str(
            sprite.rect.left - 300))
        pos_y_text_entry.set_text(str(
            sprite.rect.top))
        width_text_entry.set_text(str(
            sprite.rect.width))
        height_text_entry.set_text(str(
            sprite.rect.height))

        draw_outline(sprite, "0xF5F97E")

    # If we don't have a sprite selected, clear the text box
    else:
        pos_x_text_entry.set_text("")
        pos_y_text_entry.set_text("")
        width_text_entry.set_text("")
        height_text_entry.set_text("")
        pos_x2_text_entry.set_text("")
        pos_y2_text_entry.set_text("")
        speed_text_entry.set_text("")


def main():
    pygame.init()
    clock = pygame.time.Clock()

    global displaysurface
    displaysurface = pygame.display.set_mode((1600, 1000))
    manager = pygame_gui.UIManager((1600, 1000), PackageResource(
        "assets.themes", "editor_theme.json"))

    left_panel = pygame_gui.elements.UIPanel(relative_rect=pygame.Rect(0, 0, 300, 1000),
                                             starting_layer_height=0,
                                             manager=manager)

    previous_level_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(50, 0, 100, 50),
                                                         text="PREV",
                                                         manager=manager,
                                                         container=left_panel,
                                                         object_id="prev_level_button")
    previous_level_button.disable()

    next_level_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(150, 0, 100, 50),
                                                     text="NEXT",
                                                     manager=manager,
                                                     container=left_panel,
                                                     object_id="next_level_button")

    create_platform_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(50, 100, 200, 50),
                                                          text="PLAT",
                                                          manager=manager,
                                                          container=left_panel,
                                                          object_id="#PLATFORM_BUTTON")

    create_moving_platform_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(50, 180, 200, 50),
                                                                 text="MOV PLAT",
                                                                 manager=manager,
                                                                 container=left_panel,
                                                                 object_id="#MOVING_PLATFORM_BUTTON")

    create_player_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(50, 260, 200, 50),
                                                        text="PLAYER",
                                                        manager=manager,
                                                        container=left_panel,
                                                        object_id="#PLAYER_BUTTON")

    right_panel = pygame_gui.elements.UIPanel(relative_rect=pygame.Rect(1300, 0, 300, 1000),
                                              starting_layer_height=0,
                                              manager=manager)

    clear_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(15, 900, 125, 75),
                                                text="CLEAR",
                                                manager=manager,
                                                container=right_panel,
                                                object_id="#CLEAR_BUTTON")

    save_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(155, 900, 125, 75),
                                               text="SAVE",
                                               manager=manager,
                                               container=right_panel,
                                               object_id="#SAVE_BUTTON")

    delete_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(85, 800, 125, 75),
                                                 text="DELETE",
                                                 manager=manager,
                                                 container=right_panel,
                                                 object_id="#DELETE_BUTTON")

    red_slider = pygame_gui.elements.UIHorizontalSlider(relative_rect=pygame.Rect(40, 25, 250, 30),
                                                        start_value=0,
                                                        value_range=(0, 255),
                                                        manager=manager,
                                                        container=right_panel,
                                                        object_id="#RED_COLOR_SLIDER")

    red__rgb_text = pygame_gui.elements.UILabel(relative_rect=pygame.Rect(15, 20, -1, -1),
                                                text="R:",
                                                manager=manager,
                                                container=right_panel,
                                                object_id="#RGB_TEXT")

    green_slider = pygame_gui.elements.UIHorizontalSlider(relative_rect=pygame.Rect(40, 70, 250, 30),
                                                          start_value=0,
                                                          value_range=(0, 255),
                                                          manager=manager,
                                                          container=right_panel,
                                                          object_id="#GREEN_COLOR_SLIDER")

    green__rgb_text = pygame_gui.elements.UILabel(relative_rect=pygame.Rect(15, 65, -1, -1),
                                                  text="G:",
                                                  manager=manager,
                                                  container=right_panel,
                                                  object_id="#RGB_TEXT")

    blue_slider = pygame_gui.elements.UIHorizontalSlider(relative_rect=pygame.Rect(40, 115, 250, 30),
                                                         start_value=0,
                                                         value_range=(0, 255),
                                                         manager=manager,
                                                         container=right_panel,
                                                         object_id="#BLUE_COLOR_SLIDER")

    blue__rgb_text = pygame_gui.elements.UILabel(relative_rect=pygame.Rect(15, 110, -1, -1),
                                                 text="B:",
                                                 manager=manager,
                                                 container=right_panel,
                                                 object_id="#RGB_TEXT")

    global pos_x_text
    pos_x_text = pygame_gui.elements.UILabel(relative_rect=pygame.Rect(15, 200, -1, -1),
                                             text="X:",
                                             manager=manager,
                                             container=right_panel,
                                             object_id="#POS_X_TEXT")

    global pos_x_text_entry
    pos_x_text_entry = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect(40, 200, 75, 50),
                                                           manager=manager,
                                                           container=right_panel,
                                                           object_id="#POS_X_TEXT_ENTRY")
    pos_x_text_entry.set_allowed_characters("numbers")
    pos_x_text_entry.set_text_length_limit(4)

    global pos_y_text
    pos_y_text = pygame_gui.elements.UILabel(relative_rect=pygame.Rect(15, 250, -1, -1),
                                             text="Y:",
                                             manager=manager,
                                             container=right_panel,
                                             object_id="#POS_Y_TEXT")

    global pos_y_text_entry
    pos_y_text_entry = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect(40, 250, 75, 50),
                                                           manager=manager,
                                                           container=right_panel,
                                                           object_id="#POS_Y_TEXT_ENTRY")
    pos_y_text_entry.set_allowed_characters("numbers")
    pos_y_text_entry.set_text_length_limit(4)

    global width_text
    width_text = pygame_gui.elements.UILabel(relative_rect=pygame.Rect(145, 200, -1, -1),
                                             text="W:",
                                             manager=manager,
                                             container=right_panel,
                                             object_id="#WIDTH_TEXT")

    global width_text_entry
    width_text_entry = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect(175, 200, 75, 50),
                                                           manager=manager,
                                                           container=right_panel,
                                                           object_id="#WIDTH_TEXT_ENTRY")
    width_text_entry.set_allowed_characters("numbers")
    width_text_entry.set_text_length_limit(4)

    global height_text
    height_text = pygame_gui.elements.UILabel(relative_rect=pygame.Rect(150, 250, -1, -1),
                                              text="H:",
                                              manager=manager,
                                              container=right_panel,
                                              object_id="#HEIGHT_TEXT")

    global height_text_entry
    height_text_entry = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect(175, 250, 75, 50),
                                                            manager=manager,
                                                            container=right_panel,
                                                            object_id="#HEIGHT_TEXT_ENTRY")
    height_text_entry.set_allowed_characters("numbers")
    height_text_entry.set_text_length_limit(4)

    global pos_x2_text
    pos_x2_text = pygame_gui.elements.UILabel(relative_rect=pygame.Rect(3, 300, -1, -1),
                                              text="X2:",
                                              manager=manager,
                                              container=right_panel,
                                              object_id="#POS_X2_TEXT",
                                              visible=False)

    global pos_x2_text_entry
    pos_x2_text_entry = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect(40, 300, 75, 50),
                                                            manager=manager,
                                                            container=right_panel,
                                                            object_id="#POS_X2_TEXT_ENTRY",
                                                            visible=False)
    pos_x2_text_entry.set_allowed_characters("numbers")
    pos_x2_text_entry.set_text_length_limit(4)

    global pos_y2_text
    pos_y2_text = pygame_gui.elements.UILabel(relative_rect=pygame.Rect(3, 350, -1, -1),
                                              text="Y2:",
                                              manager=manager,
                                              container=right_panel,
                                              object_id="#POS_Y2_TEXT",
                                              visible=False)

    global pos_y2_text_entry
    pos_y2_text_entry = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect(40, 350, 75, 50),
                                                            manager=manager,
                                                            container=right_panel,
                                                            object_id="#POS_Y2_TEXT_ENTRY",
                                                            visible=False)
    pos_y2_text_entry.set_allowed_characters("numbers")
    pos_y2_text_entry.set_text_length_limit(4)

    global speed_text
    speed_text = pygame_gui.elements.UILabel(relative_rect=pygame.Rect(15, 400, -1, -1),
                                             text="S:",
                                             manager=manager,
                                             container=right_panel,
                                             object_id="#SPEED_TEXT",
                                             visible=False)

    global speed_text_entry
    speed_text_entry = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect(40, 400, 75, 50),
                                                           manager=manager,
                                                           container=right_panel,
                                                           object_id="#SPEED_TEXT_ENTRY",
                                                           visible=False)
    speed_text_entry.set_allowed_characters("numbers")
    speed_text_entry.set_text_length_limit(4)

    global error_text
    error_text = pygame_gui.elements.UITextBox(relative_rect=pygame.Rect(45, 700, 200, 100),
                                               html_text="",
                                               manager=manager,
                                               container=right_panel,
                                               object_id="#ERROR_TEXT")

    levels = []
    levels.append(SubLevel(0))
    current_sub_level = 0
    levels[current_sub_level].creation_type = None

    while True:
        delta_time = clock.tick(240) / 1000

        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_ESCAPE]:
            pygame.quit()
            quit()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                quit()

            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == previous_level_button:
                    if current_sub_level > 0:
                        current_sub_level -= 1
                        next_level_button.enable()
                        if current_sub_level == 0:
                            previous_level_button.disable()

                if event.ui_element == next_level_button:
                    if current_sub_level < 256:
                        current_sub_level += 1
                        previous_level_button.enable()
                        if current_sub_level == 255:
                            next_level_button.disable()
                        if current_sub_level >= len(levels):
                            levels.append(SubLevel(current_sub_level))

                if event.ui_element == create_platform_button:
                    levels[current_sub_level].creation_type = Platform

                if event.ui_element == create_moving_platform_button:
                    levels[current_sub_level].creation_type = MovingPlatform

                if event.ui_element == create_player_button:
                    levels[current_sub_level].creation_type = Player

                if event.ui_element == clear_button:
                    levels[current_sub_level].all_sprites.empty()
                    levels[current_sub_level].id_count = 0
                    levels[current_sub_level].current_sprite = None
                    levels[current_sub_level].original_draw_pos = None
                    levels[current_sub_level].creating_sprite = False
                    levels[current_sub_level].selected_sprite = None
                    create_player_button.enable()

                if event.ui_element == save_button:
                    data = Data_Assembler(levels)
                    Create_Level_File(data, "TEST.json")

                if event.ui_element == delete_button:
                    if levels[current_sub_level].selected_sprite is not None:
                        levels[current_sub_level].all_sprites.remove(
                            levels[current_sub_level].selected_sprite)
                        if (type(levels[current_sub_level].selected_sprite) == Player):
                            create_player_button.enable()
                        levels[current_sub_level].selected_sprite = None

            if event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED:
                if event.ui_element == pos_x_text_entry:
                    if event.text:
                        if int(event.text) >= 0 and int(event.text) + levels[current_sub_level].selected_sprite.rect.width <= 1000:
                            levels[current_sub_level].selected_sprite.rect.left = int(
                                event.text) + 300
                            error_text.set_text("")
                        else:
                            error_text.set_text("POS X IS OUT OF BOUNDS!")
                if event.ui_element == pos_y_text_entry:
                    if event.text:
                        if int(event.text) >= 0 and int(event.text) + levels[current_sub_level].selected_sprite.rect.height <= 1000:
                            levels[current_sub_level].selected_sprite.rect.top = int(
                                event.text)
                            error_text.set_text("")
                        else:
                            error_text.set_text("POS Y IS OUT OF BOUNDS!")
                if event.ui_element == width_text_entry:
                    if event.text:
                        if int(event.text) > 0 and int(event.text) + levels[current_sub_level].selected_sprite.rect.left <= 1300:
                            levels[current_sub_level].selected_sprite.surf = pygame.Surface(
                                (int(event.text), levels[current_sub_level].selected_sprite.rect.height))
                            levels[current_sub_level].selected_sprite.rect.width = int(
                                event.text)
                            error_text.set_text("")
                        else:
                            error_text.set_text("WIDTH GOES OUT OF BOUNDS!")
                if event.ui_element == height_text_entry:
                    if event.text:
                        if int(event.text) > 0 and int(event.text) + levels[current_sub_level].selected_sprite.rect.top <= 1000:
                            levels[current_sub_level].selected_sprite.surf = pygame.Surface(
                                (levels[current_sub_level].selected_sprite.rect.width, int(event.text)))
                            levels[current_sub_level].selected_sprite.rect.height = int(
                                event.text)
                            error_text.set_text("")
                        else:
                            error_text.set_text("HEIGHT GOES OUT OF BOUNDS!")

            manager.process_events(event)

        # Check whether the mouse left click is pressed
        if pygame.mouse.get_pressed()[0]:
            mouse_pos = pygame.mouse.get_pos()
            # Check if the mouse is on the drawing area
            if mouse_pos[0] > 300 and mouse_pos[0] < 1300 and mouse_pos[1] > 0 and mouse_pos[1] < 1000:
                # If we didn't already create a sprite, create one
                if not levels[current_sub_level].creating_sprite:
                    # If the mouse is on a sprite, select that sprite
                    if is_mouse_on_sprite(levels[current_sub_level].all_sprites, mouse_pos):
                        for sprite in levels[current_sub_level].all_sprites:
                            if sprite.rect.collidepoint(mouse_pos):
                                if sprite is levels[current_sub_level].selected_sprite:
                                    break

                                levels[current_sub_level].selected_sprite = sprite
                                levels[current_sub_level].creation_type = type(
                                    levels[current_sub_level].selected_sprite)
                                red_slider.set_current_value(sprite.color[0])
                                green_slider.set_current_value(sprite.color[1])
                                blue_slider.set_current_value(sprite.color[2])
                                pos_x_text_entry.set_text(str(
                                    levels[current_sub_level].selected_sprite.rect.left - 300))
                                pos_y_text_entry.set_text(str(
                                    levels[current_sub_level].selected_sprite.rect.top))
                                width_text_entry.set_text(str(
                                    levels[current_sub_level].selected_sprite.rect.width))
                                height_text_entry.set_text(str(
                                    levels[current_sub_level].selected_sprite.rect.height))

                    else:
                        if levels[current_sub_level].creation_type is not None and levels[current_sub_level].selected_sprite is None:
                            levels[current_sub_level].creating_sprite = True
                            levels[current_sub_level].selected_sprite = None

                            if levels[current_sub_level].creation_type == Platform:
                                levels[current_sub_level].current_sprite = Platform(mouse_pos[0],
                                                                                    mouse_pos[1],
                                                                                    1, 1,
                                                                                    current_selected_color,
                                                                                    levels[current_sub_level].id_count,
                                                                                    0)
                                levels[current_sub_level].original_draw_pos = (mouse_pos[0],
                                                                               mouse_pos[1])

                            if levels[current_sub_level].creation_type == MovingPlatform:

                                levels[current_sub_level].current_sprite = MovingPlatform(mouse_pos[0], mouse_pos[1],
                                                                                          mouse_pos[0], mouse_pos[1],
                                                                                          1,
                                                                                          1, 1,
                                                                                          current_selected_color,
                                                                                          levels[current_sub_level].id_count,
                                                                                          0,
                                                                                          True)
                                levels[current_sub_level].original_draw_pos = (mouse_pos[0],
                                                                               mouse_pos[1])

                            if levels[current_sub_level].creation_type == Player:
                                levels[current_sub_level].current_sprite = Player(mouse_pos[0],
                                                                                  mouse_pos[1],
                                                                                  75, 75,
                                                                                  current_selected_color,
                                                                                  levels[current_sub_level].id_count,
                                                                                  1)

                                levels[current_sub_level].current_sprite.surf = pygame.Surface((levels[current_sub_level].current_sprite.rect.width,
                                                                                                levels[current_sub_level].current_sprite.rect.height))
                                levels[current_sub_level].current_sprite.surf.fill(
                                    levels[current_sub_level].current_sprite.color)

                                levels[current_sub_level].creation_type = None

                # If we did create one, update the sprite
                elif (type(levels[current_sub_level].current_sprite) is not Player):
                    levels[current_sub_level].current_sprite.rect.left = min(levels[current_sub_level].original_draw_pos[0],
                                                                             mouse_pos[0])
                    levels[current_sub_level].current_sprite.rect.top = min(levels[current_sub_level].original_draw_pos[1],
                                                                            mouse_pos[1])
                    levels[current_sub_level].current_sprite.rect.width = abs(mouse_pos[0]
                                                                              - levels[current_sub_level].original_draw_pos[0])
                    levels[current_sub_level].current_sprite.rect.height = abs(mouse_pos[1]
                                                                               - levels[current_sub_level].original_draw_pos[1])

                    levels[current_sub_level].current_sprite.surf = pygame.Surface((levels[current_sub_level].current_sprite.rect.width,
                                                                                    levels[current_sub_level].current_sprite.rect.height))
                    levels[current_sub_level].current_sprite.surf.fill(
                        levels[current_sub_level].current_sprite.color)

        # If the mouse left click is not pressed, stop creating a sprite and add it to the sprite group
        elif levels[current_sub_level].creating_sprite:
            levels[current_sub_level].creating_sprite = False
            levels[current_sub_level].all_sprites.add(
                levels[current_sub_level].current_sprite)
            levels[current_sub_level].selected_sprite = levels[current_sub_level].current_sprite
            pos_x_text_entry.set_text(
                str(levels[current_sub_level].selected_sprite.rect.left - 300))
            pos_y_text_entry.set_text(
                str(levels[current_sub_level].selected_sprite.rect.top))
            width_text_entry.set_text(
                str(levels[current_sub_level].selected_sprite.rect.width))
            height_text_entry.set_text(
                str(levels[current_sub_level].selected_sprite.rect.height))
            levels[current_sub_level].current_sprite = None
            levels[current_sub_level].original_draw_pos = None
            levels[current_sub_level].id_count += 1

        # Clears the selection if right click is pressed
        if pygame.mouse.get_pressed()[2]:
            levels[current_sub_level].selected_sprite = None
            error_text.set_text("")

        manager.update(delta_time)

        displaysurface.fill("0xAFDEEF")

        current_selected_color = (red_slider.get_current_value(),
                                  green_slider.get_current_value(),
                                  blue_slider.get_current_value())

        # Checks whether we have a player sprite created, if so then disable the create player button, else enable it
        if any(isinstance(x, Player) for x in levels[current_sub_level].all_sprites):
            create_player_button.disable()
        else:
            create_player_button.enable()

        update_selected_sprite(levels[current_sub_level].selected_sprite,
                               current_selected_color)

        # If we are creating a sprite, draw it
        if levels[current_sub_level].current_sprite is not None:
            displaysurface.blit(levels[current_sub_level].current_sprite.surf,
                                levels[current_sub_level].current_sprite.rect)

        # Draw all the sprites
        for entity in levels[current_sub_level].all_sprites:
            displaysurface.blit(entity.surf, entity.rect)

        manager.draw_ui(displaysurface)

        pygame.draw.rect(displaysurface, current_selected_color,
                         (1345, 157, 245, 27))

        pygame.mouse.get_rel()

        pygame.display.update()


if __name__ == "__main__":
    main()
