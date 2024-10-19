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
INITIAL_TILE_SIZE = 80
GRID_WIDTH = SCREEN_WIDTH // INITIAL_TILE_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // INITIAL_TILE_SIZE
PLAYER_X = 400
PLAYER_Y = 400
MONEY_POS = (10, 10)
INVENTORY_POS = (10, SCREEN_HEIGHT-INITIAL_TILE_SIZE-40)
COOLDOWN_WITHOUT_SHOES = 500
FONT = pygame.font.Font(None, 20)
MAP_COOLDOWN = 2000
POTIONS_DURATION = 10000
POTIONS_BOOST = 10
SHOES_IMAGE_PATH = "C:\\Users\\User\\Downloads\\shoes.png"
MAP_IMAGE_PATH = "C:\\Users\\User\\Downloads\\map-removebg-preview.png"
KEY_IMAGE_PATH = "C:\\Users\\User\\Downloads\\key-removebg-preview.png"
COMPASS_IMAGE_PATH = "C:\\Users\\User\\Downloads\\compass-icon-vector-simple-91662698-removebg-preview.png"
CALM_POTION_PATH = "C:\\Users\\User\\Downloads\\calm_potion.png"
FOCUS_POTION_PATH = "C:\\Users\\User\\Downloads\\focus_potion.png"

# VARIABLES
mcf = [10, 40, 0] # [0] is money, [1] is calm and [2] is focus
current_tile_size = INITIAL_TILE_SIZE
inventory = [objects.InventoryItem(0, SCREEN_HEIGHT-INITIAL_TILE_SIZE, INITIAL_TILE_SIZE, INITIAL_TILE_SIZE, SHOES_IMAGE_PATH),
             objects.InventoryItem(INITIAL_TILE_SIZE, SCREEN_HEIGHT-INITIAL_TILE_SIZE, INITIAL_TILE_SIZE, INITIAL_TILE_SIZE, MAP_IMAGE_PATH),
             objects.InventoryItem(INITIAL_TILE_SIZE*2, SCREEN_HEIGHT-INITIAL_TILE_SIZE, INITIAL_TILE_SIZE, INITIAL_TILE_SIZE, KEY_IMAGE_PATH),
             objects.InventoryItem(INITIAL_TILE_SIZE*3, SCREEN_HEIGHT-INITIAL_TILE_SIZE, INITIAL_TILE_SIZE, INITIAL_TILE_SIZE, COMPASS_IMAGE_PATH),
             objects.InventoryItem(INITIAL_TILE_SIZE*4, SCREEN_HEIGHT-INITIAL_TILE_SIZE, INITIAL_TILE_SIZE, INITIAL_TILE_SIZE, CALM_POTION_PATH),
             objects.InventoryItem(INITIAL_TILE_SIZE*5, SCREEN_HEIGHT-INITIAL_TILE_SIZE, INITIAL_TILE_SIZE, INITIAL_TILE_SIZE, FOCUS_POTION_PATH)]
# [0] is shoes, [1] is map, [2] is key, [3] is compass, [4] is calm potion, [5] is focus potion
inventory[4].amount += 1
inventory[5].amount += 1
NUM_SLOTS = len(inventory)

# pygame setup
screen = pygame.display.set_mode((SCREEN_HEIGHT, SCREEN_WIDTH))
clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()
all_auras = pygame.sprite.Group()
boxes = []
for i in range(100):
    box = objects.Box(random.randint(-100, 100)*INITIAL_TILE_SIZE, random.randint(-100, 100)*INITIAL_TILE_SIZE, INITIAL_TILE_SIZE, INITIAL_TILE_SIZE)
    boxes.append(box)
    all_sprites.add(box)
    wall = objects.Wall((i-10)*INITIAL_TILE_SIZE,2*INITIAL_TILE_SIZE, INITIAL_TILE_SIZE, INITIAL_TILE_SIZE)
    all_sprites.add(wall)
gate = objects.Gate(240, 240, INITIAL_TILE_SIZE, INITIAL_TILE_SIZE)
all_sprites.add(gate)
monk = objects.Monk(800, 800, INITIAL_TILE_SIZE, INITIAL_TILE_SIZE, INITIAL_TILE_SIZE)
all_sprites.add(monk)
store = objects.Store(-160, 720, INITIAL_TILE_SIZE, INITIAL_TILE_SIZE)
all_sprites.add(store)
fountain = objects.Fountain(400, 1040, INITIAL_TILE_SIZE, INITIAL_TILE_SIZE)
all_sprites.add(fountain)
portal = objects.Portal(320, -80, INITIAL_TILE_SIZE, INITIAL_TILE_SIZE)
all_sprites.add(portal)
all_auras.add(monk.monk_auras)
main_char = objects.MainChar(PLAYER_X, PLAYER_Y, INITIAL_TILE_SIZE, INITIAL_TILE_SIZE)
main_chars = pygame.sprite.Group()
main_chars.add(main_char)
can_move = True
map_is_used = False
compass_is_used = False
calm_potion_active = False
focus_potion_active = False
last_calm_potion_use = 0
last_focus_potion_use = 0
shoes_cooldown = COOLDOWN_WITHOUT_SHOES
last_move_time = 0
last_map_use = 0
inventory_slots = pygame.sprite.Group()
arrow = None
arrow_shown = False
for i in range(NUM_SLOTS):
    slot = objects.InventorySlot(INITIAL_TILE_SIZE*i, SCREEN_HEIGHT-INITIAL_TILE_SIZE, INITIAL_TILE_SIZE, INITIAL_TILE_SIZE)
    inventory_slots.add(slot)
    inventory_slots.add(inventory[i])

# running the game
while running:
    current_time = pygame.time.get_ticks()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT):
                arrow_shown = False
                if event.key == pygame.K_UP:
                    if funcs.check_position("UP", all_sprites, all_auras, mcf[1], (PLAYER_X, PLAYER_Y), current_tile_size) and can_move:
                        all_sprites.update("UP", current_tile_size, PLAYER_X, PLAYER_Y)
                        all_auras.update("UP", current_tile_size, PLAYER_X, PLAYER_Y)
                        can_move = False
                        last_move_time = current_time
                elif event.key == pygame.K_DOWN:
                    if funcs.check_position("DOWN", all_sprites, all_auras, mcf[1], (PLAYER_X, PLAYER_Y), current_tile_size) and can_move:
                        all_sprites.update("DOWN", current_tile_size, PLAYER_X, PLAYER_Y)
                        all_auras.update("DOWN", current_tile_size, PLAYER_X, PLAYER_Y)
                        can_move = False
                        last_move_time = current_time
                elif event.key == pygame.K_LEFT:
                    if funcs.check_position("LEFT", all_sprites, all_auras, mcf[1], (PLAYER_X, PLAYER_Y), current_tile_size) and can_move:
                        all_sprites.update("LEFT", current_tile_size, PLAYER_X, PLAYER_Y)
                        all_auras.update("LEFT", current_tile_size, PLAYER_X, PLAYER_Y)
                        can_move = False
                        last_move_time = current_time
                elif event.key == pygame.K_RIGHT:
                    if funcs.check_position("RIGHT", all_sprites, all_auras, mcf[1], (PLAYER_X, PLAYER_Y), tile_size=current_tile_size) and can_move:
                        all_sprites.update("RIGHT", current_tile_size, PLAYER_X, PLAYER_Y)
                        all_auras.update("RIGHT", current_tile_size, PLAYER_X, PLAYER_Y)
                        can_move = False
                    last_move_time = current_time
            elif event.key == pygame.K_m and inventory[1].amount > 0:
                current_tile_size = int(INITIAL_TILE_SIZE / 2)
                all_sprites.update("", current_tile_size, PLAYER_X, PLAYER_Y, portal=False, map_use=True)
                all_auras.update("", current_tile_size, PLAYER_X, PLAYER_Y, portal=False, map_use=True)
                main_chars.update(True, False)
                last_map_use = current_time
                map_is_used = True
                inventory[1].amount -= 1
            elif event.key == pygame.K_c and inventory[3].amount > 0:
                closest_box = funcs.find_closest_box(boxes, PLAYER_X, PLAYER_Y)
                direction = ''
                arrow_position = [0, 0]
                if closest_box.rect.y < PLAYER_Y:
                    direction += 'u'
                    arrow_position[1] -= 1
                elif closest_box.rect.y > PLAYER_Y:
                    direction += 'd'
                    arrow_position[1] += 1
                if closest_box.rect.x < PLAYER_X:
                    direction += 'l'
                    arrow_position[0] -= 1
                elif closest_box.rect.x > PLAYER_X:
                    direction += 'r'
                    arrow_position[0] += 1
                arrow = objects.CompassArrow(PLAYER_X+current_tile_size*arrow_position[0], PLAYER_Y+current_tile_size*arrow_position[1], current_tile_size, current_tile_size)
                arrow.change_arrow(direction)
                arrow_shown = True
                inventory[3].amount -= 1
            elif event.key == pygame.K_1 and inventory[4].amount > 0:
                calm_potion_active = True
                last_calm_potion_use = current_time
                mcf[1] += POTIONS_BOOST
                inventory[4].amount -= 1
            elif event.key == pygame.K_2 and inventory[5].amount > 0:
                focus_potion_active = True
                last_focus_potion_use = current_time
                mcf[2] += POTIONS_BOOST
                inventory[5].amount -= 1
        screen.fill(WHITE)
        if arrow_shown:
            screen.blit(arrow.image, arrow.rect)
        for x in range(current_tile_size, SCREEN_WIDTH, current_tile_size):
            pygame.draw.line(screen, GRAY, (x, 0), (x, SCREEN_HEIGHT))
        for y in range(current_tile_size, SCREEN_HEIGHT, current_tile_size):
            pygame.draw.line(screen, GRAY, (0, y), (SCREEN_WIDTH, y))
        popup_details = [False, None] # a list to pass by reference if a popup window is needed [0] and the popup image [1]
        for sprite in all_sprites:
            if sprite.near_main is True:
                funcs.check_action(popup_details, sprite, all_sprites, all_auras, mcf, inventory, current_tile_size, (PLAYER_X, PLAYER_Y), boxes)
                shoes_cooldown = COOLDOWN_WITHOUT_SHOES/(2**inventory[0].amount)
        all_auras.draw(screen)
        all_sprites.draw(screen)
        main_chars.draw(screen)
        inventory_slots.draw(screen)
        if popup_details[0]:
            screen.blit(popup_details[1], (0, 0))
        money_text = FONT.render(f"Money: ${mcf[0]}", True, BLACK)
        inventory_text = FONT.render(f"Inventory:", True, BLACK)
        screen.blit(money_text, MONEY_POS)
        screen.blit(FONT.render(f"Calm: {mcf[1]}", True, BLACK), (10, 80))
        screen.blit(FONT.render(f"focus: {mcf[2]}", True, BLACK), (10, 100))
        screen.blit(inventory_text, INVENTORY_POS)
        for i in range(len(inventory)):
            count_item = FONT.render(f"{inventory[i].amount}", True, BLACK)
            screen.blit(count_item, (inventory[i].rect.x, inventory[i].rect.y))
        pygame.display.flip()
    if calm_potion_active and current_time - last_calm_potion_use >= POTIONS_DURATION:
        mcf[1] -= POTIONS_BOOST
        calm_potion_active = False
    if focus_potion_active and current_time - last_focus_potion_use >= POTIONS_DURATION:
        mcf[2] -= POTIONS_BOOST
        focus_potion_active = False
    if not can_move and current_time - last_move_time > shoes_cooldown:
        can_move = True
    if map_is_used and current_time - last_map_use > MAP_COOLDOWN:
        map_is_used = False
        current_tile_size *= 2
        all_sprites.update("", current_tile_size, PLAYER_X, PLAYER_Y, portal=False, map_end=True)
        all_auras.update("", current_tile_size, PLAYER_X, PLAYER_Y, portal=False, map_end=True)
        main_chars.update(False, True)
    clock.tick(60)
