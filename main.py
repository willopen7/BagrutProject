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
TILE_SIZE = 80
GRID_WIDTH = SCREEN_WIDTH // TILE_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // TILE_SIZE
PLAYER_X = 400
PLAYER_Y = 400
MONEY_POS = (10, 10)
INVENTORY_POS = (10, SCREEN_HEIGHT-TILE_SIZE-40)
COOLDOWN_WITHOUT_SHOES = 500
FONT = pygame.font.Font(None, 20)
inventory = [objects.InventoryItem(0, SCREEN_HEIGHT-TILE_SIZE, TILE_SIZE, TILE_SIZE, "C:\\Users\\User\\Downloads\\shoes.png")] # [0] is shoes
NUM_SLOTS = len(inventory)

# VARIABLES
mcf = [10, 40, 0] # [0] is money, [1] is calm and [2] is focus

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
can_move = True
cooldown = COOLDOWN_WITHOUT_SHOES
last_move_time = 0
inventory_slots = pygame.sprite.Group()
for i in range(NUM_SLOTS):
    slot = objects.InventorySlot(TILE_SIZE*i, SCREEN_HEIGHT-TILE_SIZE, TILE_SIZE, TILE_SIZE)
    inventory_slots.add(slot)
    inventory_slots.add(inventory[i])

# running the game
while running:
    current_time = pygame.time.get_ticks()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if funcs.check_position("UP", all_sprites, all_auras, mcf[1], (PLAYER_X, PLAYER_Y), TILE_SIZE) and can_move:
                    all_sprites.update("UP", TILE_SIZE, PLAYER_X, PLAYER_Y)
                    all_auras.update("UP", TILE_SIZE, PLAYER_X, PLAYER_Y)
                    can_move = False
                    last_move_time = current_time
            if event.key == pygame.K_DOWN:
                if funcs.check_position("DOWN", all_sprites, all_auras, mcf[1], (PLAYER_X, PLAYER_Y), TILE_SIZE) and can_move:
                    all_sprites.update("DOWN", TILE_SIZE, PLAYER_X, PLAYER_Y)
                    all_auras.update("DOWN", TILE_SIZE, PLAYER_X, PLAYER_Y)
                    can_move = False
                    last_move_time = current_time
            if event.key == pygame.K_LEFT:
                if funcs.check_position("LEFT", all_sprites, all_auras, mcf[1], (PLAYER_X, PLAYER_Y), TILE_SIZE) and can_move:
                    all_sprites.update("LEFT", TILE_SIZE, PLAYER_X, PLAYER_Y)
                    all_auras.update("LEFT", TILE_SIZE, PLAYER_X, PLAYER_Y)
                    can_move = False
                    last_move_time = current_time
            if event.key == pygame.K_RIGHT:
                if funcs.check_position("RIGHT", all_sprites, all_auras, mcf[1], (PLAYER_X, PLAYER_Y), TILE_SIZE) and can_move:
                    all_sprites.update("RIGHT", TILE_SIZE, PLAYER_X, PLAYER_Y)
                    all_auras.update("RIGHT", TILE_SIZE, PLAYER_X, PLAYER_Y)
                    can_move = False
                    last_move_time = current_time
        screen.fill(WHITE)
        for x in range(TILE_SIZE, SCREEN_WIDTH, TILE_SIZE):
            pygame.draw.line(screen, GRAY, (x, 0), (x, SCREEN_HEIGHT))
        for y in range(TILE_SIZE, SCREEN_HEIGHT, TILE_SIZE):
            pygame.draw.line(screen, GRAY, (0, y), (SCREEN_WIDTH, y))
        popup_details = [False, None] # a list to pass by reference if a popup window is needed [0] and the popup image [1]
        for sprite in all_sprites:
            if sprite.near_main is True:
                funcs.check_action(popup_details, sprite, all_sprites, all_auras, mcf, inventory, TILE_SIZE, (PLAYER_X, PLAYER_Y))
                cooldown = COOLDOWN_WITHOUT_SHOES/(2**inventory[0].amount)
        all_auras.draw(screen)
        all_sprites.draw(screen)
        main_chars.draw(screen)
        inventory_slots.draw(screen)
        if popup_details[0]:
            screen.blit(popup_details[1], (0, 0))
        money_text = FONT.render(f"Money: ${mcf[0]}", True, BLACK)
        inventory_text = FONT.render(f"Inventory:", True, BLACK)
        screen.blit(money_text, MONEY_POS)
        screen.blit(inventory_text, INVENTORY_POS)
        for i in range(len(inventory)):
            count_item = FONT.render(f"{inventory[i].amount}", True, BLACK)
            screen.blit(count_item, (inventory[i].rect.x, inventory[i].rect.y))
        pygame.display.flip()
    if not can_move and current_time - last_move_time > cooldown:
        can_move = True
    clock.tick(60)
