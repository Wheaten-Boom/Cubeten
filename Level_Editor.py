from doctest import FAIL_FAST
from platform import platform
import py
import pygame
from pygame.locals import *
from objects import *


def update_sprite(mouse_x, mouse_y, sprite):
    sprite.surf = pygame.Surface((abs(mouse_x - sprite.pos.x), abs(mouse_y - sprite.pos.y)))

    if (mouse_x - sprite.rect.topleft[0] < 0):
        sprite.rect.bottomleft = pygame.mouse.get_pos()

    if (mouse_x - sprite.rect.topleft[0] >= 0):
        sprite.rect.bottomright = (((sprite.rect.topright[0]) + (mouse_x - sprite.rect.topleft[0])), mouse_y - sprite.pos.y)

    # if (sprite.pos.y - mouse_y < 0):
    #     sprite.pos.y -= 1
    #     sprite.rect.midbottom = sprite.pos

    sprite.surf.fill(sprite.color)

def main():

    pygame.init()
    FramePerSec = pygame.time.Clock()

    displaysurface = pygame.display.set_mode((1000, 1000))
    all_sprits = pygame.sprite.Group()
    recent_sprites = []
    create_new_sprite = True

    while True:

        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_ESCAPE]:
            pygame.quit()
            quit()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                quit()

       
        if pygame.mouse.get_pressed(num_buttons=3)[0] == True:    

            if create_new_sprite == True:

                new_sprite = Platform(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], 0, 0, (255,255,255), 2, 1)
                all_sprits.add(new_sprite)
                recent_sprites.append(new_sprite)
                create_new_sprite =  False

            else:
                update_sprite(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], recent_sprites[-1])

        else:
            create_new_sprite = True


        displaysurface.fill((0, 0, 0))
        for entity in all_sprits:
            displaysurface.blit(entity.surf, entity.rect)

        pygame.display.update()
        FramePerSec.tick(60)


if __name__ == "__main__":
    main()

