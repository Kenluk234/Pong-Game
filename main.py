import pygame, sys, random, threading, time
from pygame.locals import *

# Color Scheme
GREEN = (150, 255, 150)

def ball_animation():
    # Ball Movement
    global ball_speed_x, ball_speed_y
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    # Ball bounces vertically or horizontally upon edge collision
    if ball.top <= 0 or ball.bottom >= screen_height:
        ball_speed_y *= -1
    if ball.left <= 0 or ball.right >= screen_width:
        ball_speed_x *= -1

    # Ball bounces back horizontally upon paddle collision
    if ball.colliderect(player) or ball.colliderect(opponent):
        ball_speed_x *= -1

def ball_restart():
    global ball_speed_x, ball_speed_y, opponent_speed, pbcollide, obcollide, speedlist
    # Ball movement randomizer factor
    speedlistx = [-1, 1]
    speedlisty = [-1.5, -1.25, 1.25, 1.5]
    pygame.time.wait(1000)

    # Ball position reset
    ball.center = (screen_width/2, screen_height/2)

    # Ball movement initializing and randomizer
    ball_speed_x = 7
    ball_speed_y = 7
    ball_speed_x *= random.choice(speedlistx)
    ball_speed_y *= random.choice(speedlisty)
    player.y = screen_height/2
    opponent.y = screen_height/2

    # Detect number of collision to disqualify unfair circumstances
    pbcollide = 0
    obcollide = 0

    # When player scores more, ball and opponent gets faster
    if player_score % 2 == 0 and player_score != 0:
        for n in speedlistx:
            ball_speed_x += 0.5
            n += 0.5

        if opponent_speed <= 7:
            opponent_speed += 0.5
        else:
            opponent_speed = 7

def even_speed_cond():
    # If opponent is too fast to beat, game instantly skips to a manageable difficulty
    if opponent_speed >= ball_speed_y and abs(ball_speed_y) < 1:
        ball_restart()

def player_animation():
    # Player movement
    player.y += player_speed

    # Player's paddle stops when paddle reaches edge
    if player.top <= 0:
        player.top = 0
    if player.bottom >= screen_height:
        player.bottom = screen_height

def opponent_animation():
    # Opponent's AI
    if opponent.top > ball.centery:
        opponent.top -= opponent_speed
    elif opponent.bottom < ball.centery:
        opponent.bottom += opponent_speed

    # Opponent's paddle stops when paddle reaches edge
    elif opponent.top <= 0:
        opponent.top = 0
    elif opponent.bottom >= screen_height:
        opponent.bottom = screen_height

def score():
    global player_score, opponent_score
    # If ball touches left edge, and opponent collided with ball before, opponent scores a point, else opponent's score is invalid
    if ball.left <= 0:
        if obcollide >= 1:
            opponent_score += 1
            ball_restart()
        else:
            opponent_score += 0
            ball_restart()

    # If ball touches right edge, and player collided with ball before, player scores a point, else player's score is invalid
    elif ball.right >= screen_width:
        if pbcollide >= 1:
            player_score += 1
            ball_restart()
        else:
            player_score += 0
            ball_restart()

def collision_count():
    # Track ball-opponent and ball-player collision
    global obcollide, pbcollide
    if ball.colliderect(opponent):
        obcollide += 1
    if ball.colliderect(player):
        pbcollide += 1

def checkfinal():
    global player_score, opponent_score, state

    # If player gets 10 points, player gets victory message
    if player_score >= 10:
        playerwins = font.render("You win!", True, GREEN)
        screen.blit(playerwins, ((screen_width/2), (screen_height/2)))
        pygame.display.update()
        pygame.time.wait(1000)
        if state == "game_screen":
            state = "main_menu"
        player_score = 0

    # If opponent gets 10 points, player gets defeat (opponent's victory) message
    elif opponent_score >= 10:
        opponentwins = font.render("Opponent wins! You lose!", True, GREEN)
        screen.blit(opponentwins, ((screen_width / 2), (screen_height / 2)))
        pygame.display.update()
        pygame.time.wait(1000)
        if state == "game_screen":
            state = "main_menu"
        opponent_score = 0

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

# Rectangles
ball = pygame.Rect(screen_width/2 - 15, screen_height/2 - 15, 30, 30)
opponent = pygame.Rect(screen_width - 20, screen_height/2 - 70, 10, 140)
player = pygame.Rect(20, screen_height/2 - 70, 10, 140)

# Background color
bg_color = pygame.Color('grey12')

# Mechanical value initialization for the 1st round
ball_speed_x = 7 * random.choice([-1, -0.75, 0.75, 1])
ball_speed_y = 7 * random.choice([-1.25, -1, 1,1.25])
player_speed = 0
opponent_speed = 5
player_score = 0
opponent_score = 0
pbcollide = 0
obcollide = 0

# Main menu state
state = "main_menu"

running = True
while running:
        # Main menu
        if state == "main_menu":
            title = font.render("PONG", True, GREEN)
            selection = font.render("""
            A. Play
            X. Exit
            """, True, GREEN)
            screen.blit(title, (screen_width/2, 20))
            screen.blit(selection, (screen_width/2, 100))

            keys = pygame.key.get_pressed()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                elif event.type == pygame.KEYDOWN:

                    # If A key pressed, game starts
                    if event.key == pygame.K_a:
                        pygame.time.wait(1000)
                        if state == "main_menu":
                            state = "game_screen"
                    # If X key pressed, game starts
                    if event.key == pygame.K_x:
                        pygame.quit()
                        sys.exit()

            # Updating the window
            pygame.display.update()
            clock.tick(90)

        # Game screen
        elif state == "game_screen":
            keys = pygame.key.get_pressed()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # Move up and down
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        player_speed += 7
                    elif event.key == pygame.K_UP:
                        player_speed -= 7

                # Key release
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_DOWN:
                        player_speed -= 7
                    elif event.key == pygame.K_UP:
                        player_speed += 7

            # Game Mechanics
            ball_animation()
            player_animation()
            opponent_animation()
            score()
            collision_count()
            even_speed_cond()
            checkfinal()
            player_score_text = font.render(str(player_score), True, GREEN)
            opponent_score_text = font.render(str(opponent_score), True, GREEN)

            # Visuals
            screen.fill(bg_color)
            pygame.draw.rect(screen, GREEN, opponent)
            pygame.draw.rect(screen, GREEN, player)
            pygame.draw.ellipse(screen, GREEN, ball)
            pygame.draw.aaline(screen, GREEN, (screen_width/2, 0), (screen_width/2, screen_height))
            screen.blit(player_score_text, (400, 20))
            screen.blit(opponent_score_text, (720, 20))

            # Updating the window
            pygame.display.update()
            clock.tick(60)

