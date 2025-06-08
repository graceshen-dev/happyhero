"""Dino Game in Python

A game similar to the famous Chrome Dino Game, built using pygame-ce.
Made by intern: @bassemfarid and Grace Shen 🤖

4c81685445dbe22bc2c71dd8d70097e199ed2554
"""

import pygame
import random #do i need to just import randint

#levels, hearts, only certaina mount of bullets and you pick them up

def display_score():
    current_time = int(pygame.time.get_ticks()/1000) - start_time
    score_surf = game_font.render(f"Score: {current_time}", False, (64, 64, 64))
    score_rect = score_surf.get_rect(center = (400, 50))
    screen.blit(score_surf, score_rect)
    return current_time

def enemy_movement(enemy_list):
    if enemy_list:
        for enemy_tup in enemy_list: #change name, not a tup
            enemy_tup[0].x -= 5

            if enemy_tup[1] == "egg":
                screen.blit(egg_surf, enemy_tup[0])
            elif enemy_tup[1] == "wall":
                if enemy_tup[2] == 30:
                    screen.blit(wall_surf1, enemy_tup[0])
                elif enemy_tup[2] == 20:
                    screen.blit(wall_surf2, enemy_tup[0])
                else:
                    screen.blit(wall_surf3, enemy_tup[0])
            elif enemy_tup[1] == "bullet": #NOT AN ENEMY BTW
                screen.blit(bullet_surf, enemy_tup[0])
            else:
                screen.blit(fly_surf, enemy_tup[0])

        temp_enemy_list = []
        for enemy_tup in enemy_list:
            if enemy_tup[0].x > -100:

                if len(enemy_tup) > 2:
                    temp_enemy_list.append([enemy_tup[0], enemy_tup[1], enemy_tup[2]])
                else:
                    temp_enemy_list.append([enemy_tup[0], enemy_tup[1]])
        return temp_enemy_list
    else: 
        return []

def collision(player, enemies):
    if enemies:
        for enemy_rect in enemies:
            if player.colliderect(enemy_rect[0]):
                return True
    return False
                 
def player_animation():
    global player_surf, player_index

    if player_rect.bottom < 300:
        #jump
        player_surf = player_jump
    else:
        player_index += 0.1
        if player_index >= len(player_walk):
            player_index = 0
        player_surf = player_walk[int(player_index)]

# Initialize Pygame and create a window
pygame.init()
start_time = 0
screen = pygame.display.set_mode((800, 400))
clock = pygame.time.Clock()
running = True  # Pygame main loop, kills pygame when False
score = 0
num_of_bullets = 10 #tehcnically not needed u can just do it in else of is-plahibg
collision1 = False #change name
pickup_inventory_list = []

# Game state variables
is_playing = False  # Whether in game or in menu
GROUND_Y = 300  # The Y-coordinate of the ground level
JUMP_GRAVITY_START_SPEED = -20  # The speed at which the player jumps
players_gravity_speed = 0  # The current speed at which the player falls

# Load level assets
SKY_SURF = pygame.image.load("graphics/level/sky.png").convert()
GROUND_SURF = pygame.image.load("graphics/level/ground.png").convert()
# license: httpsL//
game_font = pygame.font.Font(pygame.font.get_default_font(), 50)

# Load sprite assets
player_walk_1 = pygame.image.load("graphics/player/player_walk_1.png").convert_alpha()
player_walk_2 = pygame.image.load("graphics/player/player_walk_2.png").convert_alpha()
player_walk = [player_walk_1, player_walk_2]
player_index = 0
player_jump = pygame.image.load("graphics/player/player_jump.png").convert_alpha()
player_surf = player_walk[player_index]
player_rect = player_surf.get_rect(bottomleft=(25, GROUND_Y))

#sound liscence: https://pixabay.com/service/license-summary/
hitting_wall_sound = pygame.mixer.Sound('sounds/hitting_wall.mp3')
egg_frame_1 = pygame.image.load("graphics/egg/egg_1.png").convert_alpha()
egg_frame_2 = pygame.image.load("graphics/egg/egg_2.png").convert_alpha()
egg_frames = [egg_frame_1, egg_frame_2]
egg_frame_index = 0
egg_surf = egg_frames[egg_frame_index]
egg_rect = egg_surf.get_rect(bottomleft=(800, GROUND_Y))

starting_icon = pygame.image.load("graphics/player/player_walk_1.png").convert_alpha()
starting_icon = pygame.transform.rotozoom(starting_icon, 0, 2)
starting_icon_rect = starting_icon.get_rect(center=(400, 200))

fly_frame1 = pygame.image.load("graphics/player/player_walk_1.png").convert_alpha()
fly_frame2= pygame.image.load("graphics/player/player_walk_2.png").convert_alpha()
fly_frames = [fly_frame1, fly_frame2]
fly_frame_index = 0
fly_surf = fly_frames[fly_frame_index]

wall_surf1 = pygame.image.load("graphics/wall/wall1.png").convert_alpha()
wall_surf2 = pygame.image.load("graphics/wall/wall2.png").convert_alpha()
wall_surf3 = pygame.image.load("graphics/wall/wall3.png").convert_alpha()

bullet_surf = pygame.image.load("graphics/pickups/bullet.png").convert_alpha()

shooters = []

enemy_rect_list = []


#text
game_name = game_font.render("MY GAMEEEE", False, (11, 196, 169))
game_name_rect = game_name.get_rect(center = (400, 80))

game_message = game_font.render("Press space to go", False, (11, 196, 169))
game_message_rect = game_message.get_rect(center = (400, 350))



#timer
obs_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obs_timer, 1500)

egg_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(egg_animation_timer, 500)

fly_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(fly_animation_timer, 200)

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
                
        
            if (event.type == pygame.KEYDOWN and event.key == pygame.K_f):
                    #shoot stuff

                    if num_of_bullets > 0:
                        num_of_bullets -= 1 
                        shooter_rect = bullet_surf.get_rect(midleft=(player_rect.right, player_rect.centery))
                        shooters.append(shooter_rect)
                    #Hp

        else:
            # When player wants to play again by pressing SPACE
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                is_playing = True
                egg_rect.left = 800 #do i still need this
        
        if is_playing:

            if event.type == obs_timer:
                item_choice = random.randint(0, 3)
                if item_choice == 0:
                    enemy_rect_list.append([egg_surf.get_rect(bottomleft=(random.randint(900, 1200), GROUND_Y)), "egg"])
                elif item_choice == 1:
                    enemy_rect_list.append([fly_surf.get_rect(bottomleft=(random.randint(900, 1200), 210)), "fly"]) #210 is higher above
                elif item_choice == 2:
                    enemy_rect_list.append([wall_surf1.get_rect(bottomleft=(random.randint(900, 1200), 275)), "wall", 30]) #idk if this inneficient
                elif item_choice == 3:
                    pickup_inventory_list.append([bullet_surf.get_rect(bottomleft=(random.randint(900, 1200), 295)), "bullet"])
                

            if event.type == egg_animation_timer:
                if egg_frame_index == 0:
                    egg_frame_index = 1
                else:
                    egg_frame_index = 0
                egg_surf = egg_frames[egg_frame_index]

            if event.type == fly_animation_timer:
                if fly_frame_index == 0:
                    fly_frame_index = 1
                else:
                    fly_frame_index = 0
                fly_surf = fly_frames[fly_frame_index]
        

    if is_playing:
        screen.fill("purple")  # Wipe the screen

        # Blit the level assets
        screen.blit(SKY_SURF, (0, 0))
        screen.blit(GROUND_SURF, (0, GROUND_Y))
        score = display_score()

        # Adjust player's vertical location then blit it
        players_gravity_speed += 1
        player_animation()
        player_rect.y += players_gravity_speed
        if player_rect.bottom > GROUND_Y:
            player_rect.bottom = GROUND_Y
        screen.blit(player_surf, player_rect)
        

        enemy_rect_list = enemy_movement(enemy_rect_list)
        pickup_inventory_list = enemy_movement(pickup_inventory_list)

        # When player collides with enemy, game ends
        is_playing = not collision(player_rect, enemy_rect_list)

        if collision(player_rect, pickup_inventory_list):
            for item in pickup_inventory_list:
                    if player_rect.colliderect(item[0]) and item[1] == "bullet":
                        num_of_bullets += 1
                        pickup_inventory_list.remove(pickup_inventory_list[pickup_inventory_list.index(item)])
        
        inventory_surf = game_font.render(f"Bullets: {num_of_bullets}", False, (64, 64, 64))
        inventory_rect = inventory_surf.get_rect(center = (100, 50))
        screen.blit(inventory_surf, inventory_rect)
    
        #shooting
        for shot in shooters[:]:
            shot.x += 10
            screen.blit(bullet_surf, shot)

            if collision(shot, enemy_rect_list): #if it collides
                for enemy_rect in enemy_rect_list:
                    if shot.colliderect(enemy_rect[0]):
                        #enemy_rect[0].y = 0
                        shooters.remove(shooters[shooters.index(shot)])
                        if len(enemy_rect) > 2 and collision1 == False:
                            enemy_rect[2] -= 10
                            collision1 = True
                            hitting_wall_sound.play()

                            if enemy_rect[2] == 0:
                                enemy_rect_list.remove(enemy_rect)
                            break
                            
            else:
                collision1 = False
                print('false')
                    
            if shot.x > 800:
                shooters.remove(shot)

    else:
        # When game is over, display game over message
        screen.fill((94, 129, 162))
        start_time = int(pygame.time.get_ticks()/1000)
        screen.blit(starting_icon, starting_icon_rect)
        enemy_rect_list.clear()
        player_rect.midbottom = (80, 300)
        players_gravity_speed = 0
        num_of_bullets = 10 #reset num of bullets????

        score_message = game_font.render(f"Your score: {score}", False, (111, 196, 169))
        score_message_rect = score_message.get_rect(center = (400, 350))
        screen.blit(game_name, game_name_rect)

        if score == 0:
            screen.blit(game_message, game_message_rect)
        else:
            screen.blit(score_message, score_message_rect)

    # flip the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # Limits game loop to 60 FPS

pygame.quit()
