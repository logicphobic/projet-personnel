import pygame
import random
import os
pygame.init()

WIN_WIDTH, WIN_HEIGHT = 1270, 950
BUTTON_WIDTH, BUTTON_HEIGHT = 38, 38

FPS = 60 # frames per second
screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("PROTOTYPE BY MY GLORIOUS KING KAMIL")
clock = pygame.time.Clock() # clock object

PLATFORM_COLOR = (92, 64, 51)
LEFT_PLATFORM = 0
TOP_PLATFORM = WIN_HEIGHT - 25
WIDTH_PLATFORM = int(WIN_WIDTH)
HEIGHT_PLATFORM = 50
platform = pygame.Rect(LEFT_PLATFORM, TOP_PLATFORM, WIDTH_PLATFORM, HEIGHT_PLATFORM)

player_image = pygame.image.load("player.png").convert_alpha()
player_scale = pygame.transform.scale_by(player_image, 3)
KAMIL_RECT = player_scale.get_rect(bottomleft=(0, TOP_PLATFORM))
KAMIL_SPEED = 16
direction = "right"

play_button = pygame.transform.scale(pygame.image.load('play_button.png'), (BUTTON_WIDTH, BUTTON_HEIGHT))
pause_button = pygame.transform.scale(pygame.image.load('pause_button.png'), (BUTTON_WIDTH, BUTTON_HEIGHT))
skip_button = pygame.transform.scale(pygame.image.load('skip_button.png'), (BUTTON_WIDTH, BUTTON_HEIGHT))
back_button = pygame.transform.scale(pygame.image.load('back_button.png'), (BUTTON_WIDTH, BUTTON_HEIGHT))
volume_button = pygame.transform.scale(pygame.image.load('volume_button.png'), (BUTTON_WIDTH, BUTTON_HEIGHT))

songs = ['tellem.mp3', 'getbusy.mp3', 'nostylist.mp3', 'iservethebase.mp3', 'iloveuihateu.mp3', 'nosleep.mp3', 'moneysobig.mp3', '500lbs.mp3', 'kidcudi.mp3', 'maskoff.mp3', 'nostylist.mp3', 'outtheway.mp3', 'over.mp3', 'rip.mp3', 'shookones.mp3', 'solo.mp3', 'toomanynights.mp3', 'yahmean.mp3']
current_song = None

def play_song(song):
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(0)

def play_random_song():
    global current_song
    current_song = random.choice(songs)
    play_song(current_song)

play_random_song()

gravity_direction = 1
can_jump = True
JUMP_VEL = -21 
MAX_JUMP_HEIGHT = WIN_HEIGHT
vel_y = 0 
is_jumping = False
double_jump = False


keepWorkingSlave = True

BACKGROUND = (0, 0, 0)

while keepWorkingSlave:
    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_c]:
        R = random.randint(0,255)
        G = random.randint(0,255)
        B = random.randint(0,255)
        BACKGROUND = (R, G, B)

    if keys[pygame.K_f]:
        print(f"KAMIL_RECT.bottom is {KAMIL_RECT.bottom}")
        print(f"KAMIL_RECT.top is {KAMIL_RECT.top}")
        print(f"gravity_direction is {gravity_direction}")
        print(f"vel_y is {vel_y}")
        print(f"is_jumping is {is_jumping}")
        print(f"double_jump is {double_jump}")

    screen.fill((BACKGROUND))
        
    dt = clock.tick(FPS) / 1000
    events = pygame.event.get()

    for event in events:
        if event.type == pygame.QUIT:
            keepWorkingSlave = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not is_jumping:
                vel_y = JUMP_VEL
                is_jumping = True
                double_jump = True
                
            elif event.key == pygame.K_SPACE and double_jump and gravity_direction == 1:
                vel_y = JUMP_VEL
                double_jump = False

            elif event.key == pygame.K_SPACE and double_jump and gravity_direction == -1:
                vel_y = -JUMP_VEL
 
            if event.key == pygame.K_g:
               player_scale = pygame.transform.flip(player_scale, False, True)
               is_jumping = True
               vel_y = 0
               gravity_direction *= -1
               double_jump = True

    if is_jumping and gravity_direction == 1:
        vel_y += 1
    elif is_jumping and gravity_direction == -1:
        vel_y += -1
                      
    KAMIL_RECT.y += vel_y

    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        KAMIL_RECT.x -= KAMIL_SPEED
        direction = "left"
    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        KAMIL_RECT.x += KAMIL_SPEED
        direction = "right"

    if KAMIL_RECT.left < 0:
        KAMIL_RECT.left = 0

    if KAMIL_RECT.right > WIN_WIDTH:
        KAMIL_RECT.right = WIN_WIDTH
    
    if KAMIL_RECT.top < 0:
        KAMIL_RECT.top = 0

    if KAMIL_RECT.bottom > TOP_PLATFORM and gravity_direction == 1:
        KAMIL_RECT.bottom = TOP_PLATFORM
        vel_y = 0
        is_jumping = False
        double_jump = True

    elif KAMIL_RECT.bottom > TOP_PLATFORM and gravity_direction == -1:
        KAMIL_RECT.bottom = TOP_PLATFORM - 20
        isjumping = False
        double_jump = False
    if KAMIL_RECT.top == 0 and gravity_direction == -1:
        vel_y = 0
        double_jump = True

    if event.type == pygame.MOUSEBUTTONDOWN:
        x, y = pygame.mouse.get_pos()
    if event.type == pygame.MOUSEBUTTONUP:
        if x < BUTTON_WIDTH and y < BUTTON_HEIGHT:
            if pygame.mixer.music.get_busy():
                    pygame.mixer.music.stop()
            else:
                    play_song(current_song)
        elif BUTTON_WIDTH <= x < 2*BUTTON_WIDTH and y < BUTTON_HEIGHT:
                play_random_song()
        elif 2*BUTTON_WIDTH <= x < 3*BUTTON_WIDTH and y < BUTTON_HEIGHT:
                pygame.mixer.music.rewind()

 
    pygame.draw.rect(screen, PLATFORM_COLOR, platform)
    
    screen.blit(play_button if pygame.mixer.music.get_busy() else pause_button, (0, 0))
    screen.blit(skip_button, (BUTTON_WIDTH, 0))
    screen.blit(back_button, (2*BUTTON_WIDTH, 0))



    if direction == "right":
        screen.blit(player_scale, KAMIL_RECT)
    else:
        flipped_image = pygame.transform.flip(player_scale, True, False)
        screen.blit(flipped_image, KAMIL_RECT)
        

    pygame.display.flip()

pygame.quit()
