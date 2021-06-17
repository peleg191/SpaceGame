import pygame

# Screen
pygame.init()
win = pygame.display.set_mode((800, 600))
# Player
playerImg = pygame.image.load("ship.png")
global playerX, playerY
playerX = 370
playerY = 470
Xchange = 0
teleport_points = 3
# Caption and Icon
icon = pygame.image.load("console.png")
pygame.display.set_icon(icon)
pygame.display.set_caption("A Game")
teleportImg = pygame.image.load("Teleport.png")
teleportImg1 = pygame.image.load("Teleport1.png")
teleportImg2 = pygame.image.load("Teleport2.png")
# Background
background = pygame.image.load('background1.png')


# Functions


def update_screen():
    pygame.display.update()


def player(x, y):
    win.blit(playerImg, (x, y))


# main game loop
running = True
while running:
    win.fill((0, 0, 0))
    win.blit(background, (0, 0))
    if teleport_points == 3:
        win.blit(teleportImg, (10, 10))
    elif teleport_points == 2:
        win.blit(teleportImg2, (10, 10))
    elif teleport_points == 1:
        win.blit(teleportImg1, (10, 10))
    for event in pygame.event.get():
        print(event)
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F12:
                teleport_points = 3
            if event.key == pygame.K_LEFT:
                playerX -= 5
            elif event.key == pygame.K_RIGHT:
                playerX += 5
            elif event.key == pygame.K_UP:
                playerY -= 5
            elif event.key == pygame.K_DOWN:
                playerY += 5
            # Teleportation
            if event.key == pygame.K_RALT and teleport_points > 0:
                pygame.time.wait(50)
                playerX += 100
                teleport_points -= 1
            if event.key == pygame.K_LALT and teleport_points > 0:
                pygame.time.wait(50)
                teleport_points -= 1
                playerX -= 100
    # Borders
    if playerX > 735:
        playerX = 735
    elif playerX < 2:
        playerX = 1
    if playerY > 700:
        playerY = 0
    if playerY < -100:
        playerY = 599
    player(playerX, playerY)
    pygame.display.update()
