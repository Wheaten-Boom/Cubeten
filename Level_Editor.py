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
                           "PLATFORMS": [], "MOVING_PLATFORMS": [], "BUTTONS": [], "PLAYER": {}}

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

            elif type(sprite) == Button:

                final_active_command = []
                for command in sprite.activate_actions.values():
                    for element in command:
                        final_active_command.append(element)

                final_inactive_command = []
                for command in sprite.deactivate_actions.values():
                    for element in command:
                        final_inactive_command.append(element)

                new_button = {
                    "POS_X": int(sprite.rect.left) - 300,
                    "POS_Y": int(sprite.rect.top),
                    "WIDTH": int(sprite.rect.width),
                    "HEIGHT": int(sprite.rect.height),
                    "COLOR": "0x" + rgb_to_hex(sprite.color),
                    "ACTIVATE_COLOR": "0x701010",
                    "ACTIVATE_ACTION": final_active_command,
                    "DEACTIVATE_ACTION": final_inactive_command,
                    "IS_ACTIVE": sprite.isActive,
                    "MODE": change_button_mode.text,
                    "ID": sprite.ID,
                    "DRAW_LAYER": sprite.draw_layer}

                data[sub_level]["BUTTONS"].append(new_button)

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


def calculate_complementary_color(rgb):
    return (255 - rgb[0], 255 - rgb[1], 255 - rgb[2])


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
                                        -1,
                                        sprite.draw_layer)

            update_selected_sprite(selection_sprite, "0xFFFFFF")

            # Updated the UI to prevent the recursion from giving the update_UI func a platform type.

            if not (pygame.mouse.get_pos()[0] > 1300):
                sprite.end_pos = selection_sprite.rect.topleft
                pos_x2_text_entry.set_text(str(sprite.end_pos[0] - 300))
                pos_y2_text_entry.set_text(str(sprite.end_pos[1]))
                speed_text_entry.set_text(str(sprite.speed))

        elif type(sprite) is Button:
            sprite.mode = change_button_mode.text  # update the button's mode

            if sprite.mode == "BUTTON":
                # Update the button's dimensions based on his state.
                sprite.rect.width = 75
                sprite.rect.height = 25
                sprite.surf = pygame.Surface(
                    (sprite.rect.width, sprite.rect.height))

                # Refill the surf with the selected color.
                sprite.color = color
                sprite.surf.fill(sprite.color)

            elif sprite.mode == "SWITCH":
                # Update the button's dimensions based on his state.
                sprite.rect.width = 25
                sprite.rect.height = 75
                sprite.surf = pygame.Surface(
                    (sprite.rect.width, sprite.rect.height))

                # Refill the surf with the selected color.
                sprite.color = color
                sprite.surf.fill(sprite.color)

            if (button_state_text.text == "ACTIVE"):  # update the button's state (isActive)
                sprite.isActive = True
            else:
                sprite.isActive = False

            global commands_panel
            if commands_panel.options_list != sprite.activate_actions.keys():
                commands_panel.kill()
                commands_panel = pygame_gui.elements.UIDropDownMenu(sprite.activate_actions.keys(), starting_option="",
                                                                    relative_rect=pygame.Rect(
                                                                    15, 420, 155, 40),
                                                                    manager=manager,
                                                                    container=right_panel,
                                                                    object_id="#COMMANDS",
                                                                    visible=True)

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

        if not (pygame.mouse.get_pos()[0] > 1300):
            # Updates the text box with the sprite's position (if the mouse is in the main container)
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


def update_UI(sprite):
    if sprite is None:
        return

    pos_x2_text.hide()
    pos_x2_text_entry.hide()
    pos_y2_text.hide()
    pos_y2_text_entry.hide()
    speed_text.hide()
    speed_text_entry.hide()
    change_button_mode.hide()
    button_mode_text.hide()
    change_button_state.hide()
    button_state_text.hide()
    commands_panel.hide()
    create_command.hide()
    delete_command.hide()
    selection_submit_button.hide()

    if type(sprite) is MovingPlatform or sprite.ID == -1:
        pos_x2_text.show()
        pos_x2_text_entry.show()
        pos_y2_text.show()
        pos_y2_text_entry.show()
        speed_text.show()
        speed_text_entry.show()

    elif type(sprite) is Button:
        change_button_mode.show()
        button_mode_text.show()
        change_button_state.show()
        button_state_text.show()
        commands_panel.show()
        create_command.show()
        delete_command.show()


def initiate_UI(manager):

    global left_panel
    left_panel = pygame_gui.elements.UIPanel(relative_rect=pygame.Rect(0, 0, 300, 1000),
                                             starting_layer_height=0,
                                             manager=manager)

    global previous_level_button
    previous_level_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(50, 0, 100, 50),
                                                         text="PREV",
                                                         manager=manager,
                                                         container=left_panel,
                                                         object_id="prev_level_button")
    previous_level_button.disable()

    global next_level_button
    next_level_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(150, 0, 100, 50),
                                                     text="NEXT",
                                                     manager=manager,
                                                     container=left_panel,
                                                     object_id="next_level_button")

    global create_platform_button
    create_platform_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(50, 100, 200, 50),
                                                          text="PLAT",
                                                          manager=manager,
                                                          container=left_panel,
                                                          object_id="#PLATFORM_BUTTON")

    global create_moving_platform_button
    create_moving_platform_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(50, 180, 200, 50),
                                                                 text="MOV PLAT",
                                                                 manager=manager,
                                                                 container=left_panel,
                                                                 object_id="#MOVING_PLATFORM_BUTTON")

    global create_player_button
    create_player_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(50, 260, 200, 50),
                                                        text="PLAYER",
                                                        manager=manager,
                                                        container=left_panel,
                                                        object_id="#PLAYER_BUTTON")

    global create_button_button
    create_button_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(50, 340, 200, 50),
                                                        text="BUTTON",
                                                        manager=manager,
                                                        container=left_panel,
                                                        object_id="#BUTTON_BUTTON")

    global right_panel
    right_panel = pygame_gui.elements.UIPanel(relative_rect=pygame.Rect(1300, 0, 300, 1000),
                                              starting_layer_height=0,

                                              manager=manager)
    global clear_button
    clear_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(15, 900, 125, 75),
                                                text="CLEAR",
                                                manager=manager,
                                                container=right_panel,
                                                object_id="#CLEAR_BUTTON")

    global save_button
    save_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(155, 900, 125, 75),
                                               text="SAVE",
                                               manager=manager,
                                               container=right_panel,
                                               object_id="#SAVE_BUTTON")

    global delete_button
    delete_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(85, 800, 125, 75),
                                                 text="DELETE",
                                                 manager=manager,
                                                 container=right_panel,
                                                 object_id="#DELETE_BUTTON")

    global red_slider
    red_slider = pygame_gui.elements.UIHorizontalSlider(relative_rect=pygame.Rect(40, 25, 250, 30),
                                                        start_value=0,
                                                        value_range=(0, 255),
                                                        manager=manager,
                                                        container=right_panel,
                                                        object_id="#RED_COLOR_SLIDER")

    global red__rgb_text
    red__rgb_text = pygame_gui.elements.UILabel(relative_rect=pygame.Rect(15, 20, -1, -1),
                                                text="R:",
                                                manager=manager,
                                                container=right_panel,
                                                object_id="#RGB_TEXT")

    global green_slider
    green_slider = pygame_gui.elements.UIHorizontalSlider(relative_rect=pygame.Rect(40, 70, 250, 30),
                                                          start_value=0,
                                                          value_range=(0, 255),
                                                          manager=manager,
                                                          container=right_panel,
                                                          object_id="#GREEN_COLOR_SLIDER")

    global green__rgb_text
    green__rgb_text = pygame_gui.elements.UILabel(relative_rect=pygame.Rect(15, 65, -1, -1),
                                                  text="G:",
                                                  manager=manager,
                                                  container=right_panel,
                                                  object_id="#RGB_TEXT")

    global blue_slider
    blue_slider = pygame_gui.elements.UIHorizontalSlider(relative_rect=pygame.Rect(40, 115, 250, 30),
                                                         start_value=0,
                                                         value_range=(0, 255),
                                                         manager=manager,
                                                         container=right_panel,
                                                         object_id="#BLUE_COLOR_SLIDER")

    global blue__rgb_text
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

    global button_mode_text
    button_mode_text = pygame_gui.elements.UILabel(relative_rect=pygame.Rect(10, 310, -1, -1),
                                                   text="M:",
                                                   manager=manager,
                                                   container=right_panel,
                                                   object_id="#BUTTON_MODE_TEXT",
                                                   visible=False)

    global change_button_mode
    change_button_mode = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(40, 310, 150, 55),
                                                      text="SWITCH",
                                                      manager=manager,
                                                      container=right_panel,
                                                      object_id="#BUTTON_MODE",
                                                      visible=False)

    global button_state_text
    button_state_text = pygame_gui.elements.UILabel(relative_rect=pygame.Rect(14, 365, -1, -1),
                                                    text="S:",
                                                    manager=manager,
                                                    container=right_panel,
                                                    object_id="#BUTTON_STATE_TEXT",
                                                    visible=False)

    global change_button_state
    change_button_state = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(40, 365, 150, 50),
                                                       text="ACTIVE",
                                                       manager=manager,
                                                       container=right_panel,
                                                       object_id="#BUTTON_STATE",
                                                       visible=False)

    global error_text
    error_text = pygame_gui.elements.UITextBox(relative_rect=pygame.Rect(45, 700, 200, 100),
                                               html_text="",
                                               manager=manager,
                                               container=right_panel,
                                               object_id="#ERROR_TEXT")

    global commands_panel
    commands_panel = pygame_gui.elements.UIDropDownMenu([], starting_option="",
                                                        relative_rect=pygame.Rect(
                                                        15, 420, 155, 40),
                                                        manager=manager,
                                                        container=right_panel,
                                                        object_id="#COMMANDS",
                                                        visible=False)

    global create_command
    create_command = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(175, 420, 40, 40),
                                                  text="+",
                                                  manager=manager,
                                                  container=right_panel,
                                                  object_id="#configure_command",
                                                  visible=False)

    global delete_command
    delete_command = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(210, 420, 40, 40),
                                                  text="-",
                                                  manager=manager,
                                                  container=right_panel,
                                                  object_id="#DELETE_COMMAND",
                                                  visible=False)

    global selection_submit_button
    selection_submit_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(245, 420, 40, 40),
                                                           text="V",
                                                           manager=manager,
                                                           container=right_panel,
                                                           object_id="#DELETE_COMMAND",
                                                           visible=False)

    global command_configuration_menu
    command_configuration_menu = pygame_gui.elements.UIWindow(rect=pygame.Rect(500, 250, 600, 400),
                                                              manager=manager,
                                                              window_display_title="Configure Command",
                                                              element_id="#COMMAND_CONFIGURATION_WINDOW",
                                                              resizable=False,
                                                              visible=False)

    global command_type_text
    command_type_text = pygame_gui.elements.UILabel(relative_rect=pygame.Rect(15, 60, -1, -1),
                                                    text="Command type: ",
                                                    manager=manager,
                                                    container=command_configuration_menu,
                                                    object_id="#COMMAND_TYPE_TEXT")

    global save_command
    save_command = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(15, 270, 100, 50),
                                                text="SAVE",
                                                manager=manager,
                                                container=command_configuration_menu,
                                                object_id="#SAVE_COMMAND_BUTTON")

    global running_condition_text
    running_condition_text = pygame_gui.elements.UILabel(relative_rect=pygame.Rect(15, 105, -1, -1),
                                                         text="Run when button is: ",
                                                         manager=manager,
                                                         container=command_configuration_menu,
                                                         object_id="#RUNNING_CONDITION_TEXT")

    global running_condition
    running_condition = pygame_gui.elements.UIDropDownMenu(["ACTIVE", "INACTIVE"],
                                                           starting_option="ACTIVE",
                                                           relative_rect=pygame.Rect(
                                                               370, 105, 150, 40),
                                                           manager=manager,
                                                           container=command_configuration_menu,
                                                           object_id="#RUNNING_CONDITION_BUTTON")

    global complementary_command_text
    complementary_command_text = pygame_gui.elements.UILabel(relative_rect=pygame.Rect(15, 150, -1, -1),
                                                             text="Complementary command: ",
                                                             manager=manager,
                                                             container=command_configuration_menu,
                                                             object_id="#COMPLEMENTARY_COMMAND_TEXT",
                                                             visible=False)

    global create_complementary_command
    create_complementary_command = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(400, 150, 100, 40),
                                                                text="TRUE",
                                                                manager=manager,
                                                                container=command_configuration_menu,
                                                                object_id="#CREATE_COMPLEMENTARY_COMMAND",
                                                                visible=False)

    global close_command_configurator
    close_command_configurator = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(425, 270, 130, 50),
                                                              text="CANCEL",
                                                              manager=manager,
                                                              container=command_configuration_menu,
                                                              object_id="#CLOSE_COMMAND_CONFIGURATOR",
                                                              visible=True)

    global command_name_text
    command_name_text = pygame_gui.elements.UILabel(relative_rect=pygame.Rect(15, 15, -1, -1),
                                                    text="Command name: ",
                                                    manager=manager,
                                                    container=command_configuration_menu,
                                                    object_id="#COMMAND_NAME_TEXT")

    global command_name_entry
    command_name_entry = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect(250, 15, 250, 40),
                                                             manager=manager,
                                                             container=command_configuration_menu,
                                                             object_id="#COMMAND_NAME_ENTRY",
                                                             visible=True)
    command_name_entry.set_text_length_limit(20)


def configure_command(selected_button):

    selection_submit_button.show()

    sprite_list = []  # Sprite list for drawing oulines.
    sprite_ID_list = []  # ID list for actual commands.
    mouse_click_enabled = True
    # The phase which the player selects the sprites he want to control.
    while selection_submit_button.check_pressed() == False:
        if pygame.mouse.get_pressed()[0] and mouse_click_enabled:
            mouse_pos = pygame.mouse.get_pos()
            mouse_click_enabled = False
            if is_mouse_on_sprite(levels[current_sub_level].all_sprites, mouse_pos):
                for sprite in levels[current_sub_level].all_sprites:
                    if sprite.rect.collidepoint(mouse_pos) and not sprite.ID in sprite_ID_list[0::2]:
                        sprite_ID_list.append(sprite.ID)
                        sprite_ID_list.append(current_sub_level)
                        # Add the sprite to a sprite list to later draw an outline around it.
                        sprite_list.append(sprite)

                    elif sprite.rect.collidepoint(mouse_pos) and sprite in sprite_list:
                        sprite_list.remove(sprite)
                        ID_index = sprite_ID_list[0::2].index(sprite.ID)
                        sprite_ID_list.pop(ID_index)
                        sprite_ID_list.pop(ID_index)
                        # After popping the sprite ID, the current sublevel number is in the sprite's ID index.

        # Enable the mouse click again when the user stopped clicking the mouse.
        elif not pygame.mouse.get_pressed()[0]:
            mouse_click_enabled = True

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                quit()

            manager.process_events(event)

        displaysurface.fill("0xAFDEEF")

        for entity in levels[current_sub_level].all_sprites:
            displaysurface.blit(entity.surf, entity.rect)

        for sprite in sprite_list:  # draw oulites for all selected sprites.
            draw_outline(sprite, "0xF5F97E")

        manager.update(delta_time)
        manager.draw_ui(displaysurface)
        pygame.display.update()
        clock.tick(240) / 1000

    disable_editor()

    command_configuration_menu.show()

    global available_commands
    available_commands = pygame_gui.elements.UIDropDownMenu(get_available_commands(sprite_list),
                                                            starting_option="",
                                                            relative_rect=pygame.Rect(
                                                                270, 60, 250, 40),
                                                            manager=manager,
                                                            container=command_configuration_menu,
                                                            object_id="#AVAILABLE_COMMANDS")

    while True:

        complementary_command_requirements = {"ACTIVATE_OBJECT": True,
                                              "DEACTIVATE_OBJECT": True}

        # Update the complementary command button to show up only if the command supports it.
        if available_commands.selected_option != "":
            complementary_command_text.visible = complementary_command_requirements[
                available_commands.selected_option]
            create_complementary_command.visible = complementary_command_requirements[
                available_commands.selected_option]

        if create_complementary_command.check_pressed():
            if create_complementary_command.text == "TRUE":
                create_complementary_command.set_text("FALSE")
            else:
                create_complementary_command.set_text("TRUE")

        if save_command.check_pressed() == True:
            load_command(selected_button, command_name_entry.get_text(), available_commands.selected_option, sprite_ID_list,
                         running_condition.selected_option, create_complementary_command)  # Add the commend to the selected button.

            if available_commands.selected_option == "ACTIVATE_OBJECT" or available_commands.selected_option == "DEACTIVATE_OBJECT":
                for sprite in sprite_list:
                    if running_condition.selected_option == "ACTIVE":
                        sprite.isActive = False

                    else:
                        sprite.isActive = True

            command_configuration_menu.hide()
            enable_editor()
            break

        elif close_command_configurator.check_pressed() == True:
            command_configuration_menu.hide()
            enable_editor()
            break

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                quit()

            manager.process_events(event)

        displaysurface.fill("0xAFDEEF")

        for entity in levels[current_sub_level].all_sprites:
            displaysurface.blit(entity.surf, entity.rect)

        manager.update(delta_time)
        manager.draw_ui(displaysurface)
        pygame.display.update()
        clock.tick(240) / 1000


def disable_editor():
    right_panel.disable()
    left_panel.disable()
    manager.draw_ui(displaysurface)

    levels[current_sub_level].creation_type = None


def enable_editor():
    right_panel.enable()
    left_panel.enable()
    manager.draw_ui(displaysurface)


def get_available_commands(sprite_list):
    command_requirements = {"ACTIVATE_OBJECT": [MovingPlatform],
                            "DEACTIVATE_OBJECT": [MovingPlatform]}

    valid_commands = []
    for command in command_requirements:
        valid_commands.append(command)

    for command, valid_sprites in command_requirements.items():
        for sprite in sprite_list:
            if not type(sprite) in valid_sprites:
                valid_commands.remove(command)
                break

    return valid_commands


def load_command(selected_button, command_name, command_type, sprite_ID_list, running_condition, create_complementary_command=False):

    if running_condition == "ACTIVE":
        for index, sprite_ID in enumerate(sprite_ID_list[0::2]):
            selected_button.activate_actions[command_name] = [
                command_type, sprite_ID_list[index + 1], sprite_ID]

            if create_complementary_command:
                if command_type == "ACTIVATE_OBJECT":
                    selected_button.deactivate_actions[command_name] = [
                        "DEACTIVATE_OBJECT", sprite_ID_list[index + 1], sprite_ID]

                elif command_type == "DEACTIVATE_OBJECT":
                    selected_button.deactivate_actions[command_name] = [
                        "ACTIVATE_OBJECT", sprite_ID_list[index + 1], sprite_ID]
    else:
        for index, sprite_ID in enumerate(sprite_ID_list[0::2]):
            selected_button.deactivate_actions[command_name] = [
                command_type, sprite_ID_list[index + 1], sprite_ID]

            if create_complementary_command:
                if command_type == "ACTIVATE_OBJECT":
                    selected_button.activate_actions[command_name] = [
                        "DEACTIVATE_OBJECT", sprite_ID_list[index + 1], sprite_ID]

                elif command_type == "DEACTIVATE_OBJECT":
                    selected_button.activate_actions[command_name] = [
                        "DEACTIVATE_OBJECT", sprite_ID_list[index + 1], sprite_ID]

    print(selected_button.activate_actions)


def main():
    pygame.init()
    ROOT_DIRECTORY = os.path.dirname(os.path.abspath(__file__))

    global displaysurface, levels, current_sub_level, manager, clock, delta_time
    clock = pygame.time.Clock()
    displaysurface = pygame.display.set_mode((1600, 1000))
    manager = pygame_gui.UIManager((1600, 1000), os.path.join(
        ROOT_DIRECTORY, "assets", "themes", "editor_theme.json"))

    initiate_UI(manager)

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

        for event in pygame.event.get():  # Update the editor based on the button's states.
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

                if event.ui_element == create_button_button:
                    levels[current_sub_level].creation_type = Button

                if event.ui_element == create_command and type(levels[current_sub_level].selected_sprite) == Button:
                    configure_command(
                        levels[current_sub_level].selected_sprite)

                if event.ui_element == delete_command and type(levels[current_sub_level].selected_sprite) == Button:
                    if commands_panel.selected_option in levels[current_sub_level].selected_sprite.activate_actions.keys():
                        levels[current_sub_level].selected_sprite.activate_actions.pop(
                            commands_panel.selected_option)

                    commands_panel.selected_option = ""

                if event.ui_element == change_button_mode:
                    if (change_button_mode.text == "BUTTON"):
                        change_button_mode.set_text("SWITCH")
                    elif (change_button_mode.text == "SWITCH"):
                        change_button_mode.set_text("BUTTON")

                if event.ui_element == change_button_state:
                    if (change_button_state.text == "ACTIVE"):
                        change_button_state.set_text("INACTIVE")
                    elif (change_button_state.text == "INACTIVE"):
                        change_button_state.set_text("ACTIVE")

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
                    break

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
                            if type(levels[current_sub_level].selected_sprite) == MovingPlatform:
                                if levels[current_sub_level].selected_sprite.end_pos[0] + int(event.text) >= 1300:
                                    error_text.set_text(
                                        "WIDTH GOES OUT OF BOUNDS!")
                                    continue
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
                            if type(levels[current_sub_level].selected_sprite) == MovingPlatform:
                                if levels[current_sub_level].selected_sprite.end_pos[1] + int(event.text) >= 1000:
                                    error_text.set_text(
                                        "HEIGHT GOES OUT OF BOUNDS!")
                                    continue
                            levels[current_sub_level].selected_sprite.surf = pygame.Surface(
                                (levels[current_sub_level].selected_sprite.rect.width, int(event.text)))
                            levels[current_sub_level].selected_sprite.rect.height = int(
                                event.text)
                            error_text.set_text("")
                        else:
                            error_text.set_text("HEIGHT GOES OUT OF BOUNDS!")
                if event.ui_element == pos_x2_text_entry:
                    if event.text:
                        if int(event.text) >= 0 and int(event.text) + levels[current_sub_level].selected_sprite.rect.width <= 1000:
                            levels[current_sub_level].selected_sprite.end_pos = int(
                                event.text) + 300, levels[current_sub_level].selected_sprite.end_pos[1]
                            error_text.set_text("")
                        else:
                            error_text.set_text("POS X2 IS OUT OF BOUNDS!")
                if event.ui_element == pos_y2_text_entry:
                    if event.text:
                        if int(event.text) >= 0 and int(event.text) + levels[current_sub_level].selected_sprite.rect.height <= 1000:
                            levels[current_sub_level].selected_sprite.end_pos = levels[current_sub_level].selected_sprite.end_pos[0], int(
                                event.text)
                            error_text.set_text("")
                        else:
                            error_text.set_text("POS Y2 IS OUT OF BOUNDS!")
                if event.ui_element == speed_text_entry:
                    if event.text:
                        if int(event.text) > 0 and int(event.text) <= 65536:
                            levels[current_sub_level].selected_sprite.speed = int(
                                event.text)
                            error_text.set_text("")
                        else:
                            error_text.set_text("SPEED IS INVALID!")

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

                                update_UI(
                                    levels[current_sub_level].selected_sprite)

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
                                                                                          60,
                                                                                          1,
                                                                                          1,
                                                                                          current_selected_color,
                                                                                          levels[current_sub_level].id_count,
                                                                                          0,
                                                                                          True)
                                levels[current_sub_level].original_draw_pos = (mouse_pos[0],
                                                                               mouse_pos[1])

                            if levels[current_sub_level].creation_type == Button:
                                levels[current_sub_level].current_sprite = Button(mouse_pos[0],
                                                                                  mouse_pos[1],
                                                                                  25,
                                                                                  75,
                                                                                  current_selected_color,
                                                                                  rgb_to_hex(calculate_complementary_color(
                                                                                      current_selected_color)),
                                                                                  {},
                                                                                  {},
                                                                                  "BUTTON",
                                                                                  levels[current_sub_level].id_count,
                                                                                  0,
                                                                                  isActive=False)

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

                        update_UI(levels[current_sub_level].current_sprite)

                # If we did create one, update the sprite
                elif (type(levels[current_sub_level].current_sprite) is not Player and type(levels[current_sub_level].current_sprite) is not Button):
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

        save_button.enable()
        clean_levels = [level for level in levels if level.all_sprites]

        # Enable the save button only if all of the sublevels contain a player.
        for sublevel in clean_levels:
            if not any(isinstance(x, Player) for x in sublevel.all_sprites):
                save_button.disable()

        # Checks an edge case if the clean_levels are empty
        if len(clean_levels) > 0:
            save_button.disable()

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
