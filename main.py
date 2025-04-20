# main.py
import sys
import pygame
import objects
import funcs
import threading
import ble_connection


# running the game
def game_loop():
    # initialize the game
    pygame.init()
    pygame.font.init()

    # CONSTANTS
    SCREEN_HEIGHT = 880
    SCREEN_WIDTH = 880
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GRAY = (200, 200, 200)
    RED = (255, 0, 0)
    running = False
    INITIAL_TILE_SIZE = 80
    PLAYER_X = 400
    PLAYER_Y = 400
    MONEY_POS = (10, 10)
    COOLDOWN_WITHOUT_SHOES = 500
    FONT_SIZE = 20
    FONT = pygame.font.Font("fonts\\PixelifySans-Medium.ttf", FONT_SIZE)
    FONT_INVENTORY_SIZE = 12
    FONT_INVENTORY = pygame.font.Font("fonts\\PixelifySans-Medium.ttf", FONT_INVENTORY_SIZE)
    FONT_STORE_SIZE = 40
    FONT_STORE = pygame.font.Font("fonts\\PixelifySans-Medium.ttf", FONT_STORE_SIZE)
    INVENTORY_POS = (10, SCREEN_HEIGHT - INITIAL_TILE_SIZE - FONT_SIZE)
    MAP_COOLDOWN = 2000
    POTIONS_DURATION = 10000
    POTIONS_BOOST = 25
    SHOES_IMAGE_PATH = "icons\\shoe.png"
    MAP_IMAGE_PATH = "icons\\map.png"
    KEY_IMAGE_PATH = "icons\\key.png"
    COMPASS_IMAGE_PATH = "icons\\compass.png"
    CALM_POTION_PATH = "icons\\calm_potion.png"
    FOCUS_POTION_PATH = "icons\\focus_potion.png"
    END_SHARD_PATH = "icons\\end_shard.png"
    TOTAL_SHARDS = 8
    ITEMS_PRICES = [15, 30, 30, 20, 10, 10]  # [0] is shoes, [1] is map, [2] is key, [3] is compass, [4] is calm potion, [5] is focus potion

    # VARIABLES
    mcf = [50, 60, 60]  # [0] is money, [1] is calm and [2] is focus
    current_tile_size = INITIAL_TILE_SIZE
    inventory = [
        objects.InventoryItem(0, SCREEN_HEIGHT - INITIAL_TILE_SIZE, INITIAL_TILE_SIZE, INITIAL_TILE_SIZE,
                              SHOES_IMAGE_PATH),
        objects.InventoryItem(INITIAL_TILE_SIZE, SCREEN_HEIGHT - INITIAL_TILE_SIZE, INITIAL_TILE_SIZE,
                              INITIAL_TILE_SIZE,
                              MAP_IMAGE_PATH),
        objects.InventoryItem(INITIAL_TILE_SIZE * 2, SCREEN_HEIGHT - INITIAL_TILE_SIZE, INITIAL_TILE_SIZE,
                              INITIAL_TILE_SIZE, KEY_IMAGE_PATH),
        objects.InventoryItem(INITIAL_TILE_SIZE * 3, SCREEN_HEIGHT - INITIAL_TILE_SIZE, INITIAL_TILE_SIZE,
                              INITIAL_TILE_SIZE, COMPASS_IMAGE_PATH),
        objects.InventoryItem(INITIAL_TILE_SIZE * 4, SCREEN_HEIGHT - INITIAL_TILE_SIZE, INITIAL_TILE_SIZE,
                              INITIAL_TILE_SIZE, CALM_POTION_PATH),
        objects.InventoryItem(INITIAL_TILE_SIZE * 5, SCREEN_HEIGHT - INITIAL_TILE_SIZE, INITIAL_TILE_SIZE,
                              INITIAL_TILE_SIZE, FOCUS_POTION_PATH),
        objects.InventoryItem(INITIAL_TILE_SIZE * (SCREEN_WIDTH // INITIAL_TILE_SIZE - 1),
                              SCREEN_HEIGHT - INITIAL_TILE_SIZE, INITIAL_TILE_SIZE,
                              INITIAL_TILE_SIZE, END_SHARD_PATH)]
    # [0] is shoes, [1] is map, [2] is key, [3] is compass, [4] is calm potion, [5] is focus potion
    NUM_SLOTS = len(inventory)
    can_move = True # after moving, the player has a tiny cooldown depends on the amount of shoes owned. Stores whether the cooldown is on
    map_is_used = False
    calm_potion_active = False
    focus_potion_active = False
    last_calm_potion_use = 0 # stores last calm potion use time
    last_focus_potion_use = 0 # stores last focus potion use time
    shoes_cooldown = COOLDOWN_WITHOUT_SHOES
    last_move_time = 0 # last time the player moved
    last_map_use = 0
    arrow = None
    arrow_shown = False
    store_popup = [False]  # a list for passing by reference if a store is opened
    not_enough_money = False # if the player tries to buy sth unseccessfully
    enough_money = False # if the player buys sth
    current_position = [75, 48]
    types_of_blocks = {'0': objects.Grass, '1': objects.Wall, '2': objects.Box, '3': objects.Fountain,
                       '4': objects.Store, '5': objects.SpecialBox, '6': objects.Gate, '7': objects.Monk,
                       '8': objects.EndGrass}
    opening_screen = True # a variable that's on during the opening screen
    ending_screen = False # a variable that's on during the ending screen
    play_button_rect = pygame.Rect(INITIAL_TILE_SIZE * ((SCREEN_WIDTH // INITIAL_TILE_SIZE) / 2 - 1),
                                   INITIAL_TILE_SIZE * ((SCREEN_HEIGHT // INITIAL_TILE_SIZE) / 2 - 0.5),
                                   INITIAL_TILE_SIZE * 2, INITIAL_TILE_SIZE)

    # pygame setup
    screen = pygame.display.set_mode((SCREEN_HEIGHT, SCREEN_WIDTH))
    pygame.display.set_caption("Mind Quest")
    clock = pygame.time.Clock()

    # TEXTS
    play_text = FONT.render("PLAY", True, BLACK)
    game_opening_text = FONT_STORE.render("MIND QUEST", True, WHITE)
    game_ending_text = FONT_STORE.render("WELL DONE!", True, WHITE)
    welcome_text = ["Welcome to Mind Quest!", "You found yourself trapped in this mysterious island", "and you have to find your way out", "", "", "Use the arrow keys to navigate"]
    welcome_text_boxes = []
    for i in range(len(welcome_text)):
        welcome_text_boxes.append(objects.TextBox(FONT, welcome_text[i], (80, 180+FONT_SIZE*i), True, screen))
    all_texts = pygame.sprite.Group()
    for i in welcome_text_boxes:
        all_texts.add(i)
    message = [""] # message for after getting something from a box
    message_portal = [""]

    # map setup
    all_sprites = pygame.sprite.Group() # a group for all the sprites
    all_auras = pygame.sprite.Group() # a group for the monk aura
    all_grass = pygame.sprite.Group() # a group for the walkable grass
    all_rendered = pygame.sprite.Group() # a group for just the rendered sprites
    rendered_grass = pygame.sprite.Group() # a group for the rendered grass
    rendered_auras = pygame.sprite.Group() # a group for the rendered auras
    boxes = []
    # cur_obj = None
    map_coords = funcs.generate_map_txt(types_of_blocks, 'map.txt', INITIAL_TILE_SIZE, all_sprites,
                                        all_grass, all_auras, boxes=boxes) # map generation
    # generating special objects
    funcs.create_portals(all_sprites)
    end_gate = objects.EndGate((17, 48), current_tile_size, current_tile_size)
    all_sprites.add(end_gate)
    end_portal = objects.EndPortal((16, 49), current_tile_size * 3, current_tile_size * 3)
    all_sprites.add(end_portal)
    main_char = objects.MainChar(PLAYER_X, PLAYER_Y, INITIAL_TILE_SIZE, INITIAL_TILE_SIZE)
    main_chars = pygame.sprite.Group()
    main_chars.add(main_char)
    inventory_slots = pygame.sprite.Group()
    for i in range(NUM_SLOTS - 1):
        slot = objects.InventorySlot(INITIAL_TILE_SIZE * i, SCREEN_HEIGHT - INITIAL_TILE_SIZE, INITIAL_TILE_SIZE,
                                     INITIAL_TILE_SIZE)
        inventory_slots.add(slot)
        inventory_slots.add(inventory[i])
    slot = objects.InventorySlot(INITIAL_TILE_SIZE * (SCREEN_WIDTH // INITIAL_TILE_SIZE - 1),
                                 SCREEN_HEIGHT - INITIAL_TILE_SIZE, INITIAL_TILE_SIZE,
                                 INITIAL_TILE_SIZE)
    inventory_slots.add(slot)
    inventory_slots.add(inventory[len(inventory) - 1])
    all_sprites.update(current_position, all_rendered, rendered_grass, rendered_auras)
    all_grass.update(current_position, all_rendered, rendered_grass, rendered_auras)
    all_auras.update(current_position, all_rendered, rendered_grass, rendered_auras)
    all_rendered.draw(screen)
    rendered_grass.draw(screen)
    rendered_auras.draw(screen)

    # opening screen
    while opening_screen:
        mouse_pos = pygame.mouse.get_pos()
        button_color = GRAY if play_button_rect.collidepoint(mouse_pos) else WHITE
        screen.fill(BLACK)
        pygame.draw.rect(screen, button_color, play_button_rect, border_radius=10)
        screen.blit(play_text, (play_button_rect.x + 55, play_button_rect.y + 30))
        screen.blit(game_opening_text, (330, 340))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                opening_screen = False
                sys.exit(0)
            if event.type == pygame.MOUSEBUTTONDOWN and play_button_rect.collidepoint(mouse_pos):
                running = True
                opening_screen = False
        pygame.display.flip()

    while running:  # an infinite loop for keeping the game running
        current_time = pygame.time.get_ticks()
        for event in pygame.event.get():  # a loop for all the events (mouse movement, key press etc.) that are happening
            if event.type == pygame.QUIT:
                running = False
                sys.exit(0)
            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT):
                    # for each of the arrows, the program checks whether a move can be made (the player doesn't collide with a map object) and then moves all the objects in the opposite direction, making it seem like the player moved
                    arrow_shown = False
                    store_popup[0] = False
                    not_enough_money = False
                    enough_money = False
                    for i in welcome_text_boxes:
                        if i.rendered:
                            i.rendered = False
                    if message[0] != "":
                        message[0] = ""
                    if message_portal[0] != "":
                        message_portal[0] = ""
                    if event.key == pygame.K_UP:
                        if funcs.check_position("UP", all_sprites, all_auras, mcf, current_position, message_portal,
                                                tile_size=current_tile_size) and (can_move or map_is_used):
                            current_position[1] -= 1
                            can_move = False
                            last_move_time = current_time
                            main_char.image = main_char.image_back
                            main_char.image = pygame.transform.scale(main_char.image,
                                                                     (current_tile_size, current_tile_size))
                    elif event.key == pygame.K_DOWN:
                        if funcs.check_position("DOWN", all_sprites, all_auras, mcf, current_position, message_portal,
                                                tile_size=current_tile_size) and (can_move or map_is_used):
                            current_position[1] += 1
                            can_move = False
                            last_move_time = current_time
                            main_char.image = main_char.image_front
                            main_char.image = pygame.transform.scale(main_char.image,
                                                                     (current_tile_size, current_tile_size))
                    elif event.key == pygame.K_LEFT:
                        if funcs.check_position("LEFT", all_sprites, all_auras, mcf, current_position, message_portal,
                                                tile_size=current_tile_size) and (can_move or map_is_used):
                            current_position[0] -= 1
                            can_move = False
                            last_move_time = current_time
                            main_char.image = main_char.image_left
                            main_char.image = pygame.transform.scale(main_char.image,
                                                                     (current_tile_size, current_tile_size))
                    elif event.key == pygame.K_RIGHT:
                        if funcs.check_position("RIGHT", all_sprites, all_auras, mcf, current_position, message_portal,
                                                tile_size=current_tile_size) and (can_move or map_is_used):
                            current_position[0] += 1
                            can_move = False
                            last_move_time = current_time
                            main_char.image = main_char.image_right
                            main_char.image = pygame.transform.scale(main_char.image,
                                                                     (current_tile_size, current_tile_size))
                    all_sprites.update(current_position, all_rendered, rendered_grass, rendered_auras)
                    all_auras.update(current_position, all_rendered, rendered_grass, rendered_auras)
                    all_grass.update(current_position, all_rendered, rendered_grass, rendered_auras)
                elif event.key == pygame.K_m and inventory[1].amount > 0 and not store_popup[
                    0]:  # pressing 'm' uses the map, making the render distance bigger for a limited duration
                    current_tile_size = int(INITIAL_TILE_SIZE / 2)
                    all_sprites.update(current_position, all_rendered, rendered_grass, rendered_auras, map_use=True)
                    all_auras.update(current_position, all_rendered, rendered_grass, rendered_auras, map_use=True)
                    all_grass.update(current_position, all_rendered, rendered_grass, rendered_auras, map_use=True)
                    main_chars.update(True, False)
                    last_map_use = current_time
                    map_is_used = True
                    inventory[1].amount -= 1
                elif event.key == pygame.K_c and inventory[3].amount > 0 and boxes and not store_popup[
                    0]:  # pressing 'c' uses the compass, revealing the closest box if there's any
                    closest_box = funcs.find_closest_box(boxes, PLAYER_X, PLAYER_Y, current_position)
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
                    arrow = objects.CompassArrow(
                        (current_position[0] + arrow_position[0], current_position[1] + arrow_position[1]),
                        current_tile_size, current_tile_size)
                    arrow.change_arrow(direction)
                    arrow_shown = True
                    inventory[3].amount -= 1
                elif event.key == pygame.K_1 and (
                        (inventory[4].amount > 0 and calm_potion_active is False) or store_popup[0]):  # if store is opened pressing 1 will try to buy shoes, otherwise it uses a calm potion
                    if store_popup[0]:
                        if mcf[0] >= ITEMS_PRICES[0]:
                            inventory[0].amount += 1
                            mcf[0] -= ITEMS_PRICES[0]
                            not_enough_money = False
                            enough_money = True
                        else:
                            not_enough_money = True
                            enough_money = False
                    else:
                        calm_potion_active = True
                        last_calm_potion_use = current_time
                        mcf[1] += POTIONS_BOOST
                        inventory[4].amount -= 1
                elif event.key == pygame.K_2 and (
                        (inventory[5].amount > 0 and focus_potion_active is False) or store_popup[0]):  # if store is opened pressing 2 will try to buy a map, otherwise it uses a focus potion
                    if store_popup[0]:
                        if mcf[0] >= ITEMS_PRICES[1]:
                            inventory[1].amount += 1
                            mcf[0] -= ITEMS_PRICES[1]
                            not_enough_money = False
                            enough_money = True
                        else:
                            not_enough_money = True
                            enough_money = False
                    else:
                        focus_potion_active = True
                        last_focus_potion_use = current_time
                        mcf[2] += POTIONS_BOOST
                        inventory[5].amount -= 1
                elif event.key == pygame.K_3 and store_popup[0]:  # pressing 3 while the store is opened buys a key
                    if mcf[0] >= ITEMS_PRICES[2]:
                        inventory[2].amount += 1
                        mcf[0] -= ITEMS_PRICES[2]
                        not_enough_money = False
                        enough_money = True
                    else:
                        not_enough_money = True
                        enough_money = False
                elif event.key == pygame.K_4 and store_popup[0]:  # pressing 4 while the store is opened buys a compass
                    if mcf[0] >= ITEMS_PRICES[3]:
                        inventory[3].amount += 1
                        mcf[0] -= ITEMS_PRICES[3]
                        not_enough_money = False
                        enough_money = True
                    else:
                        not_enough_money = True
                        enough_money = False
                elif event.key == pygame.K_5 and store_popup[0]:  # pressing 5 while the store is opened buys a calm potion
                    if mcf[0] >= ITEMS_PRICES[4]:
                        inventory[4].amount += 1
                        mcf[0] -= ITEMS_PRICES[4]
                        not_enough_money = False
                        enough_money = True
                    else:
                        not_enough_money = True
                        enough_money = False
                elif event.key == pygame.K_6 and store_popup[0]:  # pressing 6 while the store is opened buys a focus potion
                    if mcf[0] >= ITEMS_PRICES[5]:
                        inventory[5].amount += 1
                        mcf[0] -= ITEMS_PRICES[5]
                        not_enough_money = False
                        enough_money = True
                    else:
                        not_enough_money = True
                        enough_money = False
            screen.fill(BLACK)
            popup_details = [False,
                             None]  # a list to pass by reference if a popup window is needed [0] and the popup image [1]
            for sprite in all_rendered:  # a loop for checking whether the player is near an interactable map object (s.a. a box or a gate)
                if sprite.near_main is True:
                    funcs.check_action(popup_details, sprite, all_sprites, all_auras, all_grass, all_rendered,
                                       rendered_grass, rendered_auras, mcf, inventory, current_tile_size, boxes, store_popup, current_position, message)
                    if mcf[0] == -999:
                        running = False
                        ending_screen = True
                    shoes_cooldown = COOLDOWN_WITHOUT_SHOES / (2 ** inventory[0].amount)
            # draws all the objects onto the screen
            rendered_grass.draw(screen)
            rendered_auras.draw(screen)
            all_rendered.draw(screen)
            main_chars.draw(screen)
            if arrow_shown:
                arrow.rect.x = PLAYER_X + (arrow.obj_position[0] - current_position[0]) * current_tile_size
                arrow.rect.y = PLAYER_Y + (arrow.obj_position[1] - current_position[1]) * current_tile_size
                screen.blit(arrow.image, arrow.rect)
            if popup_details[0]:
                screen.blit(popup_details[1], (0, 0))
            inventory_slots.draw(screen)
            # prints the text based on the screen the player's in
            inventory_text = FONT.render(f"Inventory:", True, WHITE)
            screen.blit(FONT.render(f"Money: ${mcf[0]}", True, WHITE), MONEY_POS)
            if not store_popup[0]:
                focus_val, calm_val = ble_connection.get_focus_and_calm()
                mcf[1] = calm_val
                mcf[2] = focus_val
                if calm_potion_active:
                    mcf[1] += POTIONS_BOOST
                if focus_potion_active:
                    mcf[2] += POTIONS_BOOST
                screen.blit(FONT.render(f"Calm: {mcf[1]}", True, WHITE), (MONEY_POS[0], MONEY_POS[1] + FONT_SIZE))
                screen.blit(FONT.render(f"focus: {mcf[2]}", True, WHITE), (MONEY_POS[0], MONEY_POS[1] + FONT_SIZE * 2))
            else:
                screen.blit(FONT.render(f"Money: ${mcf[0]}", True, BLACK), (10, 10))
                inventory_text = FONT.render(f"Inventory:", True, BLACK)
                if not_enough_money:
                    screen.blit(FONT_STORE.render(f"NOT ENOUGH MONEY", True, RED),
                                (SCREEN_WIDTH / 2 - INITIAL_TILE_SIZE * 2.25, SCREEN_HEIGHT - INITIAL_TILE_SIZE * 1.75))
                if enough_money:
                    screen.blit(FONT_STORE.render(f"PURCHASE COMPLETE", True, BLACK),
                                (SCREEN_WIDTH / 2 - INITIAL_TILE_SIZE * 2.4, SCREEN_HEIGHT - INITIAL_TILE_SIZE * 1.75))
            screen.blit(inventory_text, INVENTORY_POS)
            for i in range(len(inventory) - 1):
                count_item = FONT_INVENTORY.render(f"{inventory[i].amount}", True, BLACK)
                screen.blit(count_item, (inventory[i].rect.x, inventory[i].rect.y))
            count_item = FONT_INVENTORY.render(f"{inventory[len(inventory) - 1].amount}/{TOTAL_SHARDS}", True, BLACK)
            screen.blit(count_item, (inventory[len(inventory) - 1].rect.x, inventory[len(inventory) - 1].rect.y))
            for text in all_texts:
                if text.rendered:
                    screen.blit(text.text, text.position)
            screen.blit(FONT.render(message[0], True, WHITE), (160, 20))
            screen.blit(FONT.render(message_portal[0], True, RED), (160, 20))
            pygame.display.flip()
        # checks if the wear-off effects are still on and if not turns them off
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
            all_sprites.update(current_position, all_rendered, rendered_grass, rendered_auras, map_end=True)
            all_grass.update(current_position, all_rendered, rendered_grass, rendered_auras, map_end=True)
            all_auras.update(current_position, all_rendered, rendered_grass, rendered_auras, map_end=True)
            main_chars.update(False, True)
        clock.tick(70)

    while ending_screen:
        screen.fill(BLACK)
        screen.blit(game_ending_text, (330, 340))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                ending_screen = False
                sys.exit(0)


if __name__ == "__main__":
    ble_thread = threading.Thread(target=ble_connection.start_ble_thread, daemon=True)
    ble_thread.start()
    game_loop()
