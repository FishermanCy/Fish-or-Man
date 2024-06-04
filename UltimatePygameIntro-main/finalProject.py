import pygame
from sys import exit
import random
#All art was made myself, music/sound effects were made by my sister.

# fisherman animation function
def fisherman_animation():
    global fisherman_surf, fisherman_index    
    fisherman_index += 0.05
    if fisherman_index >= len(fisherman_swim):
        fisherman_index = 0
    fisherman_surf = fisherman_swim[int(fisherman_index)]

# fish animation function
def fish_animation():
    global fish_surf, fish_index    
    fish_index += 0.05
    if fish_index >= len(fish_swim):
        fish_index = 0
    fish_surf = fish_swim[int(fish_index)]

# jellyfish animation function
def jellyfish_animation():
    global jellyfish_surf, jellyfish_index
    jellyfish_index += 0.05
    if jellyfish_index >= len(jellyfish_wiggle):
        jellyfish_index = 0
    jellyfish_surf = jellyfish_wiggle[int(jellyfish_index)]

# initializing pygame and some variables
pygame.init()
screen=pygame.display.set_mode((800,400))
pygame.display.set_caption("Fish-or-Man")
clock=pygame.time.Clock()
test_font=pygame.font.SysFont("Comic Sans", 20)
game_active = 0
fish_wins = 0
fisherman_wins = 0
fish_jump_sound = pygame.mixer.Sound('finalProjectAudio/fishJump.ogg')
fisherman_jump_sound = pygame.mixer.Sound('finalProjectAudio/fishermanJump.ogg')
music = pygame.mixer.Sound('finalProjectAudio/background.ogg')
music.set_volume(0.3)
music.play(loops = -1)

# creating the background, foreground, and some text
water_surface=pygame.image.load("finalProjectGraphics/water.png").convert()
sand_surface=pygame.image.load("finalProjectGraphics/sand.png").convert()
fish_lead=test_font.render("FISH IS IN THE LEAD!", False, "Black")
fisherman_lead=test_font.render("FISHERMAN IS IN THE LEAD!", False, "Black")
tied=test_font.render("FISH AND FISHERMAN ARE TIED!", False, "Black")

# creating various variables for the fish, including their animation frames and rects
fish_swim_1=pygame.image.load("finalProjectGraphics/fishOne.png").convert_alpha()
fish_swim_2=pygame.image.load("finalProjectGraphics/fishTwo.png").convert_alpha()
fish_swim=[fish_swim_1,fish_swim_2]
fish_index=0
fish_surf=fish_swim[fish_index]
fish_rect = fish_surf.get_rect(midbottom = (720,325))
fish_gravity=0
fish_score=0

# creating various variables for the fisherman, including their animation frames and rects
fisherman_swim_1 = pygame.image.load('finalProjectGraphics/fishermanOne.png').convert_alpha()
fisherman_swim_2 = pygame.image.load('finalProjectGraphics/fishermanTwo.png').convert_alpha()
fisherman_swim = [fisherman_swim_1,fisherman_swim_2]
fisherman_index = 0
fisherman_surf = fisherman_swim[fisherman_index]
fisherman_rect = fisherman_surf.get_rect(midbottom = (80,300))
fisherman_gravity=0
fisherman_score=0

# creating various variables for the jellyfish, including their animation frames and rects
jellyfish_wiggle_1 = pygame.image.load('finalProjectGraphics/jellyfishOne.png').convert_alpha()
jellyfish_wiggle_2 = pygame.image.load('finalProjectGraphics/jellyfishTwo.png').convert_alpha()
jellyfish_wiggle = [jellyfish_wiggle_1,jellyfish_wiggle_2]
jellyfish_index = 0
jellyfish_surf = jellyfish_wiggle[jellyfish_index]
jellyfish_rect = jellyfish_surf.get_rect(midbottom = (400, 200))
jellyfish_gravity=0

# creating cannonball 1 and 2
cannonball1_surf = pygame.image.load('finalProjectGraphics/cannonball.png').convert_alpha()
cannonball1_rect = cannonball1_surf.get_rect(midbottom = (400,300))
cannonball2_surf = pygame.image.load('finalProjectGraphics/cannonball.png').convert_alpha()
cannonball2_rect = cannonball2_surf.get_rect(midbottom = (400,300))

# creating the cannon
cannon_surf = pygame.image.load('finalProjectGraphics/cannon.png').convert_alpha()
cannon_rect = cannon_surf.get_rect(midbottom = (400, 375))

# the game loop
while True:
    # allowing the user to quit the game
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            exit()
        
        # while the game is running
        if game_active == 0:
            # keybinds for actions in the game
            if event.type == pygame.KEYDOWN and fisherman_rect.bottom >= 300:
                if event.key==pygame.K_w:
                    fisherman_gravity = -20
                    fisherman_jump_sound.play()
            if event.type == pygame.KEYDOWN and fish_rect.bottom >= 300:
                if event.key==pygame.K_UP:
                    fish_gravity = -20
                    fish_jump_sound.play()
        # while the game is finished
        else:
            # keybinds to reset the game
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = 0
                fish_score=0
                fisherman_score=0
                cannonball1_rect.midbottom = (400, 300)
                cannonball2_rect.midbottom = (400, 300)
                fisherman_rect.midbottom = (80, 300)
                fisherman_gravity=0
                fish_rect.midbottom = (720, 325)
                fish_gravity=0

    # while the game is running
    if game_active == 0:

        # blit the background and foreground
        screen.blit(water_surface, (0,0))
        screen.blit(sand_surface, (0,300))

        # call the respective animation function and make gravity and floors work
        fish_animation()
        fish_gravity+=1
        fish_rect.y+=fish_gravity
        if fish_rect.bottom>325:
            fish_rect.bottom=325

        # call the respective animation function and make gravity and floors work
        fisherman_animation()
        fisherman_gravity+=1
        fisherman_rect.y+=fisherman_gravity
        if fisherman_rect.bottom>300:
            fisherman_rect.bottom=300

        # call the respective animation function and make gravity and floors work
        jellyfish_animation()
        jellyfish_gravity+=0.05
        jellyfish_rect.y+=jellyfish_gravity
        if jellyfish_rect.bottom > 200:
            jellyfish_rect.bottom=200
            jellyfish_gravity-=4

        # making both cannonballs have random speeds, and make them return to their original positions when they go off screen. When they return, award each player a point
        cannonball1_rect.right-=random.randint(6,13)
        if cannonball1_rect.right < -100:
            cannonball1_rect.midbottom = (400, 300)
            fisherman_score+=1
        cannonball2_rect.right+=random.randint(6,13)
        if cannonball2_rect.right > 900:
            cannonball2_rect.midbottom = (400, 300)
            fish_score+=1

        # blit all characters and objects
        screen.blit(fish_surf, fish_rect)
        screen.blit(fisherman_surf, fisherman_rect)
        screen.blit(jellyfish_surf, jellyfish_rect)
        screen.blit(cannonball1_surf, cannonball1_rect)
        screen.blit(cannonball2_surf, cannonball2_rect)
        screen.blit(cannon_surf, cannon_rect)

        # changing gamestates based on collision
        if fisherman_rect.colliderect(cannonball1_rect):
            game_active = 1
        if fish_rect.colliderect(cannonball2_rect):
            game_active = 2

        # if the fisherman died, this runs
        if game_active == 1:
            #adding a win to the fish
            fish_wins += 1
            # filling the screen and adding new text to display the fish winning, their total wins, and who's in the lead
            screen.fill('Blue')
            text_surface=test_font.render("FISHERMAN LOST, FISH PREVAILS! FISH SCORE WAS " + str(fish_score), False, "Black")
            text_surface_2=test_font.render("FISHERMAN HAS WON " + str(fisherman_wins) + " TIMES AND THE FISH HAS WON " + str(fish_wins) + " TIMES!", False, "Black")
            screen.blit(text_surface, (50,50))
            screen.blit(text_surface_2, (50,100))
            if fish_wins > fisherman_wins:
                screen.blit(fish_lead, (50,150))
            elif fisherman_wins > fish_wins:
                screen.blit(fisherman_lead, (50,150))
            elif fish_wins == fisherman_wins:
                screen.blit(tied, (50,150))
        
        # if the fish died, this runs
        elif game_active == 2:
            # adding a win to the fisherman
            fisherman_wins += 1
            # filling the screen and adding new text to display the fisherman winning, their total wins, and who's in the lead
            screen.fill('Green')
            text_surface=test_font.render("FISH LOST, FISHERMAN PREVAILS! FISHERMAN SCORE WAS " + str(fisherman_score), False, "Black")
            text_surface_2=test_font.render("FISHERMAN HAS WON " + str(fisherman_wins) + " TIMES AND THE FISH HAS WON " + str(fish_wins) + " TIMES!", False, "Black")
            screen.blit(text_surface, (50,50))
            screen.blit(text_surface_2, (50,100))
            if fish_wins > fisherman_wins:
                screen.blit(fish_lead, (50,150))
            elif fisherman_wins > fish_wins:
                screen.blit(fisherman_lead, (50,150))
            elif fish_wins == fisherman_wins:
                screen.blit(tied, (50,150))
    
    # updating the display and changing frames
    pygame.display.update()
    clock.tick(60)