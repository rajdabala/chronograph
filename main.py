import math, os
import pygame, random
import enemy, coin
from pygame.locals import *

pygame.init()
pygame.font.init()

screen = pygame.display.set_mode((1000, 800), pygame.NOFRAME)  # SCREEN SIZE
pygame.display.set_caption("chronograph")

SCREEN_WIDTH = screen.get_width()
SCREEN_HEIGHT = screen.get_height()

# fonts
font = pygame.font.Font(os.path.join('apple.ttf'), 16)
big_font = pygame.font.Font(os.path.join('apple.ttf'), 36)
title_font = pygame.font.Font(os.path.join('apple.ttf'), 50)

# ASCII representations
player_text = font.render("o", True, (255, 255, 255))
boom_text = font.render("v", True, (255, 255, 255))

numEnemies = 7
numCoins = 7

# make enemy array
enemies = []
for i in range(0, numEnemies):
    enemies.append(enemy.Enemy())

# make coin array
coins = []
for i in range(0, numCoins):
    coins.append(coin.Coin())

# boomerang setup
boom_v = 5
boom_theta = 0
boomthrown = False
boomreturn = False

# text and titles
title_text = title_font.render("chronograph", True, (0, 255, 0))
title_rect = title_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 250))

begin_text = big_font.render("F to begin tutorial", True, (255, 255, 255))
begin_rect = begin_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))

tut1_text = font.render("welcome to chronograph! use WASD to move around, and click to shoot your boomerang.", True, (255, 255, 255))
tut1_rect = tut1_text.get_rect(center=(SCREEN_WIDTH / 2, 50))

tut2_text = font.render("you are fighting the colors. you can stun them with your boomerang.", True, (255, 255, 255))
tut2_rect = tut1_text.get_rect(center=(SCREEN_WIDTH / 2, 125))

tut3_text = font.render("try to collect the coins before dying. good luck!", True, (255, 255, 255))
tut3_rect = tut1_text.get_rect(center=(SCREEN_WIDTH / 2, 200))

paused_text = big_font.render("P to resume", True, (255, 255, 255))
paused_rect = paused_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))

end_text = big_font.render("GAME OVER", True, (255, 255, 255))
end_rect = end_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))

win_text = big_font.render("YOU WIN", True, (0, 255, 0))
win_rect = win_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 50))

lose_text = big_font.render("YOU LOSE", True, (255, 0, 0))
lose_rect = lose_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 50))

# cursor setup
pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_CROSSHAIR)

# initialize clock for framerate
clock = pygame.time.Clock()

# gamestates
mainmenu = True
running = False
paused = False
gameover = False
won = False
lost = False

# initialize clock for timer
timer = pygame.time.Clock()
time = 120.0 # starting time
slowmult = 1 # slow motion time multiplier

# game parameters
lives = 3

# create PLAYER vector and place in center
player_pos = pygame.Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

# create BOOMERANG vector
boom_pos = pygame.Vector2(player_pos.x, player_pos.y)

# main menu
while mainmenu:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    screen.blit(pygame.image.load("mainmenu_bg.png"), (0, 0))

    screen.blit(title_text, title_rect)

    screen.blit(begin_text, begin_rect)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_f]:
        mainmenu = False
        running = True
    if keys[pygame.K_ESCAPE]:
        raise SystemExit()

    pygame.display.flip()

# main game
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    lives_text = font.render("LIVES: " + str(lives), True, "white")
    coins_text = font.render("COINS REMAINING: " + str(numCoins), True, "white")

    # background color
    screen.fill("black")

    # draw LIVES and COINS
    screen.blit(lives_text, (0, 0))
    screen.blit(coins_text, (0, 20))

    # tutorial text
    if clock.get_rawtime() < 5000:
        screen.blit(tut1_text, tut1_rect)
        screen.blit(tut2_text, tut2_rect)
        screen.blit(tut3_text, tut3_rect)

    # draw PLAYER
    screen.blit(player_text, player_pos)

    # draw BOOMERANG
    if boomthrown:
        screen.blit(boom_text, boom_pos)

    # draw ENEMIES
    for i in range(0, len(enemies)):
        if enemies[i].alive == True:
            screen.blit(enemies[i].text, enemies[i].pos)
        else:
            screen.blit(enemies[i].stun_text, enemies[i].stun_pos)

    for i in range(0, len(coins)):
        if not coins[i].collected:
            screen.blit(coins[i].text, coins[i].pos)

    # set KEY BINDINGS
    isMoving = False
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        player_pos.y -= 100 * dt
        isMoving = True
    if keys[pygame.K_a]:
        player_pos.x -= 100 * dt
        isMoving = True
    if keys[pygame.K_s]:
        player_pos.y += 100 * dt
        isMoving = True
    if keys[pygame.K_d]:
        player_pos.x += 100 * dt
        isMoving = True
    if keys[pygame.K_p]:
        paused = True
        running = False
    if keys[pygame.K_ESCAPE]:
        raise SystemExit()
    
    # hit reg
    for i in range(0, len(enemies)):
        if player_pos.distance_to(enemies[i].pos) <= 10 and enemies[i].alive:
            if lives == 1:
                gameover = True
                lost = True
                running = False
            else:
                lives -= 1
                player_pos.x = random.randint(0, SCREEN_WIDTH)
                player_pos.y = random.randint(0, SCREEN_HEIGHT)

    # check if all coins collected
    if numCoins == 0:
        running = False
        gameover = True
        won = True

    # coin collection
    for i in range(0, len(coins)):
        if player_pos.distance_to(coins[i].pos) <= 10 and not coins[i].collected:
            coins[i].collect(True)
            numCoins -= 1
            
    # slowmo multiplier
    if isMoving:
        slowmult = 1
    else:
        slowmult = 0.25

    # boomerang logic
    if boomthrown:
        if boomreturn:
            boom_pos += boom_v * (player_pos - boom_pos).normalize() * slowmult
        else:
            dx = boom_v * math.cos(math.radians(boom_theta))
            dy = boom_v * math.sin(math.radians(boom_theta))
            boom_pos[0] += dx * slowmult
            boom_pos[1] += dy * slowmult

        if (boom_pos[0] < 0 or boom_pos[0] > SCREEN_WIDTH or
                boom_pos[1] < 0 or boom_pos[1] > SCREEN_HEIGHT):
            boomthrown = False

        if boom_pos.distance_to(boom_dest) <= 5:
            boomreturn = True
        
        if boomreturn and boom_pos.distance_to(boom_origin) <= 5:
            boom_v = 0

        if boomreturn and boom_pos.distance_to(player_pos) <= 10:
            boomreturn = False
            boomthrown = False

        # enemy hit reg
        for i in range(0, len(enemies)):
            if enemies[i].alive and boom_pos.distance_to(enemies[i].pos) <= 15:
                boomreturn = True
                enemies[i].set_alive(False)
                enemies[i].set_stun_pos(enemies[i].pos.x, enemies[i].pos.y)
                enemies[i].set_stun_start(pygame.time.get_ticks())

    # enemy actions
    for i in range(0, len(enemies)):
        if enemies[i].alive == False:
            if pygame.time.get_ticks() - enemies[i].stun_start >= enemies[i].stun_time:
                enemies[i].set_alive(True)
                enemies[i].pos.x = enemies[i].stun_pos[0]
                enemies[i].pos.y = enemies[i].stun_pos[1]

    # enemy movement
    for i in range(0, len(enemies)):
        enemies[i].pos += (player_pos - enemies[i].pos).normalize() * slowmult * enemies[i].speed

    # coin movement
    for i in range(0, len(coins)):
        if coins[i].pos.x <= SCREEN_WIDTH and coins[i].pos.x >= 0 and coins[i].pos.y <= SCREEN_HEIGHT and coins[i].pos.y >= 0:
            coins[i].pos.x += random.randint(-5, 5)
            coins[i].pos.y += random.randint(-5, 5)
        else:
            coins[i].pos = coins[i].pos.reflect(coins[i].pos)

    # timer
    t_show = font.render(str(int(time)), True, (255, 255, 255))
    screen.blit(t_show, (screen.get_width() / 2, 25))
    time -= slowmult * (timer.tick() / 1000)

    # push display to screen
    pygame.display.flip()

    # shoot on mouse click
    if pygame.mouse.get_pressed()[0] and not boomthrown:
        boomthrown = True
        boom_v = 5
        mouse_x, mouse_y = pygame.mouse.get_pos()
        boom_pos.x = player_pos.x
        boom_pos.y = player_pos.y
        dx = mouse_x - player_pos[0]
        dy = mouse_y - player_pos[1]
        boom_theta = math.degrees(math.atan2(dy, dx))
        boom_dest = (mouse_x, mouse_y)
        boom_origin = (player_pos.x, player_pos.y)

    # run clock (FPS)
    dt = clock.tick(60) / 1000  # set PSM based on FPS

# paused menu NEEDS WORK
while paused:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    screen.blit(pygame.image.load("mainmenu_bg.png"), (0, 0))

    screen.blit(paused_text, paused_rect)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_p]:
        running = True
        paused = False
    if keys[pygame.K_ESCAPE]:
        raise SystemExit()
    
    pygame.display.flip()

# game over screen
while gameover:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    screen.fill("black")

    screen.blit(end_text, end_rect)

    if won:
        screen.blit(win_text, win_rect)
    if lost:
        screen.blit(lose_text, lose_rect)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        raise SystemExit()

    pygame.display.flip()

pygame.quit()