from sqlalchemy import false
import pygame, sys
import random
from flask_sqlalchemy import SQLAlchemy 
pygame.init()

#the Function to draw floor appear continuously
def draw_floor():
    screen.blit(floor, (floor_x_pos, 600))
    screen.blit(floor, (floor_x_pos + x, 600))

def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop = (500, random_pipe_pos))
    top_pipe = pipe_surface.get_rect(midtop = (500, random_pipe_pos - 750))
    return bottom_pipe, top_pipe

#Move the pipes to the left of the screen
def move_pipe(pipes):
    for pipe in pipes:
        pipe.centerx -= 3
    return pipes 

def draw_pipe(pipes):
    for pipe in pipes:
        if pipe.bottom >= 550 :
            screen.blit(pipe_surface, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)
            screen.blit(flip_pipe, pipe)

def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            hit_sound.play()
            return False
    if bird_rect.top <= -75 or bird_rect.bottom >= 600:
        hit_sound.play()
        return False
    return True

def rotate_bird(bird1):
    new_bird = pygame.transform.rotozoom(bird1, -bird_movement *3, 1)
    return new_bird

def bird_animation():
    new_bird = bird_list[bird_index]
    new_bird_rect = new_bird.get_rect(center = (100, bird_rect.centery))
    return new_bird, new_bird_rect

def score_display(game_state):
    if game_state == 'main_game':
        score_surface = game_font.render(f'Score: {int(score)}', True, (255, 255, 255))
        score_rect = score_surface.get_rect(center = (x/2, 100))
        screen.blit(score_surface, score_rect)
    if game_state == 'game_over':
        score_surface = game_font.render(f'Score: {int(score)}', True, (255, 255, 255))
        score_rect = score_surface.get_rect(center = (x/2, 50))
        screen.blit(score_surface, score_rect)

        high_score_surface = game_font.render(f'High Score: {int(high_score)}', True, (255, 255, 255))
        high_score_rect = high_score_surface.get_rect(center = (x/2, 100))
        screen.blit(high_score_surface, high_score_rect)

def update_score(score, high_score):
    if score > high_score:
        high_score = score
    return high_score

x = 360
y = 640
screen = pygame.display.set_mode((x,y))         #Set screen ratio
clock = pygame.time.Clock()                         #Set FPS

game_font = pygame.font.Font('FileGame/04B_19.ttf', 40)

gravity = 0.25 #Gravity pull the bird down
bird_movement = 0
game_active = True
score = 0
high_score = 0
#Create The background
bg = pygame.image.load('FileGame/assets/background-night.png').convert()
bg = pygame.transform.scale2x(bg)

#Create The floor
floor = pygame.image.load('FileGame/assets/floor.png').convert()          
floor = pygame.transform.scale2x(floor)
floor_x_pos = 0

#Create The bird 
bird_down = pygame.transform.scale2x(pygame.image.load('FileGame/assets/yellowbird-downflap.png').convert_alpha())
bird_mid = pygame.transform.scale2x(pygame.image.load('FileGame/assets/yellowbird-midflap.png').convert_alpha())
bird_up = pygame.transform.scale2x(pygame.image.load('FileGame/assets/yellowbird-upflap.png').convert_alpha())
bird_list = [bird_down, bird_mid, bird_up]
bird_index = 0
bird = bird_list[bird_index]
bird_rect = bird.get_rect(center=(100, y/2))

#Create The pipe
pipe_surface = pygame.image.load('FileGame/assets/pipe-green.png').convert()
pipe_surface = pygame.transform.scale2x(pipe_surface)
pipe_list = []

#Create timer of bird 
birdflap = pygame.USEREVENT + 1
pygame.time.set_timer(birdflap, 200)

#Create The timer of pipes
spawnpine = pygame.USEREVENT
pygame.time.set_timer(spawnpine, 1200)#Before 1.2 will create the pipe
pipe_height = [300, 310, 320, 350, 400, 410, 450, ]#choose 1 of 3 to create height pipe

#Create The end display
game_over_surface = pygame.transform.scale2x(pygame.image.load('FileGame/assets/message.png').convert_alpha())
game_over_rect = game_over_surface.get_rect(center = (x/2, y/2))

#Create The sound
flap_sound = pygame.mixer.Sound('FileGame\sound\sfx_wing.wav')
hit_sound = pygame.mixer.Sound('FileGame\sound\sfx_hit.wav')

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                bird_movement = 0
                bird_movement = -7
                flap_sound.play()
            if event.key == pygame.K_SPACE and game_active ==False:
                game_active = True
                pipe_list.clear()
                bird_rect.center = (100, y/2)
                bird_movement = 0
                score = 0
        if event.type == spawnpine:
            pipe_list.extend(create_pipe())
        if event.type == birdflap:
            if bird_index < 2:
                bird_index += 1
            else:
                bird_index = 0
            bird, bird_rect = bird_animation()
    screen.blit(bg, (0, 0))
    if game_active:
        bird_movement += gravity# The bird will move down overtime
        rotated_bird = rotate_bird(bird)
        bird_rect.centery += bird_movement
        screen.blit(rotated_bird, bird_rect)

        game_active = check_collision(pipe_list)

        pipe_list = move_pipe(pipe_list)
        draw_pipe(pipe_list)
        score += 0.01
        score_display('main_game')
    else:
        screen.blit(game_over_surface, game_over_rect)
        high_score = update_score(score, high_score)
        score_display('game_over')
    
    floor_x_pos -= 1
    draw_floor()
    if floor_x_pos <= -x:
        floor_x_pos = 0
    
    pygame.display.update()
    clock.tick(120)