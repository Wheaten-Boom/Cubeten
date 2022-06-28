import pygame
from pygame.locals import *
from main import configuration

config = configuration().config


class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, color):
        super().__init__()
        self.surf = pygame.Surface((width, height))
        self.surf.fill(color)
        self.rect = self.surf.get_rect()
        self.pos = pygame.math.Vector2(x, y)
        self.rect.midbottom = self.pos


class MovingPlatform(pygame.sprite.Sprite):
    def __init__(self, x1, y1, x2, y2, speed, width, height, color, isActive=True):
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

    def move(self, collision_group):
        self.acc = pygame.math.Vector2(0, config['PHYSICS']['GRAVITY'])
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_LEFT]:
            self.acc.x += -config['PHYSICS']['ACCELERATION']
        if pressed_keys[K_RIGHT]:
            self.acc.x += config['PHYSICS']['ACCELERATION']
        if pressed_keys[K_UP]:
            self.jump(collision_group)

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
        if collides and self.pos.y < collides[0].rect.bottom and self.vel.y > 0:
            # collides[0] is the first platform that the player collides with
            self.pos.y = collides[0].rect.top + 1
            self.vel.y = 0
            self.is_jumping = False
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
