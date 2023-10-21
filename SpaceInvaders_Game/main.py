import math
import pygame
import sys
import random
from pygame import mixer

# Initialize Pygame
pygame.init()

# Creating the screen
screen = pygame.display.set_mode((800, 600))

# BackGround Screen
background = pygame.image.load('backGround.png')

# BackGround Sound
# mixer.music.load('background.wav')
# mixer.music.play(-1)

# Title and Icon Edit
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('galaxy.png')
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load('space.png')
playerX = 370
playerY = 480
playerX_change = 0

# Score
score = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10

# Game Over Text
over_font = pygame.font.Font('freesansbold.ttf', 64)

# Enemys
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_enemies = 5

for i in range(num_enemies):
    enemyImg.append(pygame.image.load('alien.png'))
    enemyX.append(random.randint(64, 736))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(4)
    enemyY_change.append(40)

# Laser
# state = "ready" - not shot ready
# state = "fire" - it was fired
laserImg = pygame.image.load('laser.png')
laserX = 0
laserY = 480
laserX_change = 0
laserY_change = 2.5
laser_state = "ready"


# Laser2
# state = "ready" - not shot ready
# state = "fire" - it was fired
laserImg = pygame.image.load('laser.png')
laser2X = 0
laser2Y = 480
laser2X_change = 0
laser2Y_change = 2.5
laser2_state = "ready"


def player(x, y):
    screen.blit(playerImg, (x, y))


def alien_enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def laser_fired(x, y):
    global laser_state
    laser_state = "fire"
    screen.blit(laserImg, (x + 18, y + 10))


def laser_fired2(x, y):
    global laser2_state
    laser2_state = "fire"
    screen.blit(laserImg, (x - 22, y + 10))


def isCollision(enemyX, enemyY, laserX, laserY, laser2X, laser2Y, laser_state, laser2_state):
    distance_laser = math.sqrt((math.pow(enemyX - laserX, 2) + math.pow(enemyY - laserY, 2)))
    distance_laser2 = math.sqrt((math.pow(enemyX - laser2X, 2) + math.pow(enemyY - laser2Y, 2)))
    if laser_state == "fire" and distance_laser < 27:
        return True
    elif laser2_state == "fire" and distance_laser2 < 27:
        return True
    else:
        return False


def show_score(x,y):
    score_show = font.render("Score : " + str(score), True, (255, 255, 255))
    screen.blit(score_show, (x, y))


def game_over_text(x, y):
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    x = 200
    y = 250
    screen.blit(over_text, (x, y))


# Game Loop, that cloeses when it is needed
running = True
while running:
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                playerX_change = -0.5
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                playerX_change = 0.5
            if event.key == pygame.K_SPACE and laser_state == "ready":
                laserX = playerX
                laser_fired(laserX, laserY)
                mixer.music.load('laser.wav')
                mixer.music.play()
            elif event.key == pygame.K_SPACE and laser2_state == "ready" and laser_state == "fire":
                laser2X = playerX
                laser_fired2(laser2X, laser2Y)
                mixer.music.load('laser.wav')
                mixer.music.play()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT or event.key == pygame.K_d or event.key == pygame.K_a:
                playerX_change = 0

    # Player movement
    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # Enemy movement
    for i in range(num_enemies):

        # Game Over
        if enemyY[i] > 400:
            for j in range (num_enemies):
                enemyY[j] = 2000
            game_over_text(0, 0)
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 0.6
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -0.6
            enemyY[i] += enemyY_change[i]

        # Collision into the enemy
        collision = False
        collision = isCollision(enemyX[i], enemyY[i], laserX, laserY, laser2X, laser2Y, laser_state, laser2_state)
        if collision:
            mixer.music.load('explosion.wav')
            mixer.music.play()
            laserY = 480
            laser_state = "ready"
            laser2_state = "ready"
            score += 1
            enemyX[i] = random.randint(64, 736)
            enemyY[i] = random.randint(50, 150)

        alien_enemy(enemyX[i], enemyY[i], i)

    # Laser movement
    if laserY <= 0:
        laserY = 480
        laser_state = "ready"
    if laser_state == "fire":
        laser_fired(laserX, laserY)
        laserY -= laserY_change

    # Laser 2 movement
    if laser2Y <= 0:
        laser2Y = 480
        laser2_state = "ready"
    if laser2_state == "fire":
        laser_fired2(laser2X, laser2Y)
        laser2Y -= laser2Y_change

    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()

# Quit Pygame when you're done
pygame.quit()
sys.exit()
