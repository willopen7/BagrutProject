# funcs.py
import pygame
import objects
import random

DESIRED_CALM_AURA = 50
DESIRED_CALM_PORTAL = 50
DESIRED_FOCUS_PORTAL = 50
SMALL_MONEY = 5
MEDIUM_MONEY = 10
BIG_MONEY = 15
HUGE_MONEY = 30
OPEN_BOX_PATH = "icons\\opened-box.png"
SPECIAL_OPEN_BOX_PATH = "icons\\special_box_open.png"
STORE_IN_GAME_PATH = "icons\\store_in_game4.png"
types_of_blocks = {'0': objects.Grass, '1': objects.Wall, '2': objects.Box, '3': objects.Fountain, '4': objects.Store, '5': objects.SpecialBox, '6': objects.Gate, '7': objects.Monk}


def check_position(direction, sprites, auras, mcf, current_position, message_portal, player_pos=(400, 400),
                   tile_size=80):  # checks the position of all sprites before moving them so that they won't collide with player
    for sprite in sprites:
        if sprite.__class__ != objects.Portal and (
                (direction == 'UP' and current_position[0] == sprite.obj_position[0] and current_position[1] == sprite.obj_position[1] + 1)
                or (direction == 'DOWN' and current_position[0] == sprite.obj_position[0] and current_position[1] == sprite.obj_position[1] - 1)
                or (direction == 'LEFT' and current_position[1] == sprite.obj_position[1] and current_position[0] == sprite.obj_position[0] + 1)
                or (direction == 'RIGHT' and current_position[1] == sprite.obj_position[1] and current_position[0] == sprite.obj_position[0] - 1)):
            return False
        if sprite.__class__ == objects.Portal and (mcf[1] < DESIRED_CALM_PORTAL or mcf[2] < DESIRED_FOCUS_PORTAL):
            if mcf[1] < DESIRED_CALM_PORTAL:
                message_portal[0] = "You need to be calmer to enter through the portal"
            elif mcf[2] < DESIRED_FOCUS_PORTAL:
                message_portal[0] = "You need to be more focused to enter through the portal"
            return False
    for aura in auras:
        if aura.near_main is True and mcf[1] < DESIRED_CALM_AURA:
            return False
    return True


def check_action(popup_details, sprite, all_sprites, all_auras, all_grass, all_rendered, rendered_grass, rendered_auras, mcf, inventory, tile_size, boxes, store_popup, current_position, message): # checks which class is a specific sprite which is near the player and acts correspondingly
    if sprite.__class__ == objects.Box and sprite in boxes:
        open_box(inventory, mcf, message)
        boxes.remove(sprite)
        sprite.image = pygame.transform.scale(pygame.image.load(OPEN_BOX_PATH), (tile_size, tile_size))
        sprite.opened = True
    if sprite.__class__ == objects.Store:
        popup_details[0] = True
        popup_details[1] = pygame.transform.scale(pygame.image.load(STORE_IN_GAME_PATH), (880, 880))
        store_popup[0] = True
    if sprite.__class__ == objects.Gate and inventory[2].amount > 0:
        all_sprites.remove(sprite)
        all_rendered.remove(sprite)
        inventory[2].amount -= 1
    if sprite.__class__ == objects.Fountain:
        mcf[0] += int((mcf[1] + mcf[2]) / 2)
        all_sprites.remove(sprite)
        all_rendered.remove(sprite)
    if sprite.__class__ == objects.Portal and current_position[0] == sprite.obj_position[0] and current_position[1] == sprite.obj_position[1]:
        current_position[0] += sprite.distance_x
        current_position[1] += sprite.distance_y
        all_grass.update(current_position, all_rendered, rendered_grass, rendered_auras)
        all_auras.update(current_position, all_rendered, rendered_grass, rendered_auras)
        all_sprites.update(current_position, all_rendered, rendered_grass, rendered_auras)
    if sprite.__class__ == objects.SpecialBox and not sprite.opened:
        inventory[len(inventory)-1].amount += 1
        sprite.image = pygame.transform.scale(pygame.image.load(SPECIAL_OPEN_BOX_PATH), (tile_size, tile_size))
        sprite.opened = True
        message[0] = "You got an end shard! You need to collect 8 to open the end gate"
    if sprite.__class__ == objects.EndGate and inventory[len(inventory)-1].amount >= 8:
        all_sprites.remove(sprite)
        all_rendered.remove(sprite)
        inventory[len(inventory)-1].amount = 0
    if sprite.__class__ == objects.EndPortal:
        mcf[0] = -999


def open_box(inventory, mcf, message): # creates a random variable to decide the item the player recieves from a box
    sum = 0
    for i in range(6):
        sum += (5 - inventory[i].amount)
    chance = random.randint(1, 100)
    print(chance)
    if chance > 85:
        mcf[0] += SMALL_MONEY
        message[0] = f"You got {SMALL_MONEY}$. Use it in the shop!"
    elif chance > 80:
        mcf[0] += BIG_MONEY
        message[0] = f"You got {BIG_MONEY}$. Use it in the shop!"
    elif chance > 72:
        mcf[0] += MEDIUM_MONEY
        message[0] = f"You got {MEDIUM_MONEY}$. Use it in the shop!"
    elif chance > 70:
        mcf[0] += HUGE_MONEY
        message[0] = f"You got {HUGE_MONEY}$. Use it in the shop!"
    elif chance > 55:
        inventory[0].amount += 1  # player gets shoes
        message[0] = "You got shoes! These make you go faster"
    elif chance > 45:
        inventory[4].amount += 1  # player gets a calm potion
        message[0] = "You got a calm potion! To boost your calm levels press 1"
    elif chance > 35:
        inventory[5].amount += 1  # player gets a focus potion
        message[0] = "You got a focus potion! To boost your focus levels press 2"
    elif chance > 28:
        inventory[3].amount += 1  # player gets a compass
        message[0] = "You got a compass! To find the nearest box press 'c'"
    elif chance > 22:
        inventory[1].amount += 1  # player gets a map
        message[0] = "You got a map! To have a bigger render distance press 'm'"
    elif chance > 15:
        inventory[2].amount += 1  # player gets a key
        message[0] = "You got a key! These help you open gates"
    elif inventory[0].amount >= 2 and chance > 7:
        inventory[1].amount += 1  # player gets a map
        message[0] = "You got a map! To have a bigger render distance press 'm'"
    elif inventory[0].amount >= 2:
        inventory[2].amount += 1  # player gets a key
        message[0] = "You got a key! These help you open gates"
    else:
        inventory[0].amount += 1
        message[0] = "You got shoes! These make you go faster"


def find_closest_box(boxes, player_x, player_y, current_position): # a function for the compass object that finds the closest box to the player
    if len(boxes) == 0:
        return None
    closest_box = boxes[0]
    closest_distance = abs(boxes[0].obj_position[0] - current_position[0]) + abs(boxes[0].obj_position[1] - current_position[1])
    for b in boxes:
        cur = abs(b.obj_position[0] - current_position[0]) + abs(b.obj_position[1] - current_position[1])
        if cur < closest_distance:
            closest_box = b
            closest_distance = cur
    return closest_box


def generate_map_txt(types_of_blocks: dict, coordinates, tile_size, all_sprites, all_grass, all_auras, boxes=None): # generates the blocks based of a txt file. If I have time in the future i want to add a feature that renders only the necessary blocks
    with open(coordinates, "r") as coords:
        map_blocks = coords.readlines()
        for i in range(len(map_blocks)):
            map_blocks[i] = map_blocks[i].split(" ")
            map_blocks[i][-1] = map_blocks[i][-1][0]
        for i in range(len(map_blocks)):
            for j in range(len(map_blocks[i])):
                if map_blocks[i][j] == '5':
                    print('yo!')
                if map_blocks[i][j] != '9':
                    cur_obj = types_of_blocks[map_blocks[i][j]]((j, i), tile_size, tile_size)
                    if types_of_blocks[map_blocks[i][j]] == objects.Grass or types_of_blocks[map_blocks[i][j]] == objects.EndGrass:
                        all_grass.add(cur_obj)
                    else:
                        all_sprites.add(cur_obj)
                        all_grass.add(objects.Grass((j, i), tile_size, tile_size))
                    if types_of_blocks[map_blocks[i][j]] == objects.Box:
                        boxes.append(cur_obj)
                    elif types_of_blocks[map_blocks[i][j]] == objects.Monk:
                        all_auras.add(cur_obj.monk_auras)
    return map_blocks


def create_portals(all_sprites):
    portals = [((72, 51), (62, 7)), ((43, 21), (72, 33)), ((74, 33), (49, 25)), ((43, 42), (10, 35)), ((11, 35), (40, 45)), ((35, 12), (14, 27)), ((16, 27), (35, 8)), ((27, 23), (30, 40)), ((31, 40), (25, 22)), ((46, 16), (40, 49)), ((43, 49), (46, 15)), ((56, 36), (34, 35)), ((27, 33), (56, 37)), ((11, 33), (18, 7)), ((18, 8), (15, 33)), ((1, 22), (84, 20)), ((84, 18), (1, 19))]
    for p in range(len(portals)):
        cur_obj = objects.Portal(portals[p][0], 80, 80, portals[p][1])
        all_sprites.add(cur_obj)
