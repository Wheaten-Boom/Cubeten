import json
import pygame
from pygame import *
import pygame_gui
from pygame_gui import *
from pygame_gui.core import *
import settings
from settings import config
import level_loader


def main_menu():
    pygame.init()
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
    clock = pygame.time.Clock()

    manager = pygame_gui.UIManager((config["WIDTH"], config["HEIGHT"]),
                                   PackageResource("assets.themes", "level_select.json"))

    button_panel = pygame_gui.elements.UIPanel(relative_rect=pygame.Rect(250, 100, 500, 500),
                                               manager=manager,
                                               starting_layer_height=0,
                                               object_id="#button_panel")

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
                                                       object_id="#custom_level_button")

    back_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(150, 850, 200, 100),
                                               manager=manager,
                                               text="BACK",
                                               object_id="#back_button")

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

            if "#back_button" in events.ui_object_id:
                return None

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
    temp_config = config.copy()

    # This is used to get the "path" in the json to where the value we want to change is found, it's the ui_object_id to string path
    textentry_to_text = {
        "general_panel.#screen_width_text_entry": "WIDTH",
        "general_panel.#screen_height_text_entry": "HEIGHT"
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

    screen_width_text = pygame_gui.elements.UILabel(relative_rect=pygame.Rect(0, 25, 250, 100),
                                                    text="*WIDTH:",
                                                    manager=manager,
                                                    container=general_panel,
                                                    object_id="#screen_width_text")

    screen_width_text_entry = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect(275, 25, 200, 100),
                                                                  manager=manager,
                                                                  container=general_panel,
                                                                  object_id="#screen_width_text_entry")
    screen_width_text_entry.set_text(str(temp_config["WIDTH"]))
    screen_width_text_entry.set_allowed_characters("numbers")
    screen_width_text_entry.set_text_length_limit(4)

    screen_height_text = pygame_gui.elements.UILabel(relative_rect=pygame.Rect(0, 150, 250, 100),
                                                     text="*HEIGHT:",
                                                     manager=manager,
                                                     container=general_panel,
                                                     object_id="#screen_height_text")

    screen_height_text_entry = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect(275, 150, 200, 100),
                                                                   manager=manager,
                                                                   container=general_panel,
                                                                   object_id="#screen_height_text_entry")
    screen_height_text_entry.set_text(str(temp_config["HEIGHT"]))
    screen_height_text_entry.set_allowed_characters("numbers")
    screen_height_text_entry.set_text_length_limit(4)

    physics_panel = pygame_gui.elements.UIPanel(relative_rect=pygame.Rect(25, 175, 950, 650),
                                                starting_layer_height=1,
                                                manager=manager,
                                                object_id="#physics_panel")

    graphics_panel = pygame_gui.elements.UIPanel(relative_rect=pygame.Rect(25, 175, 950, 650),
                                                 starting_layer_height=1,
                                                 manager=manager,
                                                 object_id="#graphics_panel")

    while True:
        delta_time = clock.tick(60) / 1000

        settings_changed = (config != temp_config)

        events = pygame.event.poll()

        if events.type == pygame.QUIT:
            pygame.quit()
            quit()
            return "QUIT"

        if events.type == pygame_gui.UI_BUTTON_PRESSED:
            if "#apply_button" in events.ui_object_id:
                config = temp_config.copy()
                settings.set_settings(config)
                with open("settings.json", "w") as config_file:
                    temp = json.dumps(config, indent=4)
                    config_file.write(temp)

            if "#default_button" in events.ui_object_id:
                temp_config = config.copy()
                settings_changed = False
                screen_width_text_entry.set_text(str(temp_config["WIDTH"]))
                screen_height_text_entry.set_text(str(temp_config["HEIGHT"]))

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

        if events.type == pygame_gui.UI_TEXT_ENTRY_CHANGED:
            temp_config[textentry_to_text[events.ui_object_id[1:]]] = int(
                events.text)

        if events.type == pygame_gui.UI_CONFIRMATION_DIALOG_CONFIRMED:
            if "#confirmation_dialog" in events.ui_object_id:
                return False

        screen.fill("0x57AFAF")

        manager.process_events(events)
        manager.draw_ui(screen)
        manager.update(delta_time)
        pygame.display.update()
