import pygame
import objects
import random
import funcs

# initialize the game
pygame.init()
pygame.font.init()

# CONSTANTS
SCREEN_HEIGHT = 880
SCREEN_WIDTH = 880
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
running = True
TILE_SIZE = 10
GRID_WIDTH = SCREEN_WIDTH // TILE_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // TILE_SIZE
PLAYER_X = 400
PLAYER_Y = 400
MONEY_POS = (10, 10)
FONT = pygame.font.Font(None, 20)

# VARIABLES
mcf = [10, 40, 0] # [0] is money, [1] is calm and [2] is focus
inventory = []

# pygame setup
screen = pygame.display.set_mode((SCREEN_HEIGHT, SCREEN_WIDTH))
clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()
all_auras = pygame.sprite.Group()
grid_boxes = [[random.randrange(1, 5, 1) for i in range(1000)] for i in range(1000)] # This will later be replaced with the map
cur_boxes = [grid_boxes[i] for i in range(GRID_WIDTH // TILE_SIZE)]
for i in range(100):
    box = objects.Box(random.randint(-100, 100)*TILE_SIZE, random.randint(-100, 100)*TILE_SIZE, TILE_SIZE, TILE_SIZE)
    all_sprites.add(box)
    wall = objects.Wall((i-10)*TILE_SIZE,2*TILE_SIZE, TILE_SIZE, TILE_SIZE)
    all_sprites.add(wall)
gate = objects.Gate(240, 240, TILE_SIZE, TILE_SIZE)
all_sprites.add(gate)
monk = objects.Monk(800, 800, TILE_SIZE, TILE_SIZE, TILE_SIZE)
all_sprites.add(monk)
store = objects.Store(-160, 720, TILE_SIZE, TILE_SIZE)
all_sprites.add(store)
fountain = objects.Fountain(400, 1040, TILE_SIZE, TILE_SIZE)
all_sprites.add(fountain)
portal = objects.Portal(320, -80, TILE_SIZE, TILE_SIZE)
all_sprites.add(portal)
all_auras.add(monk.monk_auras)
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
                if funcs.check_position("UP", all_sprites, all_auras, mcf[1], (PLAYER_X, PLAYER_Y), TILE_SIZE):
                    all_sprites.update("UP", TILE_SIZE, PLAYER_X, PLAYER_Y)
                    all_auras.update("UP", TILE_SIZE, PLAYER_X, PLAYER_Y)
            if event.key == pygame.K_DOWN:
                if funcs.check_position("DOWN", all_sprites, all_auras, mcf[1], (PLAYER_X, PLAYER_Y), TILE_SIZE):
                    all_sprites.update("DOWN", TILE_SIZE, PLAYER_X, PLAYER_Y)
                    all_auras.update("DOWN", TILE_SIZE, PLAYER_X, PLAYER_Y)
            if event.key == pygame.K_LEFT:
                if funcs.check_position("LEFT", all_sprites, all_auras, mcf[1], (PLAYER_X, PLAYER_Y), TILE_SIZE):
                    all_sprites.update("LEFT", TILE_SIZE, PLAYER_X, PLAYER_Y)
                    all_auras.update("LEFT", TILE_SIZE, PLAYER_X, PLAYER_Y)
            if event.key == pygame.K_RIGHT:
                if funcs.check_position("RIGHT", all_sprites, all_auras, mcf[1], (PLAYER_X, PLAYER_Y), TILE_SIZE):
                    all_sprites.update("RIGHT", TILE_SIZE, PLAYER_X, PLAYER_Y)
                    all_auras.update("RIGHT", TILE_SIZE, PLAYER_X, PLAYER_Y)
        screen.fill(WHITE)
        for x in range(TILE_SIZE, SCREEN_WIDTH, TILE_SIZE):
            pygame.draw.line(screen, GRAY, (x, 0), (x, SCREEN_HEIGHT))
        for y in range(TILE_SIZE, SCREEN_HEIGHT, TILE_SIZE):
            pygame.draw.line(screen, GRAY, (0, y), (SCREEN_WIDTH, y))
        popup_details = [False, None] # a list to pass by reference if a popup window is needed [0] and the popup image [1]
        for sprite in all_sprites:
            if sprite.near_main is True:
                funcs.check_action(popup_details, sprite, all_sprites, all_auras, mcf, TILE_SIZE, (PLAYER_X, PLAYER_Y))
        all_auras.draw(screen)
        all_sprites.draw(screen)
        main_chars.draw(screen)
        if popup_details[0]:
            screen.blit(popup_details[1], (0, 0))
        money_text = FONT.render(f"Money: ${mcf[0]}", True, BLACK)
        screen.blit(money_text, MONEY_POS)
        pygame.display.flip()
