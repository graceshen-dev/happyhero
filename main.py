"""Dino Game in Python

A game similar to the famous Chrome Dino Game, built using pygame-ce.
Made by intern: @bassemfarid and Grace Shen 🤖

4c81685445dbe22bc2c71dd8d70097e199ed2554
"""

import pygame
import random

def increase_difficulty(increase_amount):
    '''
    Increases the game difficulty by adjusting speed and health values.

        Parameters:
            increase_amount (int or float): The amount that increases speed of obstacles and max pickup value + damage for bullets.
    '''
    global obstacle_speed, max_bullet_pickup_value, bullet_damage

    if obstacle_speed < 15: #cap the obstacle speed at 14
        obstacle_speed += increase_amount 
    max_bullet_pickup_value += increase_amount
    bullet_damage += increase_amount

def update_ground():
    '''
    Keeps the ground constantly moving by shifting duplicate images to the left. Loops them around again once they leave the screen.
    '''
    global ground1_x_value, ground2_x_value

    #Move both grounds to the left
    ground1_x_value -= obstacle_speed
    ground2_x_value -= obstacle_speed

    #Wrap around when they go off screen
    if ground1_x_value <= -800:
        ground1_x_value = ground2_x_value + 800
    if ground2_x_value <= -800:
        ground2_x_value = ground1_x_value + 800

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
        
            if item_name == "money" or item_name == "cupcake":
                global score
                score += item[2] * 5
    
    return collected_items

def draw_pause_button():
    '''
    Draws a small button with a question mark on the screen to let the user open instructions.
    '''
    pygame.draw.circle(screen, (200, 200, 200), (pause_button_rect.centerx, pause_button_rect.centery), 15)
    pause_menu_text = game_font.render("?", True, (0, 0, 0))
    screen.blit(pause_menu_text, (pause_button_rect.x + 12, pause_button_rect.y + 5))

def draw_instructions():
    '''
    Shows the instructions text on the screen (when the game is paused).
    '''
    instructions = [
        "Game Paused",
        "Press 'P' to resume",
        "Press 'F' to shoot happy faces",
        "Shoot them at upset/depressed people",
        "Avoid taxes and job applications",
        "+5 happiness per money/cupcake",
        "+10 happiness per person made happy"
    ]
    y = 100
    for i in range(len(instructions)):
        line = game_font.render(instructions[i], True, (0, 0, 0))
        text_rect = line.get_rect(center=(400, y))
        screen.blit(line, text_rect)
        y += 40

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

    instruction_text = instrction_font.render("POV: You are an unemployed teenager who just wants to spread some happiness in the city.\nPress SPACE to jump,\nF to shoot bullets of happiness at sad/upset people to cheer them up.\nAvoid bumping into obstacles (taxes, job applications, depressed people),\nand collect money & cupcakes!", True, (255, 255, 255))
    instruction_rect = instruction_text.get_rect(center=(400, 200))

    screen.blit(intro_background_surf, (0, 0))  # Background color
    screen.blit(title_text, title_rect)
    screen.blit(instruction_text, instruction_rect)

    dramatic_hero_sound.play()


def draw_lives(life_surf, lives, x, y, spacing):
    '''
    Draws life icons on the screen.

        Parameters:
            life_surf (pygame surface): The image represents 1 life.
            lives (int): Number of lives.
            x (int): Starting x position on the screen for the lives.
            y (int): Starting y position on the screen for the lives.
            spacing (int): Space in between each life.
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
                        happy_person_sound.play()
                        
                        if enemy_rect[2] <= 0:
                            enemy_rect_list.remove(enemy_rect)
                            happy_person_sound.play()
                            score += 10
                        break
        else:
            is_collision = False
                    
        if shot.x > 800:
            if shot in bullet_list:
                bullet_list.remove(shot)

def display_inventory():
    '''
    Shows how many bullets and lives the player currently has on the screen.
    '''
    inventory_surf = game_font.render(f"Bullets: {num_of_bullets}\nLives: ", False, (64, 64, 64))
    inventory_rect = inventory_surf.get_rect(center = (110, 50))
    screen.blit(inventory_surf, inventory_rect)

def lose_life(player, enemy_list):
    '''
    Subtract a life and play a sound whenever the player collides with any enemy in a list.

        Parameters:
            player (pygame rect): Player rectangle.
            enemy_list (list): List of enemy obstacles (rectangles).
    '''
    global num_of_lives

    for enemy in enemy_list:
        if player.colliderect(enemy[0]):
            num_of_lives -= 1
            enemy_collision_sound.play()

            enemy_list.remove(enemy_list[enemy_list.index(enemy)])


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
            if obstacle[1] == "job application":
                screen.blit(job_application_surf, obstacle[0])
            elif obstacle[1] == "mad businessman":
                if obstacle[2] == obstacle_health: #make this more dynamtic
                    screen.blit(mad_businessman_surf1, obstacle[0])
                elif obstacle[2] >= int(2*(obstacle_health/3)):
                    screen.blit(mad_businessman_surf2, obstacle[0])
                else:
                    screen.blit(mad_businessman_surf3, obstacle[0])

            elif obstacle[1] == "depressed girl":
                if obstacle[2] == obstacle_health:
                    screen.blit(depressed_girl_surf1, obstacle[0])
                elif obstacle[2] >= int(2*(obstacle_health/3)):
                    screen.blit(depressed_girl_surf2, obstacle[0])
                else:
                    screen.blit(depressed_girl_surf3, obstacle[0])

            elif obstacle[1] == "bullet":
                screen.blit(ground_bullet_surf, obstacle[0])
            elif obstacle[1] == "life":
                screen.blit(life_surf, obstacle[0])
            elif obstacle[1] == "money":
                screen.blit(money_surf, obstacle[0])
            elif obstacle[1] == "cupcake":
                screen.blit(cupcake_surf, obstacle[0])
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
        for rect in objects:
            if player.colliderect(rect[0]):
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
is_playing = False  # Whether in game or in menu
GROUND_Y = 300  # The Y-coordinate of the ground level
JUMP_GRAVITY_START_SPEED = -20  # The speed at which the player jumps
players_gravity_speed = 0  # The current speed at which the player falls
paused = False

# Load level assets
SKY_SURF = pygame.image.load("graphics/level/sky.png").convert()
GROUND_SURF = pygame.image.load("graphics/level/ground.png").convert()
intro_background_surf = pygame.image.load("graphics/level/intro_background.png").convert_alpha()
outro_background_surf = pygame.image.load("graphics/level/outro_background.png").convert_alpha()
ground1_x_value = 0
ground2_x_value = 800


game_font = pygame.font.Font("fonts/game_font.ttf", 25) # license: https://openfontlicense.org
title_font = pygame.font.Font("fonts/title_font.ttf", 60)
instrction_font = pygame.font.Font("fonts/instruction_font.ttf", 20)

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

job_application_frame_1 = pygame.image.load("graphics/enemies/job_application/job_application1.png").convert_alpha()
job_application_frame_2 = pygame.image.load("graphics/enemies/job_application/job_application2.png").convert_alpha()
job_application_frames = [job_application_frame_1, job_application_frame_2]
job_application_frame_index = 0
job_application_surf = job_application_frames[job_application_frame_index]
job_application_rect = job_application_surf.get_rect(bottomleft=(800, GROUND_Y))

starting_icon = pygame.image.load("graphics/player/game_icon.png").convert_alpha()
starting_icon = pygame.transform.rotozoom(starting_icon, 0, 2)
starting_icon_rect = starting_icon.get_rect(center=(400, 200))

fly_frame1 = pygame.image.load("graphics/enemies/flying_tax/flying_tax_frame_1.png").convert_alpha()
fly_frame1 = pygame.transform.rotozoom(fly_frame1, 0, 2.5)
fly_frame2= pygame.image.load("graphics/enemies/flying_tax/flying_tax_frame_2.png").convert_alpha()
fly_frame2 = pygame.transform.rotozoom(fly_frame2, 0, 2.5)
fly_frames = [fly_frame1, fly_frame2]
fly_frame_index = 0
fly_surf = fly_frames[fly_frame_index]

mad_businessman_surf1 = pygame.image.load("graphics/enemies/mad_businessman/mad_businessman1.png").convert_alpha()
mad_businessman_surf2 = pygame.image.load("graphics/enemies/mad_businessman/mad_businessman2.png").convert_alpha()
mad_businessman_surf3 = pygame.image.load("graphics/enemies/mad_businessman/mad_businessman3.png").convert_alpha()

depressed_girl_surf1 = pygame.image.load("graphics/enemies/depressed_girl/depressed_girl1.png").convert_alpha()
depressed_girl_surf1 = pygame.transform.rotozoom(depressed_girl_surf1, 0, 0.6)
depressed_girl_surf2 = pygame.image.load("graphics/enemies/depressed_girl/depressed_girl2.png").convert_alpha()
depressed_girl_surf2 = pygame.transform.rotozoom(depressed_girl_surf2, 0, 0.6)
depressed_girl_surf3 = pygame.image.load("graphics/enemies/depressed_girl/depressed_girl3.png").convert_alpha()
depressed_girl_surf3 = pygame.transform.rotozoom(depressed_girl_surf3, 0, 0.6)

bullet_surf = pygame.image.load("graphics/pickups/bullet.png").convert_alpha()
ground_bullet_surf = pygame.image.load("graphics/pickups/ground_bullet.png").convert_alpha()
life_surf = pygame.image.load("graphics/pickups/life.png").convert_alpha()
money_surf = pygame.image.load("graphics/pickups/money.png").convert_alpha()
cupcake_surf = pygame.image.load("graphics/pickups/cupcake.png").convert_alpha()

pause_button_rect = pygame.Rect(750, 10, 40, 40)

#sounds
money_pickup_sound = pygame.mixer.Sound('sounds/money_pickup.mp3') #all other sound liscences: https://pixabay.com/service/license-summary/
life_pickup_sound = pygame.mixer.Sound('sounds/life_pickup.mp3')
cupcake_pickup_sound = pygame.mixer.Sound('sounds/cupcake_pickup.mp3') #liscence: https://www.zapsplat.com/license-type/standard-license/
happy_bullet_pickup_sound = pygame.mixer.Sound('sounds/happy_bullet_pickup.mp3')
happy_person_sound = pygame.mixer.Sound('sounds/happy_person.mp3')
dramatic_hero_sound = pygame.mixer.Sound('sounds/dramatic_hero_sound.mp3')
enemy_collision_sound = pygame.mixer.Sound('sounds/enemy_collision.mp3')

shooters = []
enemy_rect_list = []
pickup_inventory_list = []

#timer
obs_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obs_timer, 1500)

job_application_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(job_application_animation_timer, 500)

fly_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(fly_animation_timer, 200)

pickup_timer = pygame.USEREVENT + 4
pygame.time.set_timer(pickup_timer, 1500)

while running:
    # Poll for events (?)
    for event in pygame.event.get():
    
        if event.type == pygame.QUIT: # --> user clicked X to close window
            running = False

        elif is_playing:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pause_button_rect.collidepoint(event.pos):
                    paused = True 

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:  # P key unpauses game and closes the instructions menu
                    paused = False

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


        else:
            # When player wants to play again by pressing SPACE
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                is_playing = True

                # Reset variables
                player_rect.midbottom = (80, 305)
                players_gravity_speed = 0
                enemy_rect_list.clear()
                shooters.clear()
                pickup_inventory_list.clear()
                bullet_enemy_collision = False
                num_of_bullets = 15
                num_of_lives = 3
                num_of_money = 0
                num_of_cupcakes = 0
                score = 0
                level = 1 
                obstacle_speed = 5
                obstacle_health = 30
                max_bullet_pickup_value = 1 #pickup value is how much the user will gain for picking them up
                life_pickup_value = 1
                money_pickup_value = 1
                cupcake_pickup_value = 1
                last_level_up_score = 0
                bullet_damage = 10
        
        if is_playing and paused == False:

            if event.type == obs_timer:
                enemy_choice = random.randint(0, 6)
                if enemy_choice <= 2:
                    enemy_rect_list.append([job_application_surf.get_rect(bottomleft=(random.randint(900, 1200), GROUND_Y)), "job application"])
                elif enemy_choice <= 4:
                    enemy_rect_list.append([fly_surf.get_rect(bottomleft=(random.randint(900, 1200), 200)), "fly"])
                elif enemy_choice == 5:
                    enemy_rect_list.append([mad_businessman_surf1.get_rect(bottomleft=(random.randint(900, 1200), GROUND_Y)), "mad businessman", obstacle_health])
                elif enemy_choice == 6:
                    enemy_rect_list.append([depressed_girl_surf1.get_rect(bottomleft=(random.randint(900, 1200), GROUND_Y)), "depressed girl", obstacle_health])
            
            if event.type == pickup_timer:
                item_choice = random.randint(0, 100)
                if item_choice < 70:
                    pickup_inventory_list.append([ground_bullet_surf.get_rect(bottomleft=(random.randint(900, 1200), 295)), "bullet", random.randint(1, max_bullet_pickup_value)])
                elif item_choice < 75:
                    pickup_inventory_list.append([life_surf.get_rect(bottomleft=(random.randint(900, 1200), 295)), "life", life_pickup_value])
                elif item_choice < 85:
                    pickup_inventory_list.append([life_surf.get_rect(bottomleft=(random.randint(900, 1200), 330)), "money", money_pickup_value])
                else:
                    pickup_inventory_list.append([cupcake_surf.get_rect(bottomleft=(random.randint(900, 1200), GROUND_Y)), "cupcake", cupcake_pickup_value])

            if event.type == job_application_animation_timer:
                if job_application_frame_index == 0:
                    job_application_frame_index = 1
                else:
                    job_application_frame_index = 0
                job_application_surf = job_application_frames[job_application_frame_index]

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
        dramatic_hero_sound.stop() #stop intro sound

        # Adjust player's vertical location then blit it
        players_gravity_speed += 1
        player_animation()
        player_rect.y += players_gravity_speed

        if player_rect.bottom > 305:
            player_rect.bottom = 305 #prevent it from sinking into ground
        screen.blit(player_surf, player_rect)
        
        enemy_rect_list = obstacle_movement(enemy_rect_list)
        pickup_inventory_list = obstacle_movement(pickup_inventory_list)

        display_inventory()
        shoot_mechanic(shooters, bullet_enemy_collision)
        draw_lives(life_surf, num_of_lives, 90, 25, 25)

        # When player collides with enemy, lose a life
        if collision(player_rect, enemy_rect_list):
            lose_life(player_rect, enemy_rect_list)

        if num_of_lives == 0:
            is_playing = False

        if collision(player_rect, pickup_inventory_list):
            num_of_bullets = pickup_item("bullet", pickup_inventory_list, num_of_bullets, happy_bullet_pickup_sound)
            num_of_lives = pickup_item("life", pickup_inventory_list, num_of_lives, life_pickup_sound)
            num_of_money = pickup_item("money", pickup_inventory_list, num_of_money, money_pickup_sound)
            num_of_cupcakes = pickup_item("cupcake", pickup_inventory_list, num_of_cupcakes, cupcake_pickup_sound)
    
        if score % 60 == 0 and score != last_level_up_score and score > 1:
            level += 1
            increase_difficulty(1)
            last_level_up_score = score
        

    else:
        screen.fill((94, 129, 162))
        dramatic_hero_sound.play()
    
        if score == 0:
            show_intro_screen()
        else:
            # When game is over, display game over message
            screen.blit(outro_background_surf, (0, 0)) 
            score_message = game_font.render(f"Your happiness score: {score}", False, (111, 196, 169))
            score_message_rect = score_message.get_rect(center = (400, 350))
            screen.blit(score_message, score_message_rect)
            screen.blit(starting_icon, starting_icon_rect)

        screen.blit(game_name, game_name_rect)


    # flip the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # Limits game loop to 60 FPS

pygame.quit()
