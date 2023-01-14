import pygame, sys, random, threading, time
from pygame.locals import *

player_score = 0
opponent_score = 0
GREEN = (150, 255, 150)

def ball_animation():
    global ball_speed_x, ball_speed_y
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    if ball.top <= 0 or ball.bottom >= screen_height:
        ball_speed_y *= -1
    if ball.left <= 0 or ball.right >= screen_width:
        ball_speed_x *= -1

    if ball.colliderect(player) or ball.colliderect(opponent):
        ball_speed_x *= -1

def ball_restart():
    global ball_speed_x, ball_speed_y, opponent_speed, pbcollide, obcollide
    ball.center = (screen_width/2, screen_height/2)
    ball_speed_x *= random.choice((-1, 1))
    ball_speed_y *= random.choice((-1, 1))
    pbcollide = 0
    obcollide = 0

    if player_score % 2 == 0 and player_score != 0:
        ball_speed_x += 1
        ball_speed_y += 0.5
        opponent_speed += 1

def player_animation():
    player.y += player_speed
    if player.top <= 0:
        player.top = 0
    if player.bottom >= screen_height:
        player.bottom = screen_height

def opponent_animation():
    if opponent.y == ball.y:
        opponent.y == 0
    elif opponent.top > ball.y:
        opponent.top -= opponent_speed
    elif opponent.bottom < ball.y:
        opponent.bottom += opponent_speed
    elif opponent.bottom <= 0:
        opponent.bottom = 0
    elif opponent.top >= screen_height:
        opponent.top = screen_height

def score():
    global player_score, opponent_score
    if ball.left <= 0:
        if obcollide >= 1:
            opponent_score += 1
            ball_restart()
        else:
            opponent_score += 0
            screen.blit(text, (screen_width / 2, 20))
            pygame.time.wait(2000)


    elif ball.right >= screen_width:
        if pbcollide >= 1:
            player_score += 1
            ball_restart()
        else:
            player_score += 0
            screen.blit(text, (screen_width / 2, 20))
            pygame.time.wait(2000)

def collision_count():
    global obcollide, pbcollide
    if ball.colliderect(opponent):
        obcollide += 1
    if ball.colliderect(player):
        pbcollide += 1

# Setup
pygame.init()
clock = pygame.time.Clock()

# Making the screen
screen_width = 1120
screen_height = 640
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Game')

# Creating font
font = pygame.font.Font(None, 36)
text = font.render("Unfair start detected, the opposing player is protected from a goal.", True, (100, 255, 100))

# Rectangles
ball = pygame.Rect(screen_width/2 - 15, screen_height/2 - 15, 30, 30)
opponent = pygame.Rect(screen_width - 20, screen_height/2 - 70, 10, 140)
player = pygame.Rect(10, screen_height/2 - 70, 10, 140)

bg_color = pygame.Color('grey12')
grn = (150, 255, 150)

ball_speed_x = 7 * random.choice((-1,1))
ball_speed_y = 7 * random.choice((-1,1))
player_speed = 0
opponent_speed = 2
player_score = 0
opponent_score = 0
pbcollide = 1
obcollide = 1

while True:
    # Input handling
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                player_speed += 7
            elif event.key == pygame.K_UP:
                player_speed -= 7

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                player_speed -= 7
            elif event.key == pygame.K_UP:
                player_speed += 7

    ball_animation()
    player_animation()
    opponent_animation()
    score()
    collision_count()
    player_score_text = font.render(str(player_score), True, (100, 255, 100))
    opponent_score_text = font.render(str(opponent_score), True, (100, 255, 100))

    # Visuals
    screen.fill(bg_color)
    pygame.draw.rect(screen, grn, opponent)
    pygame.draw.rect(screen, grn, player)
    pygame.draw.ellipse(screen, grn, ball)
    pygame.draw.aaline(screen, grn, (screen_width/2, 0), (screen_width/2, screen_height))
    screen.blit(player_score_text, (400, 20))
    screen.blit(opponent_score_text, (720, 20))

    # Updating the window

    pygame.display.update()
    clock.tick(60)
