from typing import *
import pygame
import math
import time

KEYMAP = {
    pygame.K_LEFT: False,
    pygame.K_RIGHT: False,
    pygame.K_UP: False,
    pygame.K_DOWN: False,
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


class Entity:

    def __init__(self, position: Vector2):
        self.position = position
        self.velocity = Vector2()

    def update(self, delta_time: float):
        self.position += self.velocity * delta_time

    def render(self, win):
        pass

    def __repr__(self):
        return f'Entity(position={repr(self.position)}, velocity={repr(self.position)})'


class Spaceship(Entity):
    THRUST = 400.0
    MAX_THRUST = 200.0

    def __init__(self):
        super(Spaceship, self).__init__(Vector2(350, 0))
        self._img = pygame.image.load("ship.png")

    def update(self, delta_time: float):
        prev_value = self.velocity.copy()

        if KEYMAP[pygame.K_UP]:
            self.velocity.y -= Spaceship.THRUST * delta_time

        if KEYMAP[pygame.K_DOWN]:
            self.velocity.y += Spaceship.THRUST * delta_time

        if KEYMAP[pygame.K_LEFT]:
            self.velocity.x -= Spaceship.THRUST * delta_time

        if KEYMAP[pygame.K_RIGHT]:
            self.velocity.x += Spaceship.THRUST * delta_time

        if self.velocity.length() >= Spaceship.MAX_THRUST:
            self.velocity = prev_value

        super(Spaceship, self).update(delta_time)

    def render(self, win):
        win.blit(self._img, (self.position.x, self.position.y))

    def borders(self):
        x = self.position.x
        y = self.position.y
        if x > 735:
            self.position.x = 735
        elif x < 2:
            self.position.x = 1
        if y > 700:
            self.position.y = 0
        if y < -100:
            self.position.y = 599
TARGET_FPS = 60
TARGET_FRAME_TIME = 1 / TARGET_FPS


def main():
    pygame.init()

    win = pygame.display.set_mode((800, 600))
    background = pygame.image.load('background1.png')

    entities = [
        Spaceship()
    ]

    running = True
    last_time = time.time()
    last_tick = time.time()
    fps = 0
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

        win.fill((0, 0, 0))
        win.blit(background, (0, 0))

        for entity in entities:
            entity.render(win)

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
