import pygame
import objects
import random
import funcs

# CONSTANTS
SCREEN_HEIGHT = 880
SCREEN_WIDTH = 880
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
running = True
TILE_SIZE = 80
GRID_WIDTH = SCREEN_WIDTH // TILE_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // TILE_SIZE
PLAYER_X = 400
PLAYER_Y = 400

# pygame setup
pygame.init()
screen = pygame.display.set_mode((SCREEN_HEIGHT, SCREEN_WIDTH))
clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()
grid_boxes = [[random.randrange(1, 5, 1) for i in range(1000)] for i in range(1000)] # This will later be replaced with the map
cur_boxes = [grid_boxes[i] for i in range(GRID_WIDTH // TILE_SIZE)]
for i in range(100):
    box = objects.Box(random.randint(-100, 100)*TILE_SIZE, random.randint(-100, 100)*TILE_SIZE, TILE_SIZE, TILE_SIZE)
    all_sprites.add(box)
    wall = objects.Wall((i-10)*TILE_SIZE,2*TILE_SIZE, TILE_SIZE, TILE_SIZE)
    all_sprites.add(wall)
main_char = objects.MainChar(PLAYER_X, PLAYER_Y, TILE_SIZE, TILE_SIZE)
main_chars = pygame.sprite.Group()
main_chars.add(main_char)

# running the game
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if funcs.check_position("UP", all_sprites, (PLAYER_X, PLAYER_Y), TILE_SIZE):
                    all_sprites.update("UP", TILE_SIZE, PLAYER_X, PLAYER_Y)
            if event.key == pygame.K_DOWN:
                if funcs.check_position("DOWN", all_sprites,(PLAYER_X, PLAYER_Y), TILE_SIZE):
                    all_sprites.update("DOWN", TILE_SIZE, PLAYER_X, PLAYER_Y)
            if event.key == pygame.K_LEFT:
                if funcs.check_position("LEFT", all_sprites,(PLAYER_X, PLAYER_Y), TILE_SIZE):
                    all_sprites.update("LEFT", TILE_SIZE, PLAYER_X, PLAYER_Y)
            if event.key == pygame.K_RIGHT:
                if funcs.check_position("RIGHT", all_sprites,(PLAYER_X, PLAYER_Y), TILE_SIZE):
                    all_sprites.update("RIGHT", TILE_SIZE, PLAYER_X, PLAYER_Y)
        screen.fill(WHITE)
        for x in range(TILE_SIZE, SCREEN_WIDTH, TILE_SIZE):
            pygame.draw.line(screen, GRAY, (x, 0), (x, SCREEN_HEIGHT))
        for y in range(TILE_SIZE, SCREEN_HEIGHT, TILE_SIZE):
            pygame.draw.line(screen, GRAY, (0, y), (SCREEN_WIDTH, y))
        opened = False
        for sprite in all_sprites:
            if sprite.__class__ == objects.Box and sprite.near_main == True:
                opened = True
        all_sprites.draw(screen)
        main_chars.draw(screen)
        if opened:
            open_box = pygame.image.load("C:\\Users\\User\\Downloads\\Champion_Chest.webp")
            screen.blit(open_box, (0, 0))
        pygame.display.flip()
