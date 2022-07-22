import math
import pygame
from pygame.locals import *
from main import *

config = load_configuration()


class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, color, ID, draw_layer):
        super().__init__()
        self.surf = pygame.Surface((width, height))
        self.surf.fill(color)
        self.color = color
        self.rect = self.surf.get_rect()
        self.pos = pygame.math.Vector2(x, y)
        self.ID = ID
        self.draw_layer = draw_layer
        self.rect.midbottom = self.pos


class MovingPlatform(pygame.sprite.Sprite):
    def __init__(self, x1, y1, x2, y2, speed, width, height, color, ID, draw_layer, isActive=True):
        super().__init__()
        self.surf = pygame.Surface((width, height))
        self.surf.fill(color)
        self.rect = self.surf.get_rect()
        self.start_pos = pygame.math.Vector2(min(x1, x2), min(y1, y2))
        self.end_pos = pygame.math.Vector2(max(x1, x2), max(y1, y2))
        self.pos = pygame.math.Vector2(x1, y1)
        self.rect.midbottom = self.pos
        self.speed = speed
        self.direction = 1
        self.isActive = isActive
        self.ID = ID
        self.draw_layer = draw_layer

    def update(self, collision_group):
        if self.isActive:
            self.pos.x += self.direction * \
                abs(self.end_pos.x - self.start_pos.x) / self.speed
            self.pos.y += self.direction * \
                abs(self.end_pos.y - self.start_pos.y) / self.speed

            # move all entities on the platform along with it
            collides = pygame.sprite.spritecollide(
                self, collision_group, False)
            for entity in collides:
                if entity.rect.bottom == self.rect.top + 1:
                    entity.pos.x += self.direction * \
                        abs(self.end_pos.x - self.start_pos.x) / self.speed
                    entity.pos.y += self.direction * \
                        abs(self.end_pos.y - self.start_pos.y) / self.speed
                    entity.rect.midbottom = entity.pos

            if self.direction == 1:
                if self.pos.x >= self.end_pos.x and self.pos.y >= self.end_pos.y:
                    self.direction = -1
            else:
                if self.pos.x <= self.start_pos.x and self.pos.y <= self.start_pos.y:
                    self.direction = 1
            self.rect.midbottom = self.pos


class Button(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, color, activate_color, activate_actions, deactivate_actions, mode, ID, draw_layer, isActive=False):
        super().__init__()
        self.surf = pygame.Surface((width, height))
        self.surf.fill(color)
        self.rect = self.surf.get_rect()
        self.color = color
        self.activate_color = activate_color
        self.pos = pygame.math.Vector2(x, y)
        self.isActive = isActive
        self.activate_actions = activate_actions
        self.deactivate_actions = deactivate_actions
        self.mode = mode
        self.ID = ID
        self.draw_layer = draw_layer
        self.rect.midbottom = self.pos

    def update(self, collision_group, level, player):
        if self.mode == "BUTTON":
            if not self.isActive:
                collides = pygame.sprite.spritecollide(
                    self, collision_group, False)
                for entity in collides:
                    if entity.rect.bottom == self.rect.top + 1:
                        self.isActive = True
                        self.surf.fill(self.activate_color)
                        self.activate_button(level)
                        break
            else:
                collides = pygame.sprite.spritecollide(
                    self, collision_group, False)
                if not collides:
                    self.isActive = False
                    self.surf.fill(self.color)
                    self.deactivate_button(level)

        elif self.mode == "SWITCH":
            if not self.isActive:
                if (self.pos.x - player.rect.width < player.pos.x and player.pos.x < self.pos.x + player.rect.width
                        and player.pos.y >= self.pos.y and player.pos.y < self.pos.y + player.rect.height):
                    self.isActive = True
                    self.surf.fill(self.activate_color)
                    self.activate_button(level)

            else:
                if (self.pos.x - player.rect.width < player.pos.x and player.pos.x < self.pos.x + player.rect.width
                        and player.pos.y >= self.pos.y and player.pos.y < self.pos.y + player.rect.height):
                    self.isActive = False
                    self.surf.fill(self.color)
                    self.deactivate_button(level)

    def activate_button(self, level):
        for index, do in enumerate(self.activate_actions):
            if type(do) != str:
                continue
            if do == "ACTIVATE_OBJECT":
                for entity in level[self.activate_actions[index + 1]].all_sprites:
                    if entity.ID == self.activate_actions[index + 2]:
                        entity.isActive = True
                        break
                        
            if do == "DEACTIVATE_OBJECT":
                for entity in level[self.activate_actions[index + 1]].all_sprites:
                    if entity.ID == self.activate_actions[index + 2]:
                        entity.isActive = False
                        break
                        

    def deactivate_button(self, level):
        for index, do in enumerate(self.deactivate_actions):
            if type(do) != str:
                continue
            if do == "ACTIVATE_OBJECT":
                for entity in level[self.deactivate_actions[index + 1]].all_sprites:
                    if entity.ID == self.deactivate_actions[index + 2]:
                        entity.isActive = True
                        break
                    
            if do == "DEACTIVATE_OBJECT":
                for entity in level[self.deactivate_actions[index + 1]].all_sprites:
                    if entity.ID == self.deactivate_actions[index + 2]:
                        entity.isActive = False
                        break


class SwitchingPanel(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, color, level_ID, ID, draw_layer):
        super().__init__()
        self.surf = pygame.Surface((width, height))
        self.surf.fill(color)
        self.rect = self.surf.get_rect()
        self.pos = pygame.math.Vector2(x, y)
        self.ID = ID
        self.draw_layer = draw_layer
        self.rect.midbottom = self.pos
        self.level_ID = level_ID

    def switch_level(self, player, level):
        if (self.pos.x - player.rect.width < player.pos.x and player.pos.x < self.pos.x + player.rect.width
                and player.pos.y >= self.pos.y and player.pos.y < self.pos.y + player.rect.height):
            level[-1] = self.level_ID


class Cube(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, color, ID, draw_layer):
        super().__init__()
        self.surf = pygame.Surface((width, height))
        self.surf.fill(color)
        self.rect = self.surf.get_rect()
        self.pos = pygame.math.Vector2(x, y)
        self.vel = pygame.math.Vector2(0, 0)
        self.acc = pygame.math.Vector2(0, 0)
        self.is_held = False
        self.ID = ID
        self.draw_layer = draw_layer
        self.rect.midbottom = self.pos

    def move(self, collision_group):
        self.acc = pygame.math.Vector2(0, config['PHYSICS']['GRAVITY'])
        collides = pygame.sprite.spritecollide(self, collision_group, False)
        for entity in collides:
            if entity is not self:
                if self.rect.top + 1 < entity.rect.bottom:
                    self.acc.x += entity.acc.x

        self.acc.x += self.vel.x * config['PHYSICS']['FRICTION']
        self.vel += self.acc
        self.pos += self.vel + config['PHYSICS']['FRICTION'] * self.acc

        if self.pos.x > config['WIDTH'] - self.rect.width / 2:
            self.pos.x = config['WIDTH'] - self.rect.width / 2
        if self.pos.x < 0 + self.rect.width / 2:
            self.pos.x = 0 + self.rect.width / 2

        self.rect.midbottom = self.pos

    def update(self, collision_group):
        if not self.is_held:
            collides = pygame.sprite.spritecollide(
                self, collision_group, False)
            for entity in collides:
                if entity is not self:
                    delta_x = entity.rect.centerx - self.rect.centerx
                    gap_x = abs(delta_x) - self.rect.width / \
                        2 - entity.rect.width / 2
                    delta_y = entity.rect.centery - self.rect.centery
                    gap_y = abs(delta_y) - self.rect.height / \
                        2 - entity.rect.height / 2

                    if abs(gap_x) > abs(gap_y):
                        self.vel.y = 0
                        if delta_y < 0:
                            self.pos.y = entity.rect.bottom + self.rect.height
                        else:
                            self.pos.y = entity.rect.top + 1
                            self.is_jumping = False
                    else:
                        self.vel.x = 0
                        if delta_x < 0:
                            self.pos.x = entity.rect.right + self.rect.width / 2
                        else:
                            self.pos.x = entity.rect.left - self.rect.width / 2
                    self.rect.midbottom = self.pos


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, color, ID, draw_layer):
        super().__init__()
        self.surf = pygame.Surface((width, height))
        self.surf.fill(color)
        self.rect = self.surf.get_rect()
        self.pos = pygame.math.Vector2(x, y)
        self.vel = pygame.math.Vector2(0, 0)
        self.acc = pygame.math.Vector2(0, 0)
        self.is_jumping = False
        self.direction = 1
        self.is_holding = False
        self.held_object = None
        self.ID = ID
        self.draw_layer = draw_layer
        self.rect.midbottom = self.pos

    def move(self):
        self.acc = pygame.math.Vector2(0, config['PHYSICS']['GRAVITY'])
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_LEFT]:
            self.acc.x += -config['PHYSICS']['ACCELERATION']
        if pressed_keys[K_RIGHT]:
            self.acc.x += config['PHYSICS']['ACCELERATION']

        self.acc.x += self.vel.x * config['PHYSICS']['FRICTION']
        self.vel += self.acc
        self.pos += self.vel + config['PHYSICS']['FRICTION'] * self.acc

        if self.pos.x > config['WIDTH'] - self.rect.width / 2:
            self.pos.x = config['WIDTH'] - self.rect.width / 2
        if self.pos.x < 0 + self.rect.width / 2:
            self.pos.x = 0 + self.rect.width / 2

        self.rect.midbottom = self.pos

    def update(self, collision_group):
        collides = pygame.sprite.spritecollide(self, collision_group, False)
        for entity in collides:
            if entity is not self:
                delta_x = entity.rect.centerx - self.rect.centerx
                gap_x = abs(delta_x) - self.rect.width / \
                    2 - entity.rect.width / 2
                delta_y = entity.rect.centery - self.rect.centery
                gap_y = abs(delta_y) - self.rect.height / \
                    2 - entity.rect.height / 2

                if abs(gap_x) > abs(gap_y):
                    self.vel.y = 0
                    if delta_y < 0:
                        self.pos.y = entity.rect.bottom + self.rect.height
                    else:
                        self.pos.y = entity.rect.top + 1
                        self.is_jumping = False
                else:
                    self.vel.x = 0
                    if delta_x < 0:
                        self.pos.x = entity.rect.right + self.rect.width / 2
                    else:
                        self.pos.x = entity.rect.left - self.rect.width / 2
                self.rect.midbottom = self.pos
        if self.vel.x > 0:
            self.direction = 1
        elif self.vel.x < 0:
            self.direction = -1

        if self.is_holding:
            self.held_object.pos.x = self.pos.x
            self.held_object.pos.y = self.pos.y
            self.held_object.rect.center = self.rect.center

    def jump(self, collision_group):
        collides = pygame.sprite.spritecollide(self, collision_group, False)
        collides.remove(self)
        # If the player is on a platform then they can jump
        if collides and not self.is_jumping:
            self.vel.y = -config['PHYSICS']['JUMP_POWER']
            self.is_jumping = True

    def stop_jump(self):
        if self.vel.y < -config['PHYSICS']['SHORT_JUMP_POWER'] and self.is_jumping:
            self.vel.y = -config['PHYSICS']['SHORT_JUMP_POWER']

    def hold_object(self, all_sprites_group, holdable_group):
        if self.is_holding:
            collision_sprite = pygame.sprite.Sprite()
            collision_sprite.rect = self.held_object.rect.copy()
            collision_sprite.rect.x += self.rect.width * self.direction
            if pygame.sprite.spritecollide(collision_sprite, all_sprites_group, False):
                collision_sprite.rect.x -= self.rect.width * self.direction * 2
                if pygame.sprite.spritecollide(collision_sprite, all_sprites_group, False):
                    return False
                else:
                    self.held_object.pos = collision_sprite.rect.midbottom
                    self.held_object.rect.midbottom = self.held_object.pos
                    self.held_object.vel = self.vel.copy()
                    self.held_object.acc = self.acc.copy()
                    self.is_holding = False
                    self.held_object.is_held = False
                    return True
            else:
                self.held_object.pos = collision_sprite.rect.midbottom
                self.held_object.rect.midbottom = self.held_object.pos
                self.held_object.vel = self.vel.copy()
                self.held_object.acc = self.acc.copy()
                self.is_holding = False
                self.held_object.is_held = False
                return True

        else:
            proximity_sprite = pygame.sprite.Sprite()
            proximity_sprite.rect = pygame.Rect(self.rect.left - self.rect.width, self.rect.top -
                                                self.rect.height, self.rect.width * 3, self.rect.height * 3)
            holdable_objects = pygame.sprite.spritecollide(
                proximity_sprite, holdable_group, False)
            for entity in holdable_objects:
                if entity is not self:
                    self.held_object = entity
                    self.is_holding = True
                    self.held_object.vel = pygame.Vector2(0, 0)
                    self.held_object.acc = pygame.Vector2(0, 0)
                    self.held_object.pos.x = self.rect.left
                    self.held_object.pos.y = self.rect.top
                    self.held_object.rect.topleft = self.held_object.pos
                    self.held_object.is_held = True
                    return True
            return False
