import pygame
import sys

pygame.init();

screen_width = 1000
screen_height = 1200;
screen = pygame.display.set_mode((screen_width, screen_height));
pygame.display.set_caption("Collision And Movement With Gravity");

sprite_image = pygame.image.load('player.png');

sprite = pygame.transform.scale(sprite_image, (87,190));

clock = pygame.time.Clock();
gravity_sign = 1;
width = 0;
centre = 0;
collision = 0;
ground_check = True;
on_ground = 1;
can_jump = 1;
sprite_position = sprite.get_rect();
sprite_position.center = (200,200);
vertical_velocity = 0;
horizontal_velocity = 0;
movement_ratio_x = screen_width / 1000;
movement_ratio_y = screen_height /1000;
acceleration = 0.006;
max_velocity = 1;
jump_speed = 3;
gravity = 0.3;
collision_objects = [pygame.Rect(0,0,40,screen_height), pygame.Rect(screen_width - 40,0, 40, screen_height), pygame.Rect(0, 0, screen_width, 40), pygame.Rect(0, screen_height - 40, screen_width, 40), pygame.Rect(150,900,700,50), pygame.Rect(1000,300,700,100), pygame.Rect(150,500, 100, 300),pygame.Rect(450,700, 100, 50),pygame.Rect(750,700, 50, 100)];


def sign(num):
    if num > 0:
        return 1;
    else:
        return -1;

running = True
while running:
    dt = clock.tick(5000) / 10000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False;
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and on_ground == True: 
                vertical_velocity = -jump_speed;
                on_ground = False;
            if event.key == pygame.K_g:
                on_ground = False;
                sprite = pygame.transform.flip(sprite, False, True);
                vertical_velocity = 0;
                gravity_sign *= -1;
                jump_speed = -jump_speed;
            if event.key == pygame.K_a:
                horizontal_velocity = -1;
            if event.key == pygame.K_d:
                horizontal_velocity = 1;
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                horizontal_velocity = 0;
            if event.key == pygame.K_d:
                horizontal_velocity = 0;


    keys = pygame.key.get_pressed()
    if keys[pygame.K_a] and abs(horizontal_velocity) < max_velocity:
        horizontal_velocity -= acceleration;
    if keys[pygame.K_d] and abs(horizontal_velocity) < max_velocity:
        horizontal_velocity += acceleration;
    vertical_velocity += gravity * gravity_sign;
    

    sprite_position.y += vertical_velocity;
    sprite_position.x += horizontal_velocity;
    screen.fill((255,0,0));

    # Collision
    for object in collision_objects:
        pygame.draw.rect(screen, (0,255,0), object);
        #Horizontal Resolution

        #Left Side
        spritewidth = sprite_position.width;
        sprite_position.x += 77
        sprite_position.width = 10;
        width = object.width
        centre = object.centerx
        object.width = 15;
        object.centerx = object.left;
        pygame.draw.rect(screen, (255,0,255), sprite_position);
        pygame.draw.rect(screen, (0,0,255), object);
        while sprite_position.colliderect(object):
            sprite_position.x -= 1;
            horizontal_velocity = 0;
        sprite_position.width = spritewidth;
        sprite_position.x -= 77
        object.width = width;
        object.centerx = centre;
        #Right Side
        spritewidth = sprite_position.width;
        sprite_position.width = 10;
        oldRight = object.right;
        width = object.width;
        centre = object.centerx;
        object.width = 15;
        object.centerx = oldRight - 8;
        pygame.draw.rect(screen, (255,0,255), sprite_position);
        pygame.draw.rect(screen, (0,0,255), object);
        if sprite_position.colliderect(object):
            sprite_position.x += 1;
            horizontal_velocity = 0;
        sprite_position.width = spritewidth;
        object.width = width;
        object.centerx = centre;
        #Vertical Resolution
        while sprite_position.colliderect(object):
            sprite_position.y += -1 * sign(vertical_velocity);
            if sign(vertical_velocity) == -1:
                vertical_velocity = 0;
        if (gravity_sign == 1 and (object.left < sprite_position.right and sprite_position.left < object.right and sprite_position.bottom == object.top)):
            ground_check = True;
        elif gravity_sign == -1 and (object.left < sprite_position.right and sprite_position.left < object.right and sprite_position.top == object.bottom):
            ground_check = True;
        else:
            gravity = 0.01;
            on_ground = False;
    if ground_check == True:
        gravity = 0;
        vertical_velocity = 0;
        on_ground = True;
        ground_check = False;
    # Draw Sprite
    pygame.draw.rect(screen, (0,0,0), sprite_position, 5);
    screen.blit(sprite, sprite_position);

    
    pygame.display.flip();
pygame.quit();
sys.exit();
