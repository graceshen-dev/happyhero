"""Dino Game in Python

A game similar to the famous Chrome Dino Game, built using pygame-ce.
Made by intern: @bassemfarid, no one or nothing else. 🤖
"""

import pygame
import random #do i need to just import randint

def display_score():
    current_time = int(pygame.time.get_ticks()/1000) - start_time
    score_surf = game_font.render(f"Score: {current_time}", False, (64, 64, 64))
    score_rect = score_surf.get_rect(center = (400, 50))
    screen.blit(score_surf, score_rect)
    return current_time

# Initialize Pygame and create a window
pygame.init()
start_time = 0
screen = pygame.display.set_mode((800, 400))
clock = pygame.time.Clock()
running = True  # Pygame main loop, kills pygame when False
score = 0

# Game state variables
is_playing = True  # Whether in game or in menu
GROUND_Y = 300  # The Y-coordinate of the ground level
JUMP_GRAVITY_START_SPEED = -20  # The speed at which the player jumps
players_gravity_speed = 0  # The current speed at which the player falls

# Load level assets
SKY_SURF = pygame.image.load("graphics/level/sky.png").convert()
GROUND_SURF = pygame.image.load("graphics/level/ground.png").convert()
# license: httpsL//
game_font = pygame.font.Font(pygame.font.get_default_font(), 50)

# Load sprite assets
player_surf = pygame.image.load("graphics/player/player_walk_1.png").convert_alpha()
player_rect = player_surf.get_rect(bottomleft=(25, GROUND_Y))
egg_surf = pygame.image.load("graphics/egg/egg_1.png").convert_alpha()
egg_rect = egg_surf.get_rect(bottomleft=(800, GROUND_Y))

starting_icon = pygame.image.load("graphics/player/player_walk_1.png").convert_alpha()
starting_icon = pygame.transform.rotozoom(starting_icon, 0, 2)
starting_icon_rect = starting_icon.get_rect(center=(400, 200))

#text
game_name = game_font.render("MY GAMEEEE", False, (11, 196, 169))
game_name_rect = game_name.get_rect(center = (400, 80))

game_message = game_font.render("Press space to go", False, (11, 196, 169))
game_message_rect = game_message.get_rect(center = (400, 350))

enemy_rect_list = []

#timer
obs_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obs_timer, 900)

while running:
    # Poll for events
    for event in pygame.event.get():
        # pygame.QUIT --> user clicked X to close your window
        if event.type == pygame.QUIT:
            running = False

        elif is_playing:
            # When player wants to jump by pressing SPACE
            if (
                event.type == pygame.KEYDOWN
                and event.key == pygame.K_SPACE
                or event.type == pygame.MOUSEBUTTONDOWN
            ) and player_rect.bottom >= GROUND_Y:
                players_gravity_speed = JUMP_GRAVITY_START_SPEED
        else:
            # When player wants to play again by pressing SPACE
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                is_playing = True
                egg_rect.left = 800
        
        if event.type == obs_timer and is_playing:
            enemy_rect_list.append(egg_surf.get_rect(bottomleft=(800, GROUND_Y)))

    if is_playing:
        screen.fill("purple")  # Wipe the screen

        # Blit the level assets
        screen.blit(SKY_SURF, (0, 0))
        screen.blit(GROUND_SURF, (0, GROUND_Y))
        #pygame.draw.rect(screen, "#c0e8ec", score_rect)
        #pygame.draw.rect(screen, "#c0e8ec", score_rect, 10)
        #screen.blit(score_surf, score_rect)
        score = display_score()

        # Adjust egg's horizontal location then blit it
        '''egg_rect.x -= 5
        if egg_rect.right <= 0:
            egg_rect.left = 800
        screen.blit(egg_surf, egg_rect)'''

        # Adjust player's vertical location then blit it
        players_gravity_speed += 1
        player_rect.y += players_gravity_speed
        if player_rect.bottom > GROUND_Y:
            player_rect.bottom = GROUND_Y
        screen.blit(player_surf, player_rect)

        # When player collides with enemy, game ends
        if egg_rect.colliderect(player_rect):
            is_playing = False

        

    # When game is over, display game over message
    else:
        screen.fill((94, 129, 162))
        start_time = int(pygame.time.get_ticks()/1000)
        screen.blit(starting_icon, starting_icon_rect)

        score_message = game_font.render(f"Your score: {score}", False, (111, 196, 169))
        score_message_rect = score_message.get_rect(center = (400, 350))
        screen.blit(game_font, game_name_rect)

        if score == 0:
            screen.blit(game_message, game_message_rect)
        else:
            screen.blit(score_message, score_message_rect)

    # flip the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # Limits game loop to 60 FPS

pygame.quit()
