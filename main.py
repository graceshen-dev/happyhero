"""Dino Game in Python

A game similar to the famous Chrome Dino Game, built using pygame-ce.
Made by intern: @bassemfarid and Grace Shen 🤖

4c81685445dbe22bc2c71dd8d70097e199ed2554
"""

import pygame
import random

#tododododo
#docstrings DONE
#variable names working on it rn
#ad
#more sounds
#comment
#more pickups
#taxes

def increase_difficulty(increase_amount):
    '''
    Increases the game difficulty by adjusting speed and health values.

        Parameters:
            increase_amount (int or float): The amount that increases speed, wall health, and max pickup value for bullets.
    '''
    global obstacle_speed, wall_health, max_bullet_pickup_value
    if obstacle_speed < 15: #cap the obstacle speed at 14
        obstacle_speed += increase_amount 
    wall_health += increase_amount * 10
    max_bullet_pickup_value += increase_amount

def pickup_item(item_name, item_list, collected_items, sound):
    '''
    Checks for collision between player and items in a list. Collects items, updates amount of colleted items, and plays sound. Collecting certain items will increase score.

        Parameters:
            item_name (string): The type of item to collect (e.g., "money"). Stored in index 1 of each item.
            item_list (list): List of items currently in the game.
            collected_items (int): Number/value of items already collected.
            sound (pygame.mixer.Sound): Sound to play when item is collected.

        Returns:
            int: Updated number of collected items.
    '''
    for item in item_list:
        if player_rect.colliderect(item[0]) and item[1] == item_name:
            collected_items += item[2] #pickup value
            item_list.remove(item_list[item_list.index(item)])
            sound.play()
        
            if item_name == "money":
                global score
                score += item[2] * 5
    
    return collected_items

def draw_pause_button():
    '''
    Draws a small button with a question mark on the screen to let the user open instructions.
    '''
    pygame.draw.rect(screen, (200, 200, 200), pause_button_rect)
    font = pygame.font.SysFont(None, 30)
    text = font.render("?", True, (0, 0, 0))
    screen.blit(text, (pause_button_rect.x + 12, pause_button_rect.y + 5))

def draw_instructions():
    '''
    Shows the instructions text on the screen (when the game is paused).
    '''
    instructions = [
        "Game Paused",
        "Press 'P' to resume",
        "Use arrow keys to move",
        "Avoid the obstacles!"
    ]
    y = 100 #idk
    for i in range(len(instructions)):
        line = game_font.render(instructions[i], True, (0, 0, 0))
        text_rect = line.get_rect(center=(400 // 2, y)) # what is 400
        screen.blit(line, text_rect)
        y += 40

def update_ground():
    '''
    Keeps the ground constantly moving by shifting duplicate images to the left. Loops them around again once they leave the screen.
    '''
    global ground1_x_value, ground2_x_value

    # Move both grounds to the left
    ground1_x_value -= obstacle_speed
    ground2_x_value -= obstacle_speed

    # Wrap around when they go off screen
    if ground1_x_value <= -800:
        ground1_x_value = ground2_x_value + 800
    if ground2_x_value <= -800:
        ground2_x_value = ground1_x_value + 800

def show_intro_screen():
    '''
    Displays the starting welcome screen with the game title, basic instructions, icon, and background.
    '''
    global game_name, game_name_rect
    game_name = title_font.render("HAPPY HERO", False, (252, 244, 3))
    game_name_rect = game_name.get_rect(center = (400, 50))

    game_message = game_font.render("Press space to go", False, (252, 244, 3))
    game_message_rect = game_message.get_rect(center = (400, 350))
    screen.blit(game_message, game_message_rect)

    title_text = game_font.render(f"Welcome, {user_name}!", True, (255, 255, 255))
    title_rect = title_text.get_rect(center=(400, 100))

    instruction_text = game_font.render("Press SPACE to jump,\nF to shoot, avoid walls, collect donuts!", True, (255, 255, 255))
    instruction_rect = instruction_text.get_rect(center=(500, 200))

    screen.blit(intro_background_surf, (0, 0))  # Background color
    screen.blit(title_text, title_rect)
    screen.blit(instruction_text, instruction_rect)
    screen.blit(starting_icon, (10, 10)) # DO THIS


def draw_lives(life_surf, lives, x, y, spacing=40):
    '''
    Draws life icons on the screen.

        Parameters:
            life_surf (pygame surface): The image represents 1 life.
            lives (int): Number of lives.
            x (int): Starting x position on the screen.
            y (int): Starting y position on the screen.
            spacing (int): Space in between each life (Default is 40).
    '''
    for life in range(lives):
        screen.blit(life_surf, (x + life * spacing, y))

def shoot_mechanic(bullet_list, is_collision):
    '''
    Moves bullets, checks for collisions with enemies, and updates score when the user successfully "cures" a sad person.

        Parameters:
            bullet_list (list): List of bullet rects currently on screen.
            is_collision (boolean): Tracks if a bullet hit an enemy.
    '''
    global score
    for shot in bullet_list[:]:
            shot.x += 10
            screen.blit(bullet_surf, shot)

            if collision(shot, enemy_rect_list): #if it collides
                for enemy_rect in enemy_rect_list:
                    if shot.colliderect(enemy_rect[0]):
                        bullet_list.remove(bullet_list[bullet_list.index(shot)])
                        if len(enemy_rect) > 2 and is_collision == False:
                            enemy_rect[2] -= bullet_damage
                            is_collision = True
                            hitting_wall_sound.play() #change

                            if enemy_rect[2] == 0:
                                enemy_rect_list.remove(enemy_rect)
                                happy_person_sound.play()
                                score += 10
                            break
            else:
                is_collision = False
                    
            if shot.x > 800:
                bullet_list.remove(shot)

def display_inventory():
    '''
    Shows how many bullets and lives the player currently has on the screen.
    '''
    inventory_surf = game_font.render(f"Bullets: {num_of_bullets}\nLives: ", False, (64, 64, 64))
    inventory_rect = inventory_surf.get_rect(center = (110, 50))
    screen.blit(inventory_surf, inventory_rect)


def display_score():
    ''' 
    Shows the player's current score, labeled as "Happiness" on the screen.
    '''
    score_surf = game_font.render(f"Happiness: {score}", False, (64, 64, 64))
    score_rect = score_surf.get_rect(center = (400, 50))
    screen.blit(score_surf, score_rect)

def obstacle_movement(obstacle_list):
    '''
    Blits the correct obstacle, then moves the obstacles left across the screen & removes any that are off-screen.

        Parameters:
            obstacle_list (list): List of obstacles.

        Returns:
            list: Updated list of obstacles that are still visible on screen.
    '''
    if obstacle_list:
        for obstacle in obstacle_list: #change name, not a tup
            obstacle[0].x -= obstacle_speed
            if obstacle[1] == "egg":
                screen.blit(egg_surf, obstacle[0])
            elif obstacle[1] == "wall":
                if obstacle[2] > int(wall_health/3): #make this more dynamtic
                    screen.blit(mad_businessman_surf1, obstacle[0])
                elif obstacle[2] > int(2*(wall_health/3)):
                    screen.blit(mad_businessman_surf2, obstacle[0])
                else:
                    screen.blit(mad_businessman_surf3, obstacle[0])

            elif obstacle[1] == "depressed girl":
                if obstacle[2] > int(wall_health/3):
                    screen.blit(depressed_girl_surf1, obstacle[0])
                elif obstacle[2] > int(2*(wall_health/3)):
                    screen.blit(depressed_girl_surf2, obstacle[0])
                else:
                    screen.blit(depressed_girl_surf3, obstacle[0])

            elif obstacle[1] == "bullet":
                screen.blit(ground_bullet_surf, obstacle[0])
            elif obstacle[1] == "life":
                screen.blit(life_surf, obstacle[0])
            elif obstacle[1] == "money":
                screen.blit(money_surf, obstacle[0])
            else:
                screen.blit(fly_surf, obstacle[0])

        temp_obstacle_list = []
        for obstacle in obstacle_list:
            if obstacle[0].x > -100:
                if len(obstacle) > 2:
                    temp_obstacle_list.append([obstacle[0], obstacle[1], obstacle[2]])
                else:
                    temp_obstacle_list.append([obstacle[0], obstacle[1]])
        return temp_obstacle_list
    else: 
        return []

def collision(player, objects):
    '''
    Checks if the player collides with any rectangle.

        Parameters:
            player (pygame.Rect): The player's rectangle.
            objects (list): List of enemy rectangles.

        Returns:
            boolean: True if there is a collision, False if no collision.
    '''
    if objects:
        for enemy_rect in objects:
            if player.colliderect(enemy_rect[0]):
                return True
    return False
                 
def player_animation():
    '''
    Changes the player's image based on whether they are jumping or walking to animate the player.
    '''
    global player_surf, player_index

    if player_rect.bottom < GROUND_Y:
        player_surf = player_jump
    else:
        player_index += 0.1
        if player_index >= len(player_walk):
            player_index = 0
        player_surf = player_walk[int(player_index)]

# Initialize Pygame and create a window
pygame.init()
user_name = input("Yo! What's your name/user? ")

screen = pygame.display.set_mode((800, 400))
clock = pygame.time.Clock()

# Game state variables
running = True  # Pygame main loop, kills pygame when False
score = 0
num_of_bullets = 15 #tehcnically not needed u can just do it in else of is-plahibg
num_of_lives = 3 #tehcnically not needed u can just do it in else of is-plahibg
num_of_money = 0 #tehcnidalfkja
bullet_wall_collision = False
pickup_inventory_list = []
is_playing = False  # Whether in game or in menu
GROUND_Y = 300  # The Y-coordinate of the ground level
JUMP_GRAVITY_START_SPEED = -20  # The speed at which the player jumps
players_gravity_speed = 0  # The current speed at which the player falls
level = 1 #move this to the start

# Load level assets
SKY_SURF = pygame.image.load("graphics/level/sky.png").convert()
GROUND_SURF = pygame.image.load("graphics/level/ground.png").convert()
intro_background_surf = pygame.image.load("graphics/level/intro_background.png").convert_alpha()
ground1_x_value = 0
ground2_x_value = 800
game_font = pygame.font.Font("fonts/game_font.ttf", 25) # license: https://openfontlicense.org
title_font = pygame.font.Font("fonts/title_font.ttf", 60)
instrction_font = pygame.font.Font("fonts/instruction_font.ttf", 20)

pause_button_rect = pygame.Rect(750, 10, 40, 40)
paused = False


# Load sprite assets
player_walk_1 = pygame.image.load("graphics/player/player_walk_1.png").convert_alpha()
player_walk_1 = pygame.transform.rotozoom(player_walk_1, 0, 0.8)
player_walk_2 = pygame.image.load("graphics/player/player_walk_2.png").convert_alpha()
player_walk_2 = pygame.transform.rotozoom(player_walk_2, 0, 0.8)
player_jump = pygame.image.load("graphics/player/player_jump.png").convert_alpha()
player_jump = pygame.transform.rotozoom(player_jump, 0, 0.8)
player_walk = [player_walk_1, player_walk_2]
player_index = 0
player_surf = player_walk[player_index]
player_rect = player_surf.get_rect(bottomleft=(25, GROUND_Y))


egg_frame_1 = pygame.image.load("graphics/enemies/job_application/job_application1.png").convert_alpha()
egg_frame_2 = pygame.image.load("graphics/enemies/job_application/job_application2.png").convert_alpha()
egg_frames = [egg_frame_1, egg_frame_2]
egg_frame_index = 0
egg_surf = egg_frames[egg_frame_index]
egg_rect = egg_surf.get_rect(bottomleft=(800, GROUND_Y))

starting_icon = pygame.image.load("graphics/player/game_icon.png").convert_alpha()
starting_icon = pygame.transform.rotozoom(starting_icon, 0, 2)
starting_icon_rect = starting_icon.get_rect(center=(400, 200))

fly_frame1 = pygame.image.load("graphics/player/player_walk_1.png").convert_alpha()
fly_frame2= pygame.image.load("graphics/player/player_walk_2.png").convert_alpha()
fly_frames = [fly_frame1, fly_frame2]
fly_frame_index = 0
fly_surf = fly_frames[fly_frame_index]

mad_businessman_surf1 = pygame.image.load("graphics/enemies/mad_businessman/mad_businessman1.png").convert_alpha()
mad_businessman_surf2 = pygame.image.load("graphics/enemies/mad_businessman/mad_businessman2.png").convert_alpha()
mad_businessman_surf3 = pygame.image.load("graphics/enemies/mad_businessman/mad_businessman3.png").convert_alpha()

depressed_girl_surf1 = pygame.image.load("graphics/enemies/depressed_girl/depressed_girl1.png").convert_alpha()
depressed_girl_surf1 = pygame.transform.rotozoom(depressed_girl_surf1, 0, 0.5)
depressed_girl_surf2 = pygame.image.load("graphics/enemies/depressed_girl/depressed_girl2.png").convert_alpha()
depressed_girl_surf2 = pygame.transform.rotozoom(depressed_girl_surf2, 0, 0.5)
depressed_girl_surf3 = pygame.image.load("graphics/enemies/depressed_girl/depressed_girl3.png").convert_alpha()
depressed_girl_surf3 = pygame.transform.rotozoom(depressed_girl_surf3, 0, 0.5)

bullet_surf = pygame.image.load("graphics/pickups/bullet.png").convert_alpha()
ground_bullet_surf = pygame.image.load("graphics/pickups/ground_bullet.png").convert_alpha()
life_surf = pygame.image.load("graphics/pickups/life.png").convert_alpha()
money_surf = pygame.image.load("graphics/pickups/money.png").convert_alpha()



#sounds
hitting_wall_sound = pygame.mixer.Sound('sounds/hitting_wall.mp3') #sound liscences: https://pixabay.com/service/license-summary/
money_pickup_sound = pygame.mixer.Sound('sounds/money_pickup.mp3')
life_pickup_sound = pygame.mixer.Sound('sounds/life_pickup.mp3')
happy_bullet_pickup_sound = pygame.mixer.Sound('sounds/happy_bullet_pickup.mp3')
happy_person_sound = pygame.mixer.Sound('sounds/happy_person.mp3')

shooters = []
enemy_rect_list = []

#timer
obs_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obs_timer, 1500)

egg_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(egg_animation_timer, 500)

fly_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(fly_animation_timer, 200)

pickup_timer = pygame.USEREVENT + 4
pygame.time.set_timer(pickup_timer, 1500)

while running:
    # Poll for events (?)
    for event in pygame.event.get():
    
        if event.type == pygame.QUIT: # --> user clicked X to close your window
            running = False

        elif is_playing:
            # When player wants to jump by pressing SPACE
            if (
                event.type == pygame.KEYDOWN
                and event.key == pygame.K_SPACE
                or event.type == pygame.MOUSEBUTTONDOWN
            ) and player_rect.bottom >= GROUND_Y and paused == False:
                players_gravity_speed = JUMP_GRAVITY_START_SPEED
                
        
            if (event.type == pygame.KEYDOWN and event.key == pygame.K_f):
                    if num_of_bullets > 0:
                        num_of_bullets -= 1 
                        shooter_rect = bullet_surf.get_rect(midleft=(player_rect.right, player_rect.centery))
                        shooters.append(shooter_rect)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if pause_button_rect.collidepoint(event.pos):
                    paused = True #hit the pause button

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:  # Press P to unpause
                    paused = False

        else:
            # When player wants to play again by pressing SPACE
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                is_playing = True

                player_rect.midbottom = (80, GROUND_Y)
                players_gravity_speed = 0
                enemy_rect_list.clear()
                shooters.clear()
                pickup_inventory_list.clear()
                num_of_bullets = 15 #reset num of bullets????
                num_of_lives = 3
                num_of_money = 0
                score = 0
                obstacle_speed = 5
                wall_health = 30
                max_bullet_pickup_value = 1 #pickup value is how much the user will gain for picking them up
                life_pickup_value = 1
                money_pickup_value = 1
                last_level_up_score = 0 #anything but zero
                bullet_damage = 10
        
        if is_playing:

            if event.type == obs_timer:
                enemy_choice = random.randint(0, 6)
                if enemy_choice <= 2:
                    enemy_rect_list.append([egg_surf.get_rect(bottomleft=(random.randint(900, 1200), GROUND_Y)), "egg"])
                elif enemy_choice <= 4:
                    enemy_rect_list.append([fly_surf.get_rect(bottomleft=(random.randint(900, 1200), 200)), "fly"]) #210 is higher above
                elif enemy_choice == 5:
                    enemy_rect_list.append([mad_businessman_surf1.get_rect(bottomleft=(random.randint(900, 1200), GROUND_Y)), "wall", wall_health]) #idk if this inneficient
                elif enemy_choice == 6:
                    enemy_rect_list.append([depressed_girl_surf1.get_rect(bottomleft=(random.randint(900, 1200), GROUND_Y)), "depressed girl", wall_health])
            
            if event.type == pickup_timer:
                item_choice = random.randint(0, 10)
                #add random item choice once u add more pickups
                if item_choice < 5:
                    pickup_inventory_list.append([ground_bullet_surf.get_rect(bottomleft=(random.randint(900, 1200), 295)), "bullet", random.randint(1, max_bullet_pickup_value)])
                elif item_choice == 10:
                    pickup_inventory_list.append([life_surf.get_rect(bottomleft=(random.randint(900, 1200), 295)), "life", life_pickup_value])
                else:
                    pickup_inventory_list.append([life_surf.get_rect(bottomleft=(random.randint(900, 1200), 330)), "money", money_pickup_value])

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
        

    if paused:
        draw_instructions()
    elif is_playing:
        screen.fill("purple")  # Wipe the screen

        # Blit the level assets
        screen.blit(SKY_SURF, (0, 0))
        
        update_ground()
        screen.blit(GROUND_SURF, (ground2_x_value, GROUND_Y))
        screen.blit(GROUND_SURF, (ground1_x_value, GROUND_Y))
        display_score() #YO THIS DOESNT WORK 
        draw_pause_button()

        # Adjust player's vertical location then blit it
        players_gravity_speed += 1
        player_animation()
        player_rect.y += players_gravity_speed
        if player_rect.bottom > GROUND_Y:
            player_rect.bottom = GROUND_Y
        screen.blit(player_surf, player_rect)
        
        enemy_rect_list = obstacle_movement(enemy_rect_list)
        pickup_inventory_list = obstacle_movement(pickup_inventory_list)


        display_inventory()
        shoot_mechanic(shooters, bullet_wall_collision)
        draw_lives(life_surf, num_of_lives, 90, 25, 25)

        # When player collides with enemy, lose a life
        if collision(player_rect, enemy_rect_list):
            for enemy in enemy_rect_list:
                if player_rect.colliderect(enemy[0]):
                    num_of_lives -= 1

                    enemy_rect_list.remove(enemy_rect_list[enemy_rect_list.index(enemy)])

        if num_of_lives == 0:
            is_playing = False


        if collision(player_rect, pickup_inventory_list):
            num_of_bullets = pickup_item("bullet", pickup_inventory_list, num_of_bullets, happy_bullet_pickup_sound)
            num_of_lives = pickup_item("life", pickup_inventory_list, num_of_lives, life_pickup_sound)
            num_of_money = pickup_item("money", pickup_inventory_list, num_of_money, money_pickup_sound)
    
        if score % 60 == 0 and score != last_level_up_score and score > 1:
            increase_difficulty(1)
            level += 1
            last_level_up_score = score
        

    else:
        # When game is over, display game over message
        #put into function?
        screen.fill((94, 129, 162))
    
        if score == 0:
            show_intro_screen()
        else:
            
            screen.blit(intro_background_surf, (0, 0)) 
            score_message = game_font.render(f"Your happiness score: {score}", False, (111, 196, 169))
            score_message_rect = score_message.get_rect(center = (400, 350))
            screen.blit(score_message, score_message_rect)
            screen.blit(starting_icon, starting_icon_rect)
        
            
        
        screen.blit(game_name, game_name_rect)


    # flip the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # Limits game loop to 60 FPS

pygame.quit()
