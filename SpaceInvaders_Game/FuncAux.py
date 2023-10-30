import math
import pygame
import sys
import random
from pygame import mixer


#game window
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Creating the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Health Bar')


# BackGround Screen
background = pygame.image.load('backGround.png')

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


#Displays the player
def player(x, y):
    screen.blit(playerImg, (x, y))


#Displays the alien
def alien_enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


#Displays the laser 2
def laser_fired(x, y):
    global laser_state
    laser_state = "fire"
    screen.blit(laserImg, (x + 18, y + 10))


#Displays the laser 2
def laser_fired2(x, y):
    global laser2_state
    laser2_state = "fire"
    screen.blit(laserImg, (x - 22, y + 10))


#Detects if it is a collision into a laser and a alien
def isCollision(enemyX, enemyY, laserX, laserY, laser2X, laser2Y, laser_state, laser2_state):
    distance_laser = math.sqrt((math.pow(enemyX - laserX, 2) + math.pow(enemyY - laserY, 2)))
    distance_laser2 = math.sqrt((math.pow(enemyX - laser2X, 2) + math.pow(enemyY - laser2Y, 2)))
    if laser_state == "fire" and distance_laser < 27:
        return True
    elif laser2_state == "fire" and distance_laser2 < 27:
        return True
    else:
        return False


#Function that displays the Score
def show_score(x,y):
    score_show = font.render("Score : " + str(score), True, (255, 255, 255))
    screen.blit(score_show, (x, y))


#Function that displays the text GAME OVER
def game_over_text(x, y):
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    x = 200
    y = 250
    screen.blit(over_text, (x, y))


#Class to define or Health bar
class HealthBar():
    def __init__(self, x, y, w, h, max_hp):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.hp = max_hp
        self.max_hp = max_hp

    def draw(self, surface):
        #calculate health ratio
        ratio = self.hp / self.max_hp
        pygame.draw.rect(surface, "red", (self.x, self.y, self.w, self.h))
        pygame.draw.rect(surface, "green", (self.x, self.y, self.w * ratio, self.h))

