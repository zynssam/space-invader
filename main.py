from random import randint
from math import sqrt, pow

import pygame
from pygame import mixer

# Initializing Pygame
pygame.init()

# Creating The Screen
screen = pygame.display.set_mode((800, 600),  pygame.NOFRAME)#Removes the Top Frame. You can add it if you want the quit sign

# Background
background = pygame.image.load('_internal/background.jpg')

#Background Music 
mixer.music.load('_internal/background.wav')
mixer.music.play(-1)

# Title and Icon
pygame.display.set_caption("Space Invader") #Title of the window
pygame.display.set_icon(pygame.image.load("_internal/space-ship.png")) # Title Icon

# Player
playerimg = pygame.image.load('_internal/mainship.png')
playerX = 370
playerY = 480
playerX_change = 0

# Enemy
enemyimg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
noofenemies = 5
for i in range(noofenemies):
    enemyimg.append(pygame.image.load('_internal/enemy.png'))
    enemyX.append(randint(64, 734))
    enemyY.append(randint(50, 150))
    enemyX_change.append(0.5)
    enemyY_change.append(10)

# Bullet
bulletimg = pygame.image.load('_internal/bullet.png')
bulletX = 0
bulletY = 480
bulletY_change = 2
bullet_state = 'ready'

# SCORE
score_value = 0 
font = pygame.font.Font('freesansbold.ttf', 32)
font1 = pygame.font.Font('freesansbold.ttf', 64)

#Score Coordinates
textX = 10
textY = 10

def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

def gameover_text(x, y):
    over_text = font1.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (x, y))

def player(x, y):
    screen.blit(playerimg, (x, y))

def enemy(x, y, i):
    screen.blit(enemyimg[i], (x, y))

def fire_bullet(x, y):
    global bullet_state
    bullet_state = 'fire'
    screen.blit(bulletimg, (x + 16, y + 10))

def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = sqrt(pow(enemyX - bulletX, 2) + pow(enemyY - bulletY, 2))
    return distance < 27

def game_over_screen():
    while True:
        screen.fill((0, 0, 0))
        over_text = font1.render("GAME OVER", True, (255, 255, 255))
        restart_text = font.render("Press R to Restart or Q to Quit", True, (255, 255, 255))
        screen.blit(over_text, (800 // 2 - 200, 600 // 2 - 50))
        screen.blit(restart_text, (800 // 2 - 240, 600 // 2 + 10))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    reset_game()  # Reset game state
                    return  # Exit the game over screen
                if event.key == pygame.K_q:
                    pygame.quit()
                    return

#To restart the game
def reset_game():
    global playerX, playerY, playerX_change, bullet_state
    global bulletX, bulletY, score_value, enemyX, enemyY
    playerX = 370
    playerY = 480
    playerX_change = 0
    bullet_state = 'ready'
    bulletY = 480
    score_value = 0
    for i in range(noofenemies):
        enemyX[i] = randint(64, 734)
        enemyY[i] = randint(50, 150)
    game_loop()

# Game Loop
running = True

def game_loop():
    global running, playerX, playerY, playerX_change, bullet_state
    global bulletX, bulletY, bulletY_change, noofenemies
    global enemyX, enemyY, enemyX_change, enemyY_change
    global score_value, textX, textY

    while running:

        # Background
        screen.blit(background, (0, 0))  # Draw the background image

        #Key Input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    playerX_change -= 0.3
                if event.key == pygame.K_RIGHT:
                    playerX_change += 0.3
                if event.key == pygame.K_SPACE and bullet_state == 'ready':
                    bulletX = playerX
                    bullet_sound = mixer.Sound('_internal/bullet.wav')
                    bullet_sound.play()
                    fire_bullet(bulletX, bulletY)

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    playerX_change = 0

        # Player Movement
        playerX += playerX_change
        if playerX <= 64:
            playerX = 64
        elif playerX >= 734:
            playerX = 734

        # Enemy Movement
        for i in range(noofenemies):
            if enemyY[i] > 460:
                game_over_sound = mixer.Sound('_internal/gameover.wav')
                game_over_sound.play()
                game_over_screen()  # Handle game over
                return  # Exit the game loop
            enemyX[i] += enemyX_change[i]
            if enemyX[i] <= 64:
                enemyX_change[i] += 0.1
                enemyY[i] += enemyY_change[i]
            elif enemyX[i] >= 734:
                enemyX_change[i] -= 0.1
                enemyY[i] += enemyY_change[i]

            # Collision
            collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
            if collision:
                collision_sound=mixer.Sound('_internal/collision.wav')
                collision_sound.play()
                bulletY = 480
                bullet_state = 'ready'
                score_value += 1
                enemyX[i] = randint(64, 734)
                enemyY[i] = randint(50, 150)
            enemy(enemyX[i], enemyY[i], i)

        # Bullet Movement
        if bullet_state == 'fire':
            fire_bullet(bulletX, bulletY)
            bulletY -= bulletY_change
            if bulletY <= 0:
                bulletY = 480
                bullet_state = 'ready'

        player(playerX, playerY)#Displays Player
        show_score(textX, textY)#Displays Score

        pygame.display.update()#Updates the display


# Start the game loop
game_loop()