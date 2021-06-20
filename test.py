from array import array
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
    pygame.K_LALT: False,
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
        self.touches = 0
        self.dead = False

    def update(self, delta_time: float):
        self.position += self.velocity * delta_time

    def render(self, win):
        win.blit(self.img, (self.position.x, self.position.y))

    def __repr__(self):
        return f'Entity(position={repr(self.position)}, velocity={repr(self.position)})'

    def isdead(self):
        return self.dead

    def respawn(self, touches_in_a_second):
        self.touches = 0
        rnd_x = random.randint(200, 700)
        if touches_in_a_second > 10:
            self.position.x = rnd_x
            self.position.y = -50

    def die(self):
        x = random.randint(10, 600)
        y = random.randint(50, 100)
        v = Vector2()
        pos = Vector2(x, -y)
        self.velocity = v
        self.position = pos
        self.dead = True
        return True

    def borders(self):
        x = self.position.x
        y = self.position.y
        v = Vector2(-1, 0)
        if x > 735:
            self.position.x = 734
            self.velocity = self.velocity.__mul__(v)
            self.touches += 1
            self.RightToLeft = False
        elif x < 2:
            self.position.x = 3
            self.velocity = self.velocity.__mul__(v)
            self.touches += 1
            self.RightToLeft = True
        if y > 535:
            self.position.y = 534
            self.touches += 1
            self.velocity = self.velocity.__mul__(Vector2(0, -1))
        if y < -100:
            self.position.y = -90
            self.velocity = self.velocity.__mul__(Vector2(0, 1))

    def is_touching_border(self):
        x = self.position.x
        y = self.position.y
        if x > 735:
            return True
        elif x < 2:
            return True
        if y > 535:
            return True
        if y < -0:
            return True
        return False

    def collision(self, other):
        v = Vector2(1, 1)
        rnd = random.randint(7, 10)
        rnd1 = random.randint(6, 9)
        if isinstance(other, Entity):
            distance = math.sqrt(
                math.pow(self.position.x - other.position.x, 2) + math.pow(self.position.y - other.position.y, 2))
            if distance < 36:
                if self.velocity.x > 0:
                    self.position.x -= 10
                elif self.velocity.x < 0:
                    self.position.x += 10
                else:
                    self.position.y += 10
                    other.position.y -= 10
                other.velocity = other.velocity * Vector2(-0.1 * rnd, -1)
                self.touches += 1
                self.velocity = self.velocity * Vector2(-1, -0.1 * rnd1)
                self.touches += 1
                # self.position.__add__(v)
                return True


class Spaceship(Entity):
    THRUST = 100.0
    MAX_THRUST = 300.0
    TELEPORT_POINTS = 3
    LIVES = 3

    def __init__(self):
        img = pygame.image.load("ship.png")
        super(Spaceship, self).__init__(Vector2(350, 500), img)
        self.img = img
        self.LIVES = 3
        self.kills = 0

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
        return Bullet(self.position.x + 12, self.position.y)

    def teleport_points_add(self):
        if self.kills - 1 % 2 and self.TELEPORT_POINTS < 10:
            self.TELEPORT_POINTS += 1


class Enemy(Entity):
    MAX_THRUST = 200.0

    def __init__(self):
        x_initial_position = random.randint(200, 600)
        self.is_dead = False
        self.sprites = []
        self.sprites.append(pygame.image.load("enemy.png"))
        self.sprites.append(pygame.image.load("enemy2.png"))
        self.sprites.append(pygame.image.load("enemy1.png"))
        self.sprites.append(pygame.image.load("enemy3.png"))
        self.sprites.append(pygame.image.load("enemy4.png"))
        self.current_sprite = 0
        self.img = self.sprites[int(self.current_sprite)]
        super(Enemy, self).__init__(Vector2(x_initial_position, 0), self.img)

    def update_sprite(self):
        if self.current_sprite == 4:
            self.current_sprite = 0
        else:
            self.current_sprite += 1
        self.img = self.sprites[int(self.current_sprite)]

    def move(self, delta_time: float):
        prev_value = self.velocity.copy()
        thrust = random.randint(1, 99)
        dy = random.randint(1, 35)
        if self.RightToLeft:
            self.velocity.x += thrust * delta_time
        else:
            self.velocity.x -= thrust * delta_time
        if self.velocity.length() >= Enemy.MAX_THRUST:
            self.velocity = prev_value
        self.velocity.y += dy * delta_time


class Bullet(Entity):
    def __init__(self, player_x, player_y):
        img_bullet = pygame.image.load("bullet.png")
        super(Bullet, self).__init__(Vector2(player_x, player_y), img_bullet)
        self.player_x = player_x
        self.player_y = player_y
        self.is_shot = False

    def fire_bullet(self):
        if KEYMAP[pygame.K_LALT]:
            self.velocity.y = -300
            self.is_shot = True
            return True
        return False

    def respawn_bullet(self):
        v = Vector2(0, 0)
        self.position = v
        self.velocity = Vector2()
        self.img = self.img
        self.RightToLeft = True
        self.touches = 0


class Item(Entity):
    def __init__(self):
        self.img = pygame.image.load("heart.png")
        super().__init__(Vector2(0, 0), self.img)

    def appear(self):
        x = random.randint(0, 730)
        y = random.randint(0, 530)
        self.position.x = x
        self.position.y = y

    def pickup(self, spaceship: Spaceship):
        distance = math.sqrt(
            math.pow(self.position.x - spaceship.position.x, 2) + math.pow(self.position.y - spaceship.position.y, 2))
        if distance < 36:
            self.position.x = -100
            self.position.y = -100
            spaceship.LIVES += 1

TARGET_FPS = 60
TARGET_FRAME_TIME = 1 / TARGET_FPS


def main():
    pygame.init()
    pygame.font.init()
    my_font = pygame.font.Font('superstarfont.ttf', 20)
    text_surface = my_font.render(' 123', False, (244, 0, 244))
    text_surface1 = my_font.render(' 123', False, (244, 0, 244))
    text_surface_lives = my_font.render('123', False, (244, 244, 244))
    win = pygame.display.set_mode((800, 600))
    win.blit(text_surface, (0, 0))
    background = pygame.image.load('background1.png')
    bullet = Spaceship().firepos()
    enemy1 = Enemy()
    cooldown = False
    enemy1.position.x = 200
    enemy2 = Enemy()
    enemy2.position.x = 100
    enemy2.RightToLeft = False
    heart = Item()
    heart.position.x = -10
    heart.position.y = -10
    entities = [bullet, Spaceship(), Enemy(), enemy1, enemy2, heart]
    running = True
    last_time = time.time()
    last_tick = time.time()
    a_second = 0
    last_touches = 0
    fps = 0
    new_bullet = False
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
        t = time.time()
        for entity in entities:
            # cooldown of a second for the life system
            if time.time() > t:
                cooldown = False
            # checks if player is hit
            if (entities[1].collision(entities[2]) or entities[1].collision(entities[3]) or entities[1].collision(
                    entities[4])) and not cooldown:
                entities[1].LIVES -= 1
                cooldown = True
                t = time.time() + 1
                print("Game Over")
                if entities[1].LIVES < 1:
                    running = False
            if type(entity) is Item:
                entity.pickup(entities[1])
                # every x seconds heart appears on the map
                if a_second % 400 == 0:
                    print("shalom")
                    heart.appear()
            # collision between bullet and enemies -> need help in this area. now a good looking code.
            if entities[0].collision(entities[2]) and entities[0].is_shot:
                new_bullet = False
                entities[1].kills += 1
                entities[1].teleport_points_add()
                entities[2].die()
                entities[2].update_sprite()
            a = entities[0].fire_bullet()
            if entities[0].collision(entities[3]) and entities[0].is_shot:
                new_bullet = False
                entities[1].kills += 1
                entities[1].teleport_points_add()
                entities[3].die()
                entities[3].update_sprite()
            a = entities[0].fire_bullet()
            if entities[0].collision(entities[4]) and entities[0].is_shot:
                new_bullet = False
                entities[1].kills += 1
                entities[1].teleport_points_add()
                entities[4].die()
                entities[4].update_sprite()
            entities[2].collision(entities[3])
            entities[3].collision(entities[4])
            entities[4].collision(entities[2])
            # collision between the enemies among themselves
            # if entities[2].collision(entities[3]):
            #     entities[2].velocity = entities[2].velocity * Vector2(-1, -1)
            #     entities[2].position.x += 2
            #     entities[3].velocity = entities[3].velocity * Vector2(-1, -1)
            # elif entities[2].collision(entities[4]):
            #     entities[2].velocity = entities[2].velocity * Vector2(-1, -1)
            #     entities[2].position.x += 2
            #     entities[4].velocity = entities[4].velocity * Vector2(-1, -1)
            # elif entities[3].collision(entities[4]):
            #     entities[3].position.x += 2
            #     entities[3].velocity = entities[3].velocity * Vector2(-1, -1)
            #     entities[4].velocity = entities[4].velocity * Vector2(-1, -1)
            a = entities[0].fire_bullet()
            if a:
                new_bullet = True
            if entities[0].is_touching_border():
                new_bullet = False
            if not a and not new_bullet:
                entities[0] = (entities[1].firepos())
            entity.borders()
            entity.update(delta)
            if a_second % 2 == 0 and type(entity) is Enemy:
                if entity.touches - last_touches > 10:
                    entity.respawn(entity.touches - last_touches)
                    entity.move(delta)
                last_touches = entity.touches
            # enemy movment
            entities[2].move(delta)
            entities[3].move(delta)
            entities[4].move(delta)
            text_surface = my_font.render(' {0} kills'.format(entities[1].kills), False, (244, 0, 244))
            text_surface1 = my_font.render('Teleport points {0}'.format(entities[1].TELEPORT_POINTS), False,
                                           (244, 0, 244))
            text_surface_lives = my_font.render(' {0} Lives'.format(entities[1].LIVES), False, (244, 0, 244))
        win.fill((0, 0, 0))
        win.blit(background, (0, 0))
        win.blit(text_surface, (0, 0))
        win.blit(text_surface_lives, (0, 100))
        win.blit(text_surface1, (600, 0))
        for entity in entities:
            entity.render(win)

        pygame.display.update()
        after_time = time.time()
        frame_time = after_time - before_time
        if frame_time <= TARGET_FRAME_TIME:
            time.sleep(TARGET_FRAME_TIME - frame_time)
            a_second += 1
        if time.time() - last_tick >= 1:

            print(f'FPS: {fps}')
            fps = 0
            last_tick = time.time()


if __name__ == '__main__':
    main()
