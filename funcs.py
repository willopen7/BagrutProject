import pygame
import objects
import random

DESIRED_CALM = 50
SMALL_MONEY = 10
MEDIUM_MONEY = 20
BIG_MONEY = 30
HUGE_MONEY = 50


def check_position(direction, sprites, auras, calm, player_pos=(400, 400),
                   tile_size=80):  # checks the position of all sprites before moving them so that they won't collide with player
    for sprite in sprites:
        if sprite.__class__ != objects.Portal and (
                (direction == 'UP' and player_pos[0] == sprite.rect.x and sprite.rect.y == player_pos[1] - tile_size)
                or (
                        direction == 'DOWN' and player_pos[0] == sprite.rect.x and sprite.rect.y == player_pos[
                    1] + tile_size)
                or (
                        direction == 'LEFT' and player_pos[1] == sprite.rect.y and sprite.rect.x == player_pos[
                    0] - tile_size)
                or (
                        direction == 'RIGHT' and player_pos[1] == sprite.rect.y and sprite.rect.x == player_pos[
                    0] + tile_size)):
            return False
    for aura in auras:
        if aura.near_main is True and calm < DESIRED_CALM:
            return False
    return True


def check_action(popup_details, sprite, all_sprites, all_auras, mcf, inventory, tile_size, player_pos, boxes):
    if sprite.__class__ == objects.Box:
        # popup_details[0] = True
        # popup_details[1] = pygame.image.load("C:\\Users\\User\\Downloads\\Champion_Chest.webp")
        open_box(inventory, mcf)
        all_sprites.remove(sprite)
        boxes.remove(sprite)
    if sprite.__class__ == objects.Store:
        popup_details[0] = True
        popup_details[1] = pygame.image.load("C:\\Users\\User\\Downloads\\inside_store.jpg")
    if sprite.__class__ == objects.Gate and inventory[2].amount > 0:
        all_sprites.remove(sprite)
        inventory[2].amount -= 1
    if sprite.__class__ == objects.Fountain:
        mcf[0] += int((mcf[1] + mcf[2]) / 2)
        all_sprites.remove(sprite)
    if sprite.__class__ == objects.Portal:
        all_sprites.update("", tile_size, player_pos[0], player_pos[1], portal=True,
                           portal_properties=(sprite.distance_x, sprite.distance_y))
        all_auras.update("", tile_size, player_pos[0], player_pos[1], portal=True,
                         portal_properties=(sprite.distance_x, sprite.distance_y))


def open_box(inventory, mcf):
    chance = random.randint(1, 100)
    if chance > 95:
        inventory[1].amount += 1  # player gets a map
    elif chance > 85:
        inventory[0].amount += 1  # player gets shoes
    elif chance > 80:
        inventory[2].amount += 1  # player gets a key
    elif chance > 55:
        mcf[0] += SMALL_MONEY
    elif chance > 45:
        mcf[0] += MEDIUM_MONEY
    elif chance > 40:
        mcf[0] += BIG_MONEY
    elif chance > 38:
        mcf[0] += HUGE_MONEY
    elif chance > 30:
        inventory[3].amount += 1  # player gets a compass
    elif chance > 15:
        inventory[4].amount += 1  # player gets a calm potion
    else:
        inventory[5].amount += 1  # player gets a focus potion


def find_closest_box(boxes, player_x, player_y):
    if len(boxes) == 0:
        return None
    closest_box = boxes[0]
    closest_distance = abs(boxes[0].rect.x - player_x) + abs(boxes[0].rect.y - player_y)
    for b in boxes:
        cur = abs(b.rect.x - player_x) + abs(b.rect.y - player_y)
        if cur < closest_distance:
            closest_box = b
            closest_distance = cur
    return closest_box


def place_map_object_binary(all_sprites, object_type, places, start_coords, main_coords, tile_size, boxes=None):
    for i in range(len(places)):
        for j in range(len(places[i])):
            if places[i][j]:
                cur_obj = object_type(main_coords[0] - (start_coords[0] - j) * tile_size,
                                      main_coords[1] - (start_coords[1] - i) * tile_size,
                                      tile_size, tile_size)
                all_sprites.add(cur_obj)
                if object_type == objects.Box:
                    boxes.append(cur_obj)


def place_map_object_tuple(all_sprites, object_type, places, main_coords, tile_size, boxes=None):
    for i in range(len(places)):
        cur_obj = object_type(main_coords[0] + places[i][0] * tile_size, main_coords[1] + places[i][1] * tile_size,
                              tile_size, tile_size)
        all_sprites.add(cur_obj)
        if object_type == objects.Box:
            boxes.append(cur_obj)
