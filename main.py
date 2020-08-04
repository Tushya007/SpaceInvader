import pygame
import random
import math
from pygame import mixer

# initialize the pygame
pygame.init()

# screen
screen = pygame.display.set_mode((800, 600))

# background
background = pygame.image.load('bg.jpg')

# music
mixer.music.load('background.wav')
mixer.music.play(-1)

# title and icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('spaceship.png')
pygame.display.set_icon(icon)

# score
score_value = 0
font = pygame.font.Font('Headcorps.ttf', 25)
tentX = 10
textY = 10

# game over
over = pygame.font.Font('Headcorps.ttf', 64)


def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (0, 0, 0))
    screen.blit(score, (x, y))


def game_over_text(x, y):
    game_over = over.render("Game Over", True, (255, 255, 255))
    screen.blit(game_over, (x, y))


def you_won(x, y):
    win = over.render("YOU WON!", True, (255, 255, 255))
    screen.blit(win, (x, y))


# bullet
bullet = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 3
bullet_state = 'ready'
# bullet not on screen

# player
player_image = pygame.image.load('ship.png')
PlayerX = 370
PlayerY = 480
playerX_change = 0

enemy_image = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemy = 6

# enemy
for i in range(num_of_enemy):
    enemy_image.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(50, 200))
    enemyX_change.append(1)
    enemyY_change.append(40)


def enemy(x, y, i):
    screen.blit(enemy_image[i], (x, y))


def player(x, y):
    screen.blit(player_image, (x, y))


def bullet_shot(x, y):
    global bullet_state
    bullet_state = 'fire'
    screen.blit(bullet, (x + 16, y + 10))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Player movement
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -2
            elif event.key == pygame.K_RIGHT:
                playerX_change = 2
            if event.key == pygame.K_SPACE:
                bullet_sound = mixer.Sound("laser.wav")
                bullet_sound.play()
                if bullet_state is 'ready':
                    bulletX = PlayerX
                    bullet_shot(bulletX, bulletY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # bg colour
    screen.fill((0, 150, 0))
    screen.blit(background, (0, 0))

    PlayerX += playerX_change

    # boundary of player
    if PlayerX <= 0:
        PlayerX = 0
    elif PlayerX >= 736:
        PlayerX = 736

    # bullet movement
    if bullet_state is 'fire':
        bullet_shot(bulletX, bulletY)
        bulletY -= bulletY_change

    # bullet reset
    if bulletY <= 0:
        bullet_state = 'ready'
        bulletY = 480

    # boundary of enemy
    for i in range(num_of_enemy):

        # game over
        if enemyY[i] > 440 or score_value == 20:
            for j in range(num_of_enemy):
                enemyY[j] = 2000
            game_over_text(240, 250)
            if score_value == 20:
                you_won(255, 300)
        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 1
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -1
            enemyY[i] += enemyY_change[i]

        # collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            bulletY = 480
            bullet_state = 'ready'
            score_value += 1
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(50, 200)
            collision_sound = mixer.Sound('explosion.wav')
            collision_sound.play()

        enemy(enemyX[i], enemyY[i], i)
    player(PlayerX, PlayerY)
    show_score(tentX, textY)
    pygame.display.update()