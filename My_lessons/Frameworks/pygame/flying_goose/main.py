import random
import pygame
from pygame.constants import QUIT, KEYDOWN, K_DOWN, K_UP, K_LEFT, K_RIGHT

pygame.init()

FPS = pygame.time.Clock()

HEIGHT = 800
WIDTH = 1200

FONT = pygame.font.SysFont('Verdana', 20)

COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_BLUE = (0, 0, 255)
COLOR_YELLOW = (255, 255, 0)

main_display = pygame.display.set_mode((WIDTH, HEIGHT))

bg = pygame.transform.scale(pygame.image.load('drawable/background.png'), (WIDTH, HEIGHT))
bgX1 = 0
bgX2 = bg.get_width()
bg_move = 3

player_animations = [pygame.image.load(f'drawable/player/1-{i}.png') for i in range(1, 5)]
current_frame = 0
player_rect = player_animations[current_frame].get_rect(topleft=(100, 400))
player_move_down = [0, 4]
player_move_right = [4, 0]
player_move_up = [0, -4]
player_move_left = [-4, 0]

frame_change_delay = 100
last_frame_change_time = pygame.time.get_ticks()

def create_enemy():
    enemy = pygame.image.load('drawable/enemy.png')
    enemy_size = enemy.get_size()
    enemy_rect = pygame.Rect(WIDTH, random.randint(0, HEIGHT), *enemy_size)
    enemy_move = [random.randint(-8, -4), 0]
    return [enemy, enemy_rect, enemy_move]

CREATE_ENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(CREATE_ENEMY, 1500)
enemies = []

def create_bonus():
    bonus = pygame.image.load('drawable/bonus.png')
    bonus_size = bonus.get_size()
    bonus_rect = pygame.Rect(random.randint(0, WIDTH), 0, *bonus_size)
    bonus_move = [0, random.randint(4, 8)]
    return [bonus, bonus_rect, bonus_move]

CREATE_BONUS = pygame.USEREVENT + 1
pygame.time.set_timer(CREATE_BONUS, 1500)
bonuses = []

score = 0
playing = True

while playing:
    FPS.tick(144)

    for event in pygame.event.get():
        if event.type == QUIT:
            playing = False
        if event.type == CREATE_ENEMY:
            enemies.append(create_enemy())
        if event.type == CREATE_BONUS:
            bonuses.append(create_bonus())

    bgX1 -= bg_move
    bgX2 -= bg_move

    main_display.blit(bg, (bgX1, 0))
    main_display.blit(bg, (bgX2, 0))

    if bgX1 < -bg.get_width():
        bgX1 = bg.get_width()

    if bgX2 < -bg.get_width():
        bgX2 = bg.get_width()

    keys = pygame.key.get_pressed()

    if keys[K_DOWN] and player_rect.bottom < HEIGHT:
        player_rect = player_rect.move(player_move_down)
    elif keys[K_RIGHT] and player_rect.right < WIDTH:
        player_rect = player_rect.move(player_move_right)
    elif keys[K_UP] and player_rect.top > 0:
        player_rect = player_rect.move(player_move_up)
    elif keys[K_LEFT] and player_rect.left > 0:
        player_rect = player_rect.move(player_move_left)

    current_time = pygame.time.get_ticks()
    if current_time - last_frame_change_time >= frame_change_delay:
        current_frame = (current_frame + 1) % len(player_animations)
        last_frame_change_time = current_time

    for enemy in enemies:
        enemy[1] = enemy[1].move(enemy[2])
        main_display.blit(enemy[0], enemy[1])

        if player_rect.colliderect(enemy[1]):
            playing = False

    for bonus in bonuses:
        bonus[1] = bonus[1].move(bonus[2])
        main_display.blit(bonus[0], bonus[1])

        if player_rect.colliderect(bonus[1]):
            score += 1
            bonuses.pop(bonuses.index(bonus))

    main_display.blit(FONT.render(str(score), True, COLOR_BLACK), (WIDTH - 50, 20))
    main_display.blit(player_animations[current_frame], player_rect)

    pygame.display.flip()

    for enemy in enemies:
        if enemy[1].left < 0:
            enemies.pop(enemies.index(enemy))

    for bonus in bonuses:
        if bonus[1].bottom > HEIGHT:
            bonuses.pop(bonuses.index(bonus))
