import pygame
import math
import time
import random

# Caption and Icon
icon = pygame.image.load("Assets/console.png")
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
        self.isfloor = False

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
        if touches_in_a_second > 12:
            self.position.y -= 50
            # self.velocity = Vector2(1, -3)

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
        v = Vector2(-0.5, 0)
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
        if y > 570:
            # self.position.y = 534
            # self.touches += 1
            # self.velocity = self.velocity.__mul__(Vector2(0, -1))
            self.position.y = -90
            self.velocity *= 0.7
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
        v_self = Vector2(self.velocity.x, self.velocity.y)
        v_other = Vector2(other.velocity.x, other.velocity.y)
        rnd = random.randint(7, 10)
        rnd1 = random.randint(7, 10)
        if isinstance(other, Entity):
            distance = math.sqrt(
                math.pow(self.position.x - other.position.x, 2) + math.pow(self.position.y - other.position.y, 2))
            if distance < 36:
                if self.velocity.x > 0:
                    self.position.x -= 6
                elif self.velocity.x < 0:
                    self.position.x += 6
                if self.velocity.y < 0:
                    self.position.y += 6
                elif self.velocity.y > 0:
                    self.position.y -= 6
                if other.velocity.x > 0:
                    other.position.x -= 6
                elif other.velocity.x < 0:
                    other.position.x += 6
                if other.velocity.y < 0:
                    other.position.y += 6
                elif other.velocity.y > 0:
                    other.position.y -= 6
                other.velocity = v_other * Vector2(-0.1 * rnd, -1)
                other.touches += 1
                self.velocity = v_self * Vector2(-1, -0.1 * rnd1)
                self.touches += 1
                return True


class Spaceship(Entity):
    THRUST = 250.0
    MAX_THRUST = 300.0
    TELEPORT_POINTS = 3
    LIVES = 3

    def __init__(self):
        img = pygame.image.load("Assets/ship.png")
        super(Spaceship, self).__init__(Vector2(350, 500), img)
        self.img = img
        self.LIVES = 3
        self.kills = 0

    def update(self, delta_time: float):
        prev_value = self.velocity.copy()
        prev_press = ""
        if KEYMAP[pygame.K_UP]:
            self.position.y -= 1
            self.velocity.y -= Spaceship.THRUST * delta_time
            prev_press = "up"
        if KEYMAP[pygame.K_DOWN]:
            self.position.y += 1
            self.velocity.y += Spaceship.THRUST * delta_time
            prev_press = "down"
        if KEYMAP[pygame.K_LEFT]:
            self.position.x -= 1
            prev_press = "left"
            self.velocity.x -= Spaceship.THRUST * delta_time
        if KEYMAP[pygame.K_RIGHT]:
            self.position.x += 1
            prev_press = "right"
            self.velocity.x += Spaceship.THRUST * delta_time
        if KEYMAP[pygame.K_F12]:
            self.isfloor = True
        if self.velocity.length() >= Spaceship.MAX_THRUST:
            self.velocity = prev_value
        super(Spaceship, self).update(delta_time)

    def update_once_in_a_second(self):
        prev_press = ""
        if KEYMAP[pygame.K_UP]:
            prev_press = "up"
        if KEYMAP[pygame.K_DOWN]:
            prev_press = "down"
        if KEYMAP[pygame.K_LEFT]:
            self.position.x -= 1
            prev_press = "left"
        if KEYMAP[pygame.K_RIGHT]:
            prev_press = "right"
        if KEYMAP[pygame.K_SPACE] and self.TELEPORT_POINTS > 0:
            if prev_press == "right":
                self.position.x += 100
                self.use_teleport()
            elif prev_press == "left":
                self.position.x -= 100
                self.use_teleport()
            elif prev_press == "up":
                self.position.y -= 100
                self.use_teleport()

    def use_teleport(self):
        self.TELEPORT_POINTS -= 1

    def render(self, win):
        win.blit(self.img, (self.position.x, self.position.y))

    def firepos(self):
        return Bullet(self.position.x + 12, self.position.y)

    def teleport_points_add(self):
        if self.kills - 1 % 2 and self.TELEPORT_POINTS < 10:
            self.TELEPORT_POINTS += 1

    def borders(self):
        x = self.position.x
        y = self.position.y
        v = Vector2(-0.5, 0)
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
            self.position.y = 530
            self.touches += 1
            self.velocity = self.velocity.__mul__(Vector2(0, -1))
            # self.position.y = -90
            # self.velocity *= 0.7
        if y < 0:
            self.position.y = 10
            self.velocity = self.velocity.__mul__(Vector2(0, -1))


class Enemy(Entity):
    MAX_THRUST = 200.0

    def __init__(self):
        x_initial_position = random.randint(200, 600)
        self.is_dead = False
        self.sprites = []
        self.sprites.append(pygame.image.load("Assets/enemy.png"))
        self.sprites.append(pygame.image.load("Assets/enemy2.png"))
        self.sprites.append(pygame.image.load("Assets/enemy1.png"))
        self.sprites.append(pygame.image.load("Assets/enemy3.png"))
        self.sprites.append(pygame.image.load("Assets/enemy4.png"))
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
        thrust = random.randint(50, 200)
        dy = random.randint(1, 160)
        if self.RightToLeft:
            self.velocity.x += thrust * delta_time
        else:
            self.velocity.x -= thrust * delta_time
        if self.velocity.length() >= self.MAX_THRUST:
            self.velocity = prev_value
        self.velocity.y += dy * delta_time


class Music:
    def __init__(self):
        self.img = pygame.image.load("Assets/music.png")
        self.img_music = pygame.image.load("Assets/music.png")
        self.img1 = pygame.image.load("Assets/mute.png")
        self.background_music = pygame.mixer.Sound("Assets/SpaceGame.mp3")
        self.shot_music = pygame.mixer.Sound("Assets/shot.mp3")
        self.pos = Vector2(0, 0)
        pygame.mixer.Sound.play(self.background_music, 100)
        self.shot_music.set_volume(0.05)


class Bullet(Entity):
    def __init__(self, player_x, player_y):
        img_bullet = pygame.image.load("Assets/bullet.png")
        super(Bullet, self).__init__(Vector2(player_x, player_y), img_bullet)
        self.player_x = player_x
        self.player_y = player_y
        self.is_shot = False

    def fire_bullet(self, music: Music):
        if KEYMAP[pygame.K_LALT]:
            self.velocity.y = -300
            self.is_shot = True
            pygame.mixer.Sound.play(music.shot_music)
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
        self.img = pygame.image.load("Assets/heart.png")
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
    pygame.mixer.init()
    music = Music()
    music.pos = Vector2(0, 570)
    my_font = pygame.font.Font('Assets/superstarfont.ttf', 20)
    my_font2 = pygame.font.Font('Assets/superstarfont.ttf', 80)
    text_surface = my_font.render(' 123', False, (200, 0, 244))
    text_surface1 = my_font.render(' 123', False, (200, 0, 244))
    text_surface_lives = my_font.render('123', False, (200, 244, 244))
    text_surface_general = my_font.render('123', False, (200, 244, 244))
    win = pygame.display.set_mode((800, 600))
    win.blit(text_surface, (0, 0))
    background = pygame.image.load('Assets/background1.png')
    bullet = Spaceship().firepos()
    enemy1 = Enemy()
    enemy1.position.x = 200
    enemy2 = Enemy()
    enemy2.position.x = 100
    enemy2.RightToLeft = False
    heart = Item()
    heart_appear = False
    heart.position.x = -100
    heart.position.y = -100
    entities = [bullet, Spaceship(), Enemy(), enemy1, enemy2, heart]
    running = True
    last_time = time.time()
    last_tick = time.time()
    this_time = time.time()
    a_second = 0
    last_touches = 0
    fps = 0
    new_bullet = False
    t = time.time()
    cooldown = False
    counter = 0
    game_over = False
    while running:
        current_time = time.time()
        delta = current_time - last_time
        last_time = current_time
        before_time = time.time()
        fps += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m or event.key == pygame.K_F12:
                    if pygame.mixer.Sound.get_volume(music.background_music) > 0:
                        pygame.mixer.Sound.set_volume(music.background_music, 0)
                        pygame.mixer.Sound.set_volume(music.shot_music, 0)
                        music.img = music.img1
                    else:
                        pygame.mixer.Sound.set_volume(music.background_music, 1.0)
                        pygame.mixer.Sound.set_volume(music.shot_music, 0.05)
                        music.img = music.img_music
            if event.type == pygame.KEYDOWN and event.key in KEYMAP:
                KEYMAP[event.key] = True
            elif event.type == pygame.KEYUP and event.key in KEYMAP:
                KEYMAP[event.key] = False
        for entity in entities:
            # cooldown of a second for the life system
            # checks if player is hit
            if time.time() > t:
                cooldown = False
            if (entities[1].collision(entities[2]) or entities[1].collision(entities[3]) or entities[1].collision(
                    entities[4]) or entities[2].collision(entities[1]) or entities[3].collision(entities[1]) or
                    entities[4].collision(entities[1])) and not cooldown:
                entities[1].LIVES -= 1
                cooldown = True
                t = time.time() + 3
                if entities[1].LIVES < 1:
                    game_over = True
            if type(entity) is Item:
                entity.pickup(entities[1])
                # every 10 seconds heart appears on the map
                if a_second % 600 == 0 and entities[1].LIVES == 1:
                    print("Heart Appears")
                    heart_appear = True
                    heart.appear()
            # collision between bullet and enemies -> need help in this area. now a good looking code.
            if entities[0].collision(entities[2]) and entities[0].is_shot:
                new_bullet = False
                entities[1].kills += 1
                entities[1].teleport_points_add()
                entities[2].die()
                entities[2].update_sprite()
            a = entities[0].fire_bullet(music)
            if entities[0].collision(entities[3]) and entities[0].is_shot:
                new_bullet = False
                entities[1].kills += 1
                entities[1].teleport_points_add()
                entities[3].die()
                entities[3].update_sprite()
            a = entities[0].fire_bullet(music)
            if entities[0].collision(entities[4]) and entities[0].is_shot:
                new_bullet = False
                entities[1].kills += 1
                entities[1].teleport_points_add()
                entities[4].die()
                entities[4].update_sprite()
            entities[2].collision(entities[3])
            entities[3].collision(entities[4])
            entities[4].collision(entities[2])
            a = entities[0].fire_bullet(music)
            if a:
                new_bullet = True
            if entities[0].is_touching_border():
                new_bullet = False
            if not a and not new_bullet:
                entities[0] = (entities[1].firepos())
            entity.borders()
            entity.update(delta)
            # every 2 seconds, if the entity is enemy and there were 12 collions, respawns the enemy
            if a_second % 120 == 0 and type(entity) is Enemy and entity.touches - last_touches > 12:
                entity.respawn(entity.touches - last_touches)
            last_touches = entity.touches
            if a_second % 3 == 0 and type(entity) is Spaceship:
                entity.update_once_in_a_second()
            # enemy movment
            if type(entity) is Enemy:
                entity.move(delta)
            text_surface = my_font.render(' {0} kills'.format(entities[1].kills), False, (200, 0, 244))
            text_surface1 = my_font.render('Teleport points {0}'.format(entities[1].TELEPORT_POINTS), False,
                                           (200, 0, 244))
            text_surface_lives = my_font.render(' {0} Lives'.format(entities[1].LIVES), False, (200, 0, 244))
            text_surface_general = my_font.render("Life Cooldown On", False, (200, 0, 244))
        text_surface_game = my_font2.render("Game Over", False, (200, 0, 244))
        win.fill((0, 0, 0))
        win.blit(background, (0, 0))
        win.blit(text_surface, (0, 0))
        win.blit(text_surface_lives, (0, 50))
        win.blit(text_surface1, (600, 0))
        win.blit(music.img, (music.pos.x, music.pos.y))
        if cooldown and not game_over:
            win.blit(text_surface_general, (300, 300))
        for entity in entities:
            entity.render(win)
        if game_over:
            if counter == 0:
                this_time = time.time()
            counter += 1
            win.blit(text_surface_game, (200, 300))
            this_time1 = time.time()
            if this_time1 - this_time > 5:
                running = False
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
