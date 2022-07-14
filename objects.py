import math
import pygame
from pygame.locals import *
from main import *

config = load_configuration()


class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, color, ID):
        super().__init__()
        self.surf = pygame.Surface((width, height))
        self.surf.fill(color)
        self.rect = self.surf.get_rect()
        self.pos = pygame.math.Vector2(x, y)
        self.ID = ID
        self.rect.midbottom = self.pos


class MovingPlatform(pygame.sprite.Sprite):
    def __init__(self, x1, y1, x2, y2, speed, width, height, color, ID, isActive=True):
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
    def __init__(self, x, y, width, height, color, activate_actions, deactivate_actions, ID, mode, isActive=False):
        super().__init__()
        self.surf = pygame.Surface((width, height))
        self.surf.fill(color)
        self.rect = self.surf.get_rect()
        self.pos = pygame.math.Vector2(x, y)
        self.isActive = isActive
        self.activate_actions = activate_actions
        self.deactivate_actions = deactivate_actions
        self.mode = mode
        self.ID = ID
        self.rect.midbottom = self.pos

    def update(self, collision_group, activation_group, player):
        if self.mode == "BUTTON":
            if not self.isActive:
                collides = pygame.sprite.spritecollide(
                    self, collision_group, False)
                for entity in collides:
                    if entity.rect.bottom == self.rect.top + 1:
                        self.isActive = True
                        self.activate_button(activation_group)
                        break
            else:
                collides = pygame.sprite.spritecollide(
                    self, collision_group, False)
                if not collides:
                    self.isActive = False
                    self.deactivate_button(activation_group)

        if self.mode == "SWITCH":
            if not self.isActive:
                if (self.pos.x - 50 < player.pos.x and player.pos.x < self.pos.x + 50 and player.pos.y >= self.pos.y and player.pos.y < self.pos.y + 75):
                    self.isActive = True
                    self.activate_button(activation_group)

            else:
                if (self.pos.x - 50 < player.pos.x and player.pos.x < self.pos.x + 50 and player.pos.y >= self.pos.y and player.pos.y < self.pos.y + 75):
                    self.isActive = False
                    self.deactivate_button(activation_group)

    def activate_button(self, activation_group):
        for index, do in enumerate(self.activate_actions):
            if type(do) != str:
                continue
            if do == "ACTIVATE_OBJECT":
                for entity in activation_group:
                    if entity.ID == self.activate_actions[index + 1]:
                        entity.isActive = True
                        break
            if do == "DEACTIVATE_OBJECT":
                for entity in activation_group:
                    if entity.ID == self.activate_actions[index + 1]:
                        entity.isActive = False
                        break

    def deactivate_button(self, activation_group):
        for index, do in enumerate(self.deactivate_actions):
            if type(do) != str:
                continue
            if do == "ACTIVATE_OBJECT":
                for entity in activation_group:
                    if entity.ID == self.deactivate_actions[index + 1]:
                        entity.isActive = True
                        break
            if do == "DEACTIVATE_OBJECT":
                for entity in activation_group:
                    if entity.ID == self.deactivate_actions[index + 1]:
                        entity.isActive = False
                        break


class Switching_Panel(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, color, ID, level_ID):
        super().__init__()
        self.surf = pygame.Surface((width, height))
        self.surf.fill(color)
        self.rect = self.surf.get_rect()
        self.pos = pygame.math.Vector2(x, y)
        self.ID = ID
        self.rect.midbottom = self.pos
        self.level_ID = level_ID

    def Switch_Level(self, player, level):
        if (self.pos.x - 50 < player.pos.x and player.pos.x < self.pos.x + 50 and player.pos.y >= self.pos.y and player.pos.y < self.pos.y + 75):
            level[-1] = self.level_ID


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, color):
        super().__init__()
        self.surf = pygame.Surface((width, height))
        self.surf.fill(color)
        self.rect = self.surf.get_rect()
        self.pos = pygame.math.Vector2(x, y)
        self.vel = pygame.math.Vector2(0, 0)
        self.acc = pygame.math.Vector2(0, 0)
        self.is_jumping = False
        self.rect.midbottom = self.pos

    def move(self, collision_group):
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
            delta_x = entity.rect.centerx - self.rect.centerx
            gap_x = abs(delta_x) - self.rect.width / 2 - entity.rect.width / 2
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

    def jump(self, collision_group):
        collides = pygame.sprite.spritecollide(self, collision_group, False)
        # If the player is on a platform then they can jump
        if collides and not self.is_jumping:
            self.vel.y = -config['PHYSICS']['JUMP_POWER']
            self.is_jumping = True

    def stop_jump(self):
        if self.vel.y < -config['PHYSICS']['SHORT_JUMP_POWER'] and self.is_jumping:
            self.vel.y = -config['PHYSICS']['SHORT_JUMP_POWER']
