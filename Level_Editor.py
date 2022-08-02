import os
import json
from select import select
import pygame
from pygame.locals import *
import pygame_gui
from objects import *


def Create_Level_File(data, filename):
    with open(os.path.join(os.path.dirname(__file__), "levels", filename), "w") as file:
        json.dump(data, file, indent=4)


def Data_Assembler(all_sprites):
    data = {"SUB_LEVELS": ["SUBLEVEL_0"], "SUBLEVEL_0": {"PLATFORMS": []}}
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
    manager = pygame_gui.UIManager((1600, 1000))

    left_panel = pygame_gui.elements.UIPanel(relative_rect=pygame.Rect(0, 0, 300, 1000),
                                             starting_layer_height=0,
                                             manager=manager)

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

    Red_Slider = pygame_gui.elements.UIHorizontalSlider(relative_rect=pygame.Rect(40, 25, 250, 30),
                                                        start_value=0,
                                                        value_range=(0,255),
                                                        manager=manager,
                                                        container=right_panel,
                                                        object_id="#RED_COLOR_SLIDER")

    Green_Slider = pygame_gui.elements.UIHorizontalSlider(relative_rect=pygame.Rect(40, 70, 250, 30),
                                                        start_value=0,
                                                        value_range=(0,255),
                                                        manager=manager,
                                                        container=right_panel,
                                                        object_id="#GREEN_COLOR_SLIDER")   

    Blue_Slider = pygame_gui.elements.UIHorizontalSlider(relative_rect=pygame.Rect(40, 115, 250, 30),
                                                        start_value=0,
                                                        value_range=(0,255),
                                                        manager=manager,
                                                        container=right_panel,
                                                        object_id="#BLUE_COLOR_SLIDER")

    

                                                                                        

    all_sprites = pygame.sprite.Group()
    id_count = 0
    current_sprite = None
    original_draw_pos = None
    creating_sprite = False
    selected_sprite = None

    while True:
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_ESCAPE]:
            pygame.quit()
            quit()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                quit()

            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == clear_button:
                    all_sprites.empty()
                    id_count = 0
                    current_sprite = None
                    original_draw_pos = None
                    creating_sprite = False
                    selected_sprite = None
                if event.ui_element == save_button:
                    data = Data_Assembler(all_sprites)
                    Create_Level_File(data, "TEST.json")

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

                                selected_sprite = sprite
                                break
                    else:
                        creating_sprite = True
                        selected_sprite = None
                        current_sprite = Platform(
                            mouse_pos[0], mouse_pos[1], 1, 1, Current_Selected_Color, id_count, 0)
                        original_draw_pos = (mouse_pos[0], mouse_pos[1])
                # If we did create one, update the sprite
                else:
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
            current_sprite = None
            original_draw_pos = None
            id_count += 1

        manager.process_events(event)
        manager.update(clock.get_time())

        displaysurface.fill("0xAFDEEF")

        # If we do have a sprite selected, draw an outline around it
        if selected_sprite is not None:
            draw_outline(selected_sprite, displaysurface)
            if pygame.mouse.get_pressed()[0] and selected_sprite.rect.collidepoint(pygame.mouse.get_pos()):
                selected_sprite.rect.center = pygame.mouse.get_pos()

        # If we are creating a sprite, draw it
        if current_sprite is not None:
            displaysurface.blit(current_sprite.surf, current_sprite.rect)

        # Draw all the sprites
        for entity in all_sprites:
            displaysurface.blit(entity.surf, entity.rect)

        manager.draw_ui(displaysurface)

        Current_Selected_Color = (Red_Slider.get_current_value(), Green_Slider.get_current_value(), Blue_Slider.get_current_value())

        pygame.draw.rect(displaysurface, Current_Selected_Color, pygame.Rect(1345, 160, 125, 22))

        pygame.display.update()
        clock.tick(240)


if __name__ == "__main__":
    main()
