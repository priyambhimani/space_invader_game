import pygame
import random
import math as m

# Initialize pygame
pygame.init()

back = pygame.image.load('background.png')
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Space Battle")
icon = pygame.image.load('spacegame_logo.png')
pygame.display.set_icon(icon)

# Player Space ship
playerImg = pygame.image.load('spaceship.png')
playerX = 370
playerY = 480
playerX_change = 0

# Enemy Spaceship
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
enemy_bullets = []
num_of_enemy = 3


# Enemy Bullet Class
class enemy_bullet:

    def __init__(self, enemyX, enemyY):
        self.x = enemyX
        self.y = enemyY
        self.y_change = 1.5
        self.enemy_bullet_state = 'ready'


def is_Bullet_Passed(bulletY):
    if bulletY >= 600:
        return True

for i in range(num_of_enemy):
    enemyImg.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(49, 751))
    enemyY.append(50)
    enemyX_change.append(3)
    enemyY_change.append(40)
    new_enemy_bullet = enemy_bullet(enemyX[i],enemyY[i])
    enemy_bullets.append(new_enemy_bullet)

# Bullet If ready then invisible and fire then fired
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 2
bullet_state = "ready"

enemyBulletImg = pygame.image.load('bullet_inverted.png')

# Score
score = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textx = 10
texty = 10

over = pygame.font.Font('freesansbold.ttf', 64)
overx = 200
overy = 50


def show_score(x, y):
    sc = font.render("Score: " + str(score), True, (255, 255, 255))
    screen.blit(sc, (x, y))


def game_over(x, y):
    go = over.render("GAME OVER", True, (255, 255, 255))
    screen.blit(go, (x, y))


def printing_image(x, y, image):
    screen.blit(image, (x, y))


def bullet_fire(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))

def bullet_fire_enemy(x, y):
    screen.blit(bulletImg,(x, y))

def isCollision(enemyX, enemyY, bullX, bullY):
    d = m.sqrt(m.pow(enemyX - bullX, 2) + m.pow(enemyY - bullY, 2))
    if d <= 27:
        return True
    else:
        return False


running = True

while running:
    screen.fill((0, 0, 0))
    screen.blit(back, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print(score)
            running = False

        # Detecting any key for left or right is pressed or not
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -3
            if event.key == pygame.K_RIGHT:
                playerX_change = 3
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bulletX = playerX
                    bullet_fire(playerX, bulletY)

        if (event.type == pygame.KEYUP):
            if event.key == pygame.K_LEFT:
                playerX_change = 0
            if event.key == pygame.K_RIGHT:
                playerX_change = 0

    # Checking for boundaries
    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 751:
        playerX = 751

    for i in range(num_of_enemy):

        if enemyY[i] >= 400:
            for j in range(num_of_enemy):
                enemyX[j] = 2000
                enemyY[j] = 2000
            game_over(overx, overy)
            break

        if enemy_bullets[i].enemy_bullet_state == 'ready':
            enemy_bullets[i].enemy_bullet_state = 'fire'

        elif enemy_bullets[i].enemy_bullet_state == 'fire':
            bullet_fire_enemy(enemy_bullets[i].x, enemy_bullets[i].y)
            enemy_bullets[i].y += enemy_bullets[i].y_change

        if isCollision(playerX,playerY,enemy_bullets[i].x,enemy_bullets[i].y):
            for j in range(num_of_enemy):
                enemyX[j] = 2000
                enemyY[j] = 2000
            game_over(overx, overy)
            break

        if is_Bullet_Passed(enemy_bullets[i].y):
            enemy_bullets[i].x = enemyX[i]
            enemy_bullets[i].y = enemyY[i]
            enemy_bullets[i].enemy_bullet_state = 'ready'

        enemyX[i] = enemyX[i] + enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 2
            enemyX[i] = 0
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 751:
            enemyX_change[i] = -2
            enemyX[i] = 751
            enemyY[i] += enemyY_change[i]

        if isCollision(enemyX[i], enemyY[i], bulletX, bulletY):
            bulletY = 480
            enemyX[i] = random.randint(49, 751)
            enemyY[i] = random.randint(49, 250)
            bullet_state = "ready"
            score += 1

    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state == "fire":
        bullet_fire(bulletX, bulletY)
        bulletY = bulletY - bulletY_change

    printing_image(playerX, playerY, playerImg)
    for i in range(num_of_enemy):
        printing_image(enemyX[i], enemyY[i], enemyImg[i])
        printing_image(enemy_bullets[i].x, enemy_bullets[i].y, enemyBulletImg)
    show_score(textx, texty)
    pygame.display.update()

