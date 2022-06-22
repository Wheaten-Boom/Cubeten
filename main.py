import pygame
from pygame.locals import *


class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.surf = pygame.Surface((width, height))
        self.surf.fill((255, 128, 0))
        self.rect = self.surf.get_rect()
        self.pos = pygame.math.Vector2(x, y)
        self.rect.midbottom = self.pos


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((75, 75))
        self.surf.fill((0, 128, 255))
        self.rect = self.surf.get_rect()

        self.pos = pygame.math.Vector2((400, 500))
        self.vel = pygame.math.Vector2(0, 0)
        self.acc = pygame.math.Vector2(0, 0)
        self.is_jumping = False

    def move(self):
        # The Y value is 1 to simulate gravity
        self.acc = pygame.math.Vector2(0, 1)
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_LEFT]:
            self.acc.x += -ACCLERATION
        if pressed_keys[K_RIGHT]:
            self.acc.x += ACCLERATION
        if pressed_keys[K_UP]:
            self.jump()

        self.acc.x += self.vel.x * FRICTION
        self.vel += self.acc
        self.pos += self.vel + FRICTION * self.acc

        if self.pos.x > WIDTH - self.rect.width / 2:
            self.pos.x = WIDTH - self.rect.width / 2
        if self.pos.x < 0 + self.rect.width / 2:
            self.pos.x = 0 + self.rect.width / 2

        self.rect.midbottom = self.pos

    def update(self):
        collides = pygame.sprite.spritecollide(self, platforms, False)
        if collides and self.pos.y < collides[0].rect.bottom and self.vel.y > 0:
            # collides[0] is the first platform that the player collides with
            self.pos.y = collides[0].rect.top + 1
            self.vel.y = 0
            self.is_jumping = False
            self.rect.midbottom = self.pos

    def jump(self):
        collides = pygame.sprite.spritecollide(self, platforms, False)
        # If the player is on a platform then they can jump
        if collides and not self.is_jumping:
            self.vel.y = -JUMP_POWER
            self.is_jumping = True

    def stop_jump(self):
        if self.vel.y < -SHORT_JUMP_POWER and self.is_jumping:
            self.vel.y = -SHORT_JUMP_POWER


def main():
    pygame.init()
    global ACCLERATION, FRICTION, JUMP_POWER, SHORT_JUMP_POWER, WIDTH, HEIGHT
    ACCLERATION = 1
    JUMP_POWER = 20
    SHORT_JUMP_POWER = 10
    FRICTION = -0.125
    WIDTH = 800
    HEIGHT = 600
    FPS = 60

    FramePerSec = pygame.time.Clock()

    displaysurface = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Cubeten')

    all_sprites = pygame.sprite.Group()

    global platforms
    platforms = pygame.sprite.Group()
    platforms.add(Platform(400, 600, 800, 100))
    platforms.add(Platform(400, 350, 300, 25))
    all_sprites.add(platforms)

    player = Player()
    all_sprites.add(player)

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                quit()
            if event.type == KEYUP:
                if event.key == K_UP:
                    player.stop_jump()

        displaysurface.fill((0, 0, 0))

        for entity in all_sprites:
            entity.update()
            displaysurface.blit(entity.surf, entity.rect)

        player.move()

        pygame.display.update()
        FramePerSec.tick(FPS)


if __name__ == "__main__":
    main()
