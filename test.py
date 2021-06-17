from typing import *
import pygame
import math
import time
import random

# Caption and Icon
icon = pygame.image.load("console.png")
pygame.display.set_icon(icon)
pygame.display.set_caption("Space Game")
KEYMAP = {
    pygame.K_LEFT: False,
    pygame.K_RIGHT: False,
    pygame.K_UP: False,
    pygame.K_DOWN: False,
    pygame.K_SPACE: False,
    pygame.K_F12: False,
}


class Vector2:

    def __init__(self, x=0.0, y=0.0):
        self.x = float(x)
        self.y = float(y)

    def __add__(self, other):
        if isinstance(other, float):
            return Vector2(self.x + other, self.y + other)
        elif isinstance(other, Vector2):
            return Vector2(self.x + other.x, self.y + other.y)
        else:
            assert False, "Unknown type"

    def __mul__(self, other):
        if isinstance(other, float):
            return Vector2(self.x * other, self.y * other)
        elif isinstance(other, Vector2):
            return Vector2(self.x * other.x, self.y * other.y)
        else:
            assert False, "Unknown type"

    def shorten_length(self, reduction_length: float):
        return self * (1.0 - reduction_length / self.length())

    def length(self) -> float:
        return math.sqrt(self.x ** 2 + self.y ** 2)

    def copy(self):
        return Vector2(self.x, self.y)

    def __repr__(self):
        return f'Vector2(x={self.x}, y={self.y})'

    def print_scalar(self):
        return math.sqrt(self.x ** 2 + self.y ** 2)


class Entity:

    def __init__(self, position: Vector2, img):
        self.position = position
        self.velocity = Vector2()
        self.img = img
        self.RightToLeft = True
        self.side_touches = 0

    def update(self, delta_time: float):
        self.position += self.velocity * delta_time

    def render(self, win):
        win.blit(self.img, (self.position.x, self.position.y))

    def __repr__(self):
        return f'Entity(position={repr(self.position)}, velocity={repr(self.position)})'

    def borders(self):
        x = self.position.x
        y = self.position.y
        v = Vector2(-1, 0)
        if x > 735:
            self.position.x = 735
            self.velocity = self.velocity.__mul__(v)
            self.side_touches += 1
            self.RightToLeft = False
        elif x < 2:
            self.position.x = 1
            self.velocity = self.velocity.__mul__(v)
            self.side_touches += 1
            self.RightToLeft = True
        if y > 700:
            self.position.y = 0
        if y < -100:
            self.position.y = 599

    def collision(self, other):
        if isinstance(other, Entity):
            distance = math.sqrt(
                math.pow(self.position.x - other.position.x, 2) + math.pow(self.position.y - other.position.y, 2))
            if distance < 36:
                print("Collision")
                return True


class Spaceship(Entity):
    THRUST = 400.0
    MAX_THRUST = 200.0
    TELEPORT_POINTS = 9

    def __init__(self):
        img = pygame.image.load("ship.png")
        super(Spaceship, self).__init__(Vector2(350, 500), img)
        self.img = img

    def update(self, delta_time: float):
        prev_value = self.velocity.copy()
        prev_press = ""
        if KEYMAP[pygame.K_UP]:
            self.velocity.y -= Spaceship.THRUST * delta_time
            prev_press = "up"
        if KEYMAP[pygame.K_DOWN]:
            self.velocity.y += Spaceship.THRUST * delta_time
            prev_press = "down"
        if KEYMAP[pygame.K_LEFT]:
            prev_press = "left"
            self.velocity.x -= Spaceship.THRUST * delta_time

        if KEYMAP[pygame.K_RIGHT]:
            prev_press = "right"
            self.velocity.x += Spaceship.THRUST * delta_time
        if KEYMAP[pygame.K_SPACE] and self.TELEPORT_POINTS > 0:
            if prev_press == "right":
                self.position.x += 100
                self.use_teleport()
            if prev_press == "left":
                self.position.x -= 100
                self.use_teleport()
        if self.velocity.length() >= Spaceship.MAX_THRUST:
            self.velocity = prev_value
        super(Spaceship, self).update(delta_time)

    def use_teleport(self):
        self.TELEPORT_POINTS -= 1

    def render(self, win):
        win.blit(self.img, (self.position.x, self.position.y))

    def firepos(self):
        return Bullet(self.position.x, self.position.y)


class Enemy(Entity):
    MAX_THRUST = 200.0

    def __init__(self):
        img = pygame.image.load("enemy.png")
        img1 = pygame.image.load("enemy1.png")
        super(Enemy, self).__init__(Vector2(350, 0), img)
        self.img = img
        self.img1 = img1

    def move(self, delta_time: float):
        prev_value = self.velocity.copy()
        thrust = random.randint(198, 199)
        dy = random.randint(1, 50)
        if self.RightToLeft:
            self.velocity.x += thrust * delta_time
        else:
            self.velocity.x -= thrust * delta_time
        if self.velocity.length() >= Enemy.MAX_THRUST:
            self.velocity = prev_value
        if self.side_touches > 0:
            self.velocity.y += 0.1


class Bullet(Entity):
    def __init__(self, player_x, player_y):
        img_bullet = pygame.image.load("bullet.png")
        super(Bullet, self).__init__(Vector2(player_x, player_y), img_bullet)
        self.player_x = player_x
        self.player_y = player_y

    def render(self, win):
        win.blit(self.img, (self.player_x, self.player_y))

    def fireBullet(self):
        self.velocity.y -= 5


TARGET_FPS = 60
TARGET_FRAME_TIME = 1 / TARGET_FPS


def main():
    pygame.init()
    win = pygame.display.set_mode((800, 600))
    background = pygame.image.load('background1.png')
    entities = [Spaceship().firepos(), Enemy(), Spaceship()]
    running = True
    last_time = time.time()
    last_tick = time.time()
    fps = 0
    entities[0].fireBullet()
    while running:
        current_time = time.time()
        delta = current_time - last_time
        last_time = current_time
        before_time = time.time()
        fps += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key in KEYMAP:
                KEYMAP[event.key] = True
            elif event.type == pygame.KEYUP and event.key in KEYMAP:
                KEYMAP[event.key] = False

        for entity in entities:
            entity.borders()
            entity.update(delta)
            # enemy movment
            entities[1].move(delta)
        win.fill((0, 0, 0))
        win.blit(background, (0, 0))

        for entity in entities:
            # renders game
            entity.render(win)
            # collision between spaceship and enemy
            entities[1].collision(entities[2])

        pygame.display.update()
        after_time = time.time()
        frame_time = after_time - before_time
        if frame_time <= TARGET_FRAME_TIME:
            time.sleep(TARGET_FRAME_TIME - frame_time)
        if time.time() - last_tick >= 1:
            print(f'FPS: {fps}')
            fps = 0
            last_tick = time.time()


if __name__ == '__main__':
    main()
