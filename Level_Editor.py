import os
import json
import pygame
from pygame.locals import *
import pygame_gui
from pygame_gui import *
from objects import *


def Create_Level_File(data, filename):
    with open(os.path.join(os.path.dirname(__file__), "levels", filename), "w") as file:
        json.dump(data, file, indent=4)


def Data_Assembler(all_sprites):
    data = {"SUB_LEVELS": ["SUBLEVEL_0"], "SUBLEVEL_0": {"PLATFORMS": [], "PLAYER": {}}}
    for sprite in all_sprites:
        if type(sprite) == Platform:
            new_platform = {"POS_X": int(sprite.rect.left) - 300,
                            "POS_Y": int(sprite.rect.top),
                            "WIDTH": int(sprite.rect.width),
                            "HEIGHT": int(sprite.rect.height),
                            "COLOR": sprite.color,
                            "ID": sprite.ID,
                            "DRAW_LAYER": sprite.draw_layer}

            data["SUBLEVEL_0"]["PLATFORMS"].append(new_platform)

        if type(sprite) == Player:
            new_player = {"POS_X": int(sprite.rect.left) - 300,
                            "POS_Y": int(sprite.rect.top),
                            "WIDTH": int(sprite.rect.width),
                            "HEIGHT": int(sprite.rect.height),
                            "COLOR": sprite.color,
                            "ID": sprite.ID,
                            "DRAW_LAYER": sprite.draw_layer}

            data["SUBLEVEL_0"]["PLAYER"] = (new_player)

            

    return data


def is_mouse_on_sprite(sprite_list, mouse_pos):
    for sprite in sprite_list:
        if sprite.rect.collidepoint(mouse_pos):
            return True
    return False


def draw_outline(sprite, displaysurface):
    outline_rect = sprite.rect.copy()
    outline_rect.inflate_ip((outline_rect.width + outline_rect.height) / 25,
                            (outline_rect.width + outline_rect.height) / 25)
    pygame.draw.rect(displaysurface, "0xF5F97E", outline_rect, 0)


def main():
    pygame.init()
    clock = pygame.time.Clock()

    displaysurface = pygame.display.set_mode((1600, 1000))
    manager = pygame_gui.UIManager((1600, 1000), PackageResource(
        "assets.themes", "editor_theme.json"))

    left_panel = pygame_gui.elements.UIPanel(relative_rect=pygame.Rect(0, 0, 300, 1000),
                                             starting_layer_height=0,
                                             manager=manager)

    create_platform_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(50, 40, 200, 50),
                                                          text="PLAT",
                                                          manager=manager,
                                                          container=left_panel,
                                                          object_id="#PLATFORM_BUTTON")

    create_moving_platform_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(50, 120, 200, 50),
                                                                 text="MOV PLAT",
                                                                 manager=manager,
                                                                 container=left_panel,
                                                                 object_id="#MOVING_PLATFORM_BUTTON")

    create_player_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(50, 200, 200, 50),
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

    pos_x_text = pygame_gui.elements.UILabel(relative_rect=pygame.Rect(15, 200, -1, -1),
                                             text="X:",
                                             manager=manager,
                                             container=right_panel,
                                             object_id="#POS_X_TEXT")

    pos_x_text_entry = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect(40, 200, 75, 50),
                                                           manager=manager,
                                                           container=right_panel,
                                                           object_id="#POS_X_TEXT_ENTRY")
    pos_x_text_entry.set_allowed_characters("numbers")
    pos_x_text_entry.set_text_length_limit(4)

    pos_y_text = pygame_gui.elements.UILabel(relative_rect=pygame.Rect(15, 250, -1, -1),
                                             text="Y:",
                                             manager=manager,
                                             container=right_panel,
                                             object_id="#POS_Y_TEXT")

    pos_y_text_entry = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect(40, 250, 75, 50),
                                                           manager=manager,
                                                           container=right_panel,
                                                           object_id="#POS_Y_TEXT_ENTRY")
    pos_y_text_entry.set_allowed_characters("numbers")
    pos_y_text_entry.set_text_length_limit(4)

    width_text = pygame_gui.elements.UILabel(relative_rect=pygame.Rect(145, 200, -1, -1),
                                             text="W:",
                                             manager=manager,
                                             container=right_panel,
                                             object_id="#WIDTH_TEXT")

    width_text_entry = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect(175, 200, 75, 50),
                                                           manager=manager,
                                                           container=right_panel,
                                                           object_id="#WIDTH_TEXT_ENTRY")
    width_text_entry.set_allowed_characters("numbers")
    width_text_entry.set_text_length_limit(4)

    height_text = pygame_gui.elements.UILabel(relative_rect=pygame.Rect(150, 250, -1, -1),
                                              text="H:",
                                              manager=manager,
                                              container=right_panel,
                                              object_id="#HEIGHT_TEXT")

    height_text_entry = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect(175, 250, 75, 50),
                                                            manager=manager,
                                                            container=right_panel,
                                                            object_id="#HEIGHT_TEXT_ENTRY")
    height_text_entry.set_allowed_characters("numbers")
    height_text_entry.set_text_length_limit(4)

    input_out_of_bounds = pygame_gui.elements.UILabel(relative_rect=pygame.Rect(15, 310, -1, -1),
                                                      text="",
                                                      manager=manager,
                                                      container=right_panel,
                                                      visible=True,
                                                      object_id="#INPUT_OUT_OF_BOUNDS")

    all_sprites = pygame.sprite.Group()
    id_count = 0
    current_sprite = None
    original_draw_pos = None
    creating_sprite = False
    selected_sprite = None
    creation_type = None

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
                if event.ui_element == create_platform_button:
                    creation_type = Platform
                if event.ui_element == create_moving_platform_button:
                    creation_type = MovingPlatform
                if event.ui_element == create_player_button:
                    creation_type = Player
                if event.ui_element == clear_button:
                    all_sprites.empty()
                    id_count = 0
                    current_sprite = None
                    original_draw_pos = None
                    creating_sprite = False
                    selected_sprite = None
                    create_player_button.enable()

                if event.ui_element == save_button:
                    data = Data_Assembler(all_sprites)
                    Create_Level_File(data, "TEST.json")
                    
                if event.ui_element == delete_button:
                    if selected_sprite is not None:
                        all_sprites.remove(selected_sprite)
                        if (type(selected_sprite) == Player):
                            create_player_button.enable()
                        selected_sprite = None

            if event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED:
                if event.ui_element == pos_x_text_entry:
                    if event.text:
                        if int(event.text) >= 0 and int(event.text) + selected_sprite.rect.width <= 1000:
                            selected_sprite.rect.left = int(event.text) + 300
                            input_out_of_bounds.set_text("")
                        else:
                            input_out_of_bounds.set_text(
                                "POS X IS OUT OF BOUNDS!")
                if event.ui_element == pos_y_text_entry:
                    if event.text:
                        if int(event.text) >= 0 and int(event.text) + selected_sprite.rect.height <= 1000:
                            selected_sprite.rect.top = int(event.text)
                            input_out_of_bounds.set_text("")
                        else:
                            input_out_of_bounds.set_text(
                                "POS Y IS OUT OF BOUNDS!")
                if event.ui_element == width_text_entry:
                    if event.text:
                        if int(event.text) > 0 and int(event.text) + selected_sprite.rect.left <= 1300:
                            selected_sprite.surf = pygame.Surface(
                                (int(event.text), selected_sprite.rect.height))
                            selected_sprite.rect.width = int(event.text)
                            input_out_of_bounds.set_text("")
                        else:
                            input_out_of_bounds.set_text(
                                "WIDTH GOES OUT OF BOUNDS!")
                if event.ui_element == height_text_entry:
                    if event.text:
                        if int(event.text) > 0 and int(event.text) + selected_sprite.rect.top <= 1000:
                            selected_sprite.surf = pygame.Surface(
                                (selected_sprite.rect.width, int(event.text)))
                            selected_sprite.rect.height = int(event.text)
                            input_out_of_bounds.set_text("")
                        else:
                            input_out_of_bounds.set_text(
                                "HEIGHT GOES OUT OF BOUNDS!")

            manager.process_events(event)

        # Check whether the mouse left click is pressed
        if pygame.mouse.get_pressed()[0]:
            mouse_pos = pygame.mouse.get_pos()
            # Check if the mouse is on the drawing area
            if mouse_pos[0] > 300 and mouse_pos[0] < 1300 and mouse_pos[1] > 0 and mouse_pos[1] < 1000:
                # If we didn't already create a sprite, create one
                if not creating_sprite:
                    # If the mouse is on a sprite, select that sprite
                    if is_mouse_on_sprite(all_sprites, mouse_pos):
                        for sprite in all_sprites:
                            if sprite.rect.collidepoint(mouse_pos):
                                if sprite is selected_sprite:
                                    break

                                selected_sprite = sprite
                                creation_type = type(selected_sprite)
                                red_slider.set_current_value(sprite.color[0])
                                green_slider.set_current_value(sprite.color[1])
                                blue_slider.set_current_value(sprite.color[2])
                                pos_x_text_entry.set_text(str(
                                    selected_sprite.rect.left - 300))
                                pos_y_text_entry.set_text(str(
                                    selected_sprite.rect.top))
                                width_text_entry.set_text(str(
                                    selected_sprite.rect.width))
                                height_text_entry.set_text(str(
                                    selected_sprite.rect.height))

                    else:
                        if creation_type is not None and selected_sprite is None:
                            creating_sprite = True
                            selected_sprite = None

                            if creation_type == Platform:
                                current_sprite = Platform(mouse_pos[0],
                                                          mouse_pos[1],
                                                          1, 1,
                                                          current_selected_color,
                                                          id_count,
                                                          0)
                                original_draw_pos = (
                                    mouse_pos[0], mouse_pos[1])

                            if creation_type == Player:
                                current_sprite = Player(mouse_pos[0],
                                                        mouse_pos[1],
                                                        75, 75,
                                                        current_selected_color,
                                                        id_count,
                                                        0)

                                current_sprite.surf = pygame.Surface((current_sprite.rect.width,
                                                                      current_sprite.rect.height))
                                current_sprite.surf.fill(current_sprite.color)

                                create_player_button.disable()
                                creation_type = None

                # If we did create one, update the sprite
                elif (type(current_sprite) is not Player):
                    current_sprite.rect.left = min(original_draw_pos[0],
                                                   mouse_pos[0])
                    current_sprite.rect.top = min(original_draw_pos[1],
                                                  mouse_pos[1])
                    current_sprite.rect.width = abs(mouse_pos[0]
                                                    - original_draw_pos[0])
                    current_sprite.rect.height = abs(mouse_pos[1]
                                                     - original_draw_pos[1])

                    current_sprite.surf = pygame.Surface((current_sprite.rect.width,
                                                          current_sprite.rect.height))
                    current_sprite.surf.fill(current_sprite.color)

        # If the mouse left click is not pressed, stop creating a sprite and add it to the sprite group
        elif creating_sprite:
            creating_sprite = False
            all_sprites.add(current_sprite)
            selected_sprite = current_sprite
            pos_x_text_entry.set_text(str(selected_sprite.rect.left - 300))
            pos_y_text_entry.set_text(str(selected_sprite.rect.top))
            width_text_entry.set_text(str(selected_sprite.rect.width))
            height_text_entry.set_text(str(selected_sprite.rect.height))
            current_sprite = None
            original_draw_pos = None
            id_count += 1

        # Clears the selection if right click is pressed
        if pygame.mouse.get_pressed()[2]:
            selected_sprite = None
            input_out_of_bounds.set_text("")

        manager.update(delta_time)

        displaysurface.fill("0xAFDEEF")

        current_selected_color = (red_slider.get_current_value(),
                                  green_slider.get_current_value(),
                                  blue_slider.get_current_value())

        # If we do have a sprite selected, draw an outline around it
        if selected_sprite is not None:
            selected_sprite.color = current_selected_color
            selected_sprite.surf.fill(selected_sprite.color)

            if (pygame.mouse.get_pressed()[0]
                    and selected_sprite.rect.collidepoint(pygame.mouse.get_pos())):
                # Adds pygame.mouse.get_rel() to the sprite's position (drags it)
                new_pos = tuple(map(lambda i, j: i + j,
                                    selected_sprite.rect.topleft,
                                    pygame.mouse.get_rel()))
                # If the sprite didn't move we don't want to update the position, this is to allow us to type new values in the text entry boxes
                if selected_sprite.rect.topleft != new_pos:
                    # Checks we aren't dragging it outside of the screen
                    if new_pos[0] >= 300 and new_pos[0] + selected_sprite.rect.width <= 1300:
                        selected_sprite.rect.left = new_pos[0]
                    if new_pos[1] >= 0 and new_pos[1] + selected_sprite.rect.height <= 1000:
                        selected_sprite.rect.top = new_pos[1]
                    # Updates the text box with the sprite's position
                    pos_x_text_entry.set_text(str(
                        selected_sprite.rect.left - 300))
                    pos_y_text_entry.set_text(str(
                        selected_sprite.rect.top))
                    width_text_entry.set_text(str(
                        selected_sprite.rect.width))
                    height_text_entry.set_text(str(
                        selected_sprite.rect.height))

            draw_outline(selected_sprite, displaysurface)
        # If we don't have a sprite selected, clear the text box
        else:
            pos_x_text_entry.set_text("")
            pos_y_text_entry.set_text("")
            width_text_entry.set_text("")
            height_text_entry.set_text("")

        # If we are creating a sprite, draw it
        if current_sprite is not None:
            displaysurface.blit(current_sprite.surf, current_sprite.rect)

        # Draw all the sprites
        for entity in all_sprites:
            displaysurface.blit(entity.surf, entity.rect)

        manager.draw_ui(displaysurface)

        pygame.draw.rect(displaysurface, current_selected_color,
                         (1345, 157, 245, 27))

        pygame.mouse.get_rel()

        pygame.display.update()


if __name__ == "__main__":
    main()
