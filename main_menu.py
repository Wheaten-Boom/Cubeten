import copy
import json
import os

import pygame
import pygame_gui
from pygame_gui import *
from pygame_gui.core import *

import level_loader
import settings


def main_menu():
    pygame.init()
    config = settings.get_settings()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode(
        (config["WIDTH"], config["HEIGHT"]))
    pygame.display.set_caption(config["TITLE"])

    manager = pygame_gui.UIManager((config["WIDTH"], config["HEIGHT"]),
                                   PackageResource("assets.themes", "main_menu.json"))

    level_select_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(250, 450, 500, 100),
                                                       manager=manager,
                                                       text="Level Select",
                                                       object_id="#level_select_button")

    settings_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(250, 600, 500, 100),
                                                   manager=manager,
                                                   text="Settings",
                                                   object_id="#settings_button")

    quit_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(250, 750, 500, 100),
                                               manager=manager,
                                               text="Quit",
                                               object_id="#quit_button")

    while True:
        delta_time = clock.tick(60) / 1000

        events = pygame.event.poll()

        if events.type == pygame.QUIT:
            pygame.quit()
            quit()
            return None, None

        if events.type == pygame_gui.UI_BUTTON_PRESSED:
            if "#level_select_button" in events.ui_object_id:
                level = level_select(screen)
                if level is None:
                    continue
                if level == "QUIT":
                    return None, None
                return level, screen

            if "#settings_button" in events.ui_object_id:
                settings_changed = settings_screen(screen)
                if settings_changed == "QUIT":
                    return None, None

                if settings_changed:
                    pygame.quit()
                    quit()
                    # do it again but with new settings
                    main_menu()
                    break

            if "#quit_button" in events.ui_object_id:
                return None, None

        screen.fill("0x57AFAF")

        manager.process_events(events)
        manager.update(delta_time)
        manager.draw_ui(screen)
        pygame.display.update()


def level_select(screen):
    pygame.init()
    config = settings.get_settings()
    clock = pygame.time.Clock()

    manager = pygame_gui.UIManager((config["WIDTH"], config["HEIGHT"]),
                                   PackageResource("assets.themes", "level_select.json"))

    button_panel = pygame_gui.elements.UIPanel(relative_rect=pygame.Rect(250, 100, 500, 500),
                                               manager=manager,
                                               starting_layer_height=0,
                                               object_id=ObjectID(class_id="@regular_button",
                                                                  object_id="#button_panel"))

    for x in range(3):
        for y in range(3):
            level_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(15 + (x * 160), 15 + (y * 160), 150, 150),
                                                        manager=manager,
                                                        container=button_panel,
                                                        text=str(x + (y * 3)
                                                                 + 1),
                                                        object_id=ObjectID(class_id="@level_button",
                                                                           object_id="#level_" + str(x + (y * 3) + 1) + "_button"))

    custom_level_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(225, 700, 550, 100),
                                                       manager=manager,
                                                       text="CUSTOM LEVEL",
                                                       object_id=ObjectID(class_id="@regular_button",
                                                                          object_id="#custom_level_button"))

    back_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(150, 850, 200, 100),
                                               manager=manager,
                                               text="BACK",
                                               object_id=ObjectID(class_id="@regular_button",
                                                                  object_id="#back_button"))

    while True:
        delta_time = clock.tick(60) / 1000

        events = pygame.event.poll()

        if events.type == pygame.QUIT:
            pygame.quit()
            quit()
            return "QUIT"

        if events.type == pygame_gui.UI_BUTTON_PRESSED:
            if "#level_1_button" in events.ui_object_id:
                return level_loader.Load("Demo")

            if "#level_2_button" in events.ui_object_id:
                return level_loader.Load("LEVEL_1")

            if "#custom_level_button" in events.ui_object_id:
                window = pygame_gui.windows.UIFileDialog(rect=pygame.Rect(200, 100, 600, 600),
                                                         manager=manager,
                                                         window_title="Choose a custom level",
                                                         initial_file_path=os.path.join(
                                                             os.path.dirname(__file__), "levels"),
                                                         object_id="#file_dialog_window")

            if "#back_button" in events.ui_object_id:
                return None

        if events.type == pygame_gui.UI_FILE_DIALOG_PATH_PICKED:
            path = events.text
            print(path)
            if path.endswith(".json"):
                return level_loader.Load(
                    path.split("/")[-1].removesuffix(".json")
                )
            else:
                print('What the fuck did you just fucking say about me, you little bitch? I’ll have you know I graduated top of my class in the Navy Seals, and I’ve been involved in numerous secret raids on Al-Quaeda, and I have over 300 confirmed kills.\nI am trained in gorilla warfare and I’m the top sniper in the entire US armed forces. You are nothing to me but just another target. I will wipe you the fuck out with precision the likes of which has never been seen before on this Earth, mark my fucking words.\nYou think you can get away with saying that shit to me over the Internet? Think again, fucker. As we speak I am contacting my secret network of spies across the USA and your IP is being traced right now so you better prepare for the storm, maggot. The storm that wipes out the pathetic little thing you call your life. You’re fucking dead, kid. I can be anywhere, anytime, and I can kill you in over seven hundred ways, and that’s just with my bare hands.\nNot only am I extensively trained in unarmed combat, but I have access to the entire arsenal of the United States Marine Corps and I will use it to its full extent to wipe your miserable ass off the face of the continent, you little shit. If only you could have known what unholy retribution your little “clever” comment was about to bring down upon you, maybe you would have held your fucking tongue.\nBut you couldn’t, you didn’t, and now you’re paying the price, you goddamn idiot. I will shit fury all over you and you will drown in it.\nYou’re fucking dead, kiddo.')

        screen.fill("0x57AFAF")

        manager.process_events(events)
        manager.draw_ui(screen)
        manager.update(delta_time)
        pygame.display.update()


def settings_screen(screen):
    pygame.init()
    clock = pygame.time.Clock()
    settings_changed = False
    config = settings.get_settings()
    temp_config = DynamicAccessNestedDict(copy.deepcopy(config))

    # This is used to get the "path" in the json to where the value we want to change is found, it's the ui_object_id to string path
    textentry_to_path = {
        "#general_panel.#screen_width_text_entry": ["WIDTH"],
        "#general_panel.#screen_height_text_entry": ["HEIGHT"],
        "#physics_panel.#game_gravity_text_entry": ["PHYSICS", "GRAVITY"],
        "#physics_panel.#game_acceleration_text_entry": ["PHYSICS", "ACCELERATION"],
        "#physics_panel.#game_jump_power_text_entry": ["PHYSICS", "JUMP_POWER"],
        "#physics_panel.#game_short_jump_power_text_entry": ["PHYSICS", "SHORT_JUMP_POWER"],
        "#physics_panel.#game_friction_text_entry": ["PHYSICS", "FRICTION"]
    }

    manager = pygame_gui.UIManager((config["WIDTH"], config["HEIGHT"]),
                                   PackageResource("assets.themes", "settings_screen.json"))
    # The textbox gives me an error if I don't do this, eh
    manager.add_font_paths("PixeloidSans",
                           PackageResource("assets.fonts", "PixeloidSans.ttf"))
    manager.preload_fonts([{"name": "PixeloidSans",
                            "point_size": 18,
                            "style": "regular"}])

    apply_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(675, 850, 300, 100),
                                                manager=manager,
                                                text="APPLY",
                                                object_id="#apply_button")

    default_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(350, 850, 300, 100),
                                                  manager=manager,
                                                  text="DEFAULT",
                                                  object_id="#default_button")

    back_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(25, 850, 300, 100),
                                               manager=manager,
                                               text="BACK",
                                               object_id="#back_button")

    general_tab_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(25, 100, 300, 75),
                                                      manager=manager,
                                                      text="GENERAL",
                                                      object_id=ObjectID(class_id="@tab_button",
                                                                         object_id="#general_tab_button"))

    physics_tab_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(350, 100, 300, 75),
                                                      manager=manager,
                                                      text="PHYSICS",
                                                      object_id=ObjectID(class_id="@tab_button",
                                                                         object_id="#physics_tab_button"))

    graphics_tab_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(675, 100, 300, 75),
                                                       manager=manager,
                                                       text="GRAPHICS",
                                                       object_id=ObjectID(class_id="@tab_button",
                                                                          object_id="#graphics_tab_button"))

    general_panel = pygame_gui.elements.UIPanel(relative_rect=pygame.Rect(25, 175, 950, 650),
                                                starting_layer_height=1,
                                                manager=manager,
                                                object_id="#general_panel")

    screen_width_text = pygame_gui.elements.UILabel(relative_rect=pygame.Rect(0, 25, 425, 100),
                                                    text="WIDTH:",
                                                    manager=manager,
                                                    container=general_panel,
                                                    object_id="#screen_width_text")

    screen_width_text_entry = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect(450, 25, 200, 100),
                                                                  manager=manager,
                                                                  container=general_panel,
                                                                  object_id="#screen_width_text_entry")
    screen_width_text_entry.set_text(str(temp_config.get_value(["WIDTH"])))
    screen_width_text_entry.set_allowed_characters("numbers")
    screen_width_text_entry.set_text_length_limit(6)

    screen_height_text = pygame_gui.elements.UILabel(relative_rect=pygame.Rect(0, 150, 425, 100),
                                                     text="HEIGHT:",
                                                     manager=manager,
                                                     container=general_panel,
                                                     object_id="#screen_height_text")

    screen_height_text_entry = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect(450, 150, 200, 100),
                                                                   manager=manager,
                                                                   container=general_panel,
                                                                   object_id="#screen_height_text_entry")
    screen_height_text_entry.set_text(str(temp_config.get_value(["HEIGHT"])))
    screen_height_text_entry.set_allowed_characters("numbers")
    screen_height_text_entry.set_text_length_limit(6)

    physics_panel = pygame_gui.elements.UIPanel(relative_rect=pygame.Rect(25, 175, 950, 650),
                                                starting_layer_height=1,
                                                manager=manager,
                                                object_id="#physics_panel")

    game_gravity_text = pygame_gui.elements.UILabel(relative_rect=pygame.Rect(0, 25, 425, 100),
                                                    text="GRAVITY:",
                                                    manager=manager,
                                                    container=physics_panel,
                                                    object_id="#game_gravity_text")

    game_gravity_text_entry = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect(450, 25, 200, 100),
                                                                  manager=manager,
                                                                  container=physics_panel,
                                                                  object_id="#game_gravity_text_entry")
    game_gravity_text_entry.set_text(
        str(temp_config.get_value(["PHYSICS", "GRAVITY"])))
    game_gravity_text_entry.set_allowed_characters(
        ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", ".", "-"])
    game_gravity_text_entry.set_text_length_limit(6)

    game_acceleration_text = pygame_gui.elements.UILabel(relative_rect=pygame.Rect(0, 150, 425, 100),
                                                         text="ACCELERATION:",
                                                         manager=manager,
                                                         container=physics_panel,
                                                         object_id="#game_acceleration_text")

    game_acceleration_text_entry = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect(450, 150, 200, 100),
                                                                       manager=manager,
                                                                       container=physics_panel,
                                                                       object_id="#game_acceleration_text_entry")
    game_acceleration_text_entry.set_text(
        str(temp_config.get_value(["PHYSICS", "ACCELERATION"])))
    game_acceleration_text_entry.set_allowed_characters(
        ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", ".", "-"])
    game_acceleration_text_entry.set_text_length_limit(6)

    game_jump_power_text = pygame_gui.elements.UILabel(relative_rect=pygame.Rect(0, 275, 425, 100),
                                                       text="JUMP:",
                                                       manager=manager,
                                                       container=physics_panel,
                                                       object_id="#game_jump_power_text")

    game_jump_power_text_entry = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect(450, 275, 200, 100),
                                                                     manager=manager,
                                                                     container=physics_panel,
                                                                     object_id="#game_jump_power_text_entry")
    game_jump_power_text_entry.set_text(
        str(temp_config.get_value(["PHYSICS", "JUMP_POWER"])))
    game_jump_power_text_entry.set_allowed_characters(
        ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", ".", "-"])
    game_jump_power_text_entry.set_text_length_limit(6)

    game_short_jump_power_text = pygame_gui.elements.UILabel(relative_rect=pygame.Rect(0, 400, 425, 100),
                                                             text="SHORT JUMP:",
                                                             manager=manager,
                                                             container=physics_panel,
                                                             object_id="#game_short_jump_power_text")

    game_short_jump_power_text_entry = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect(450, 400, 200, 100),
                                                                           manager=manager,
                                                                           container=physics_panel,
                                                                           object_id="#game_short_jump_power_text_entry")
    game_short_jump_power_text_entry.set_text(
        str(temp_config.get_value(["PHYSICS", "SHORT_JUMP_POWER"])))
    game_short_jump_power_text_entry.set_allowed_characters(
        ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", ".", "-"])
    game_short_jump_power_text_entry.set_text_length_limit(6)

    game_friction_text = pygame_gui.elements.UILabel(relative_rect=pygame.Rect(0, 525, 425, 100),
                                                     text="FRICTION:",
                                                     manager=manager,
                                                     container=physics_panel,
                                                     object_id="#game_friction_text")

    game_friction_text_entry = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect(450, 525, 200, 100),
                                                                   manager=manager,
                                                                   container=physics_panel,
                                                                   object_id="#game_friction_text_entry")
    game_friction_text_entry.set_text(
        str(temp_config.get_value(["PHYSICS", "FRICTION"])))
    game_friction_text_entry.set_allowed_characters(
        ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", ".", "-"])
    game_friction_text_entry.set_text_length_limit(6)

    physics_panel.hide()

    graphics_panel = pygame_gui.elements.UIPanel(relative_rect=pygame.Rect(25, 175, 950, 650),
                                                 starting_layer_height=1,
                                                 manager=manager,
                                                 object_id="#graphics_panel")

    graphics_coming_soon_text = pygame_gui.elements.UILabel(relative_rect=pygame.Rect(225, 275, 425, 100),
                                                            text="COMING NEVER",
                                                            manager=manager,
                                                            container=graphics_panel,
                                                            object_id="#graphics_coming_soon_text")

    graphics_panel.hide()

    while True:
        delta_time = clock.tick(60) / 1000

        settings_changed = (config != temp_config.copy())

        events = pygame.event.poll()

        if events.type == pygame.QUIT:
            pygame.quit()
            quit()
            return "QUIT"

        if events.type == pygame_gui.UI_BUTTON_PRESSED:
            if "#apply_button" in events.ui_object_id:
                config = copy.deepcopy(temp_config.copy())
                settings.set_settings(config)
                with open("settings.json", "w") as config_file:
                    temp = json.dumps(config, indent=4)
                    config_file.write(temp)

            if "#default_button" in events.ui_object_id:
                temp_config.set_dict(copy.deepcopy(config))
                settings_changed = False
                for text_entry in [text_entry for text_entry in manager.get_sprite_group() if type(text_entry) is pygame_gui.elements.UITextEntryLine]:
                    text_entry.set_text(
                        str(temp_config.get_value(textentry_to_path[text_entry.most_specific_combined_id])))

            if "#back_button" in events.ui_object_id:
                if settings_changed:
                    # open a confirmation dialog to see if the user wants to continue without saving changes
                    confirmation_dialog = pygame_gui.windows.UIConfirmationDialog(rect=pygame.Rect(350, 400, 300, 200),
                                                                                  manager=manager,
                                                                                  action_long_desc="<font face='PixeloidSans' color='#ffffff' size=5>"
                                                                                  + "You have unsaved changes.<br>Do you wish to continue?</font>",
                                                                                  blocking=False)
                else:
                    return settings_changed

            if "#general_tab_button" in events.ui_object_id:
                general_panel.show()
                physics_panel.hide()
                graphics_panel.hide()

            if "#physics_tab_button" in events.ui_object_id:
                general_panel.hide()
                physics_panel.show()
                graphics_panel.hide()

            if "#graphics_tab_button" in events.ui_object_id:
                general_panel.hide()
                physics_panel.hide()
                graphics_panel.show()

        if events.type == pygame_gui.UI_TEXT_ENTRY_CHANGED:
            if events.text == "":
                temp_config.set_value(textentry_to_path[events.ui_object_id],
                                      0)
            else:
                try:
                    if "." in events.text:
                        temp_config.set_value(textentry_to_path[events.ui_object_id],
                                              float(events.text))
                    else:
                        temp_config.set_value(textentry_to_path[events.ui_object_id],
                                              int(events.text))
                except ValueError:
                    pass

        if events.type == pygame_gui.UI_CONFIRMATION_DIALOG_CONFIRMED:
            if "#confirmation_dialog" in events.ui_object_id:
                return False

        screen.fill("0x57AFAF")

        manager.process_events(events)
        manager.draw_ui(screen)
        manager.update(delta_time)
        pygame.display.update()


class DynamicAccessNestedDict:
    # Blatantly copied from https://stackoverflow.com/a/56930261, thank you
    """
    A class used to wrap a dict in order to dynamically get/set nested dictionary keys of "data" dict
    """

    def __init__(self, data: dict):
        self.data = data

    def get_value(self, keys) -> any:
        """
        Returns the value at the end of the list of keys, the format of the keys is ("a", "b", "c", etc...)

        :param - keys: a list of string keys
        """
        data = self.data

        for k in keys:
            data = data[k]
        return data

    def set_value(self, keys, val) -> None:
        """
        Sets the value at the end of the list of keys, the format of the keys is ("a", "b", "c", etc...)

        :param - keys: a list of string keys
        :param - val: the new value
        """
        data = self.data
        lastkey = keys[-1]
        for k in keys[:-1]:  # when assigning drill down to *second* last key
            data = data[k]
        data[lastkey] = val
        return None

    def set_dict(self, data: dict):
        self.data = data

    def copy(self):
        return self.data
