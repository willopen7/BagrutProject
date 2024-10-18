import pygame
import objects
import random

DESIRED_CALM = 50


def check_position(direction, sprites, auras, calm, player_pos=(400, 400),
                   tile_size=80):  # checks the position of all sprites before moving them so that they won't collide with player
    for sprite in sprites:
        if sprite.__class__ == objects.Portal:
            return True
        if (direction == 'UP' and player_pos[0] == sprite.rect.x and sprite.rect.y == player_pos[1] - tile_size) \
                or (
                direction == 'DOWN' and player_pos[0] == sprite.rect.x and sprite.rect.y == player_pos[1] + tile_size) \
                or (
                direction == 'LEFT' and player_pos[1] == sprite.rect.y and sprite.rect.x == player_pos[0] - tile_size) \
                or (
                direction == 'RIGHT' and player_pos[1] == sprite.rect.y and sprite.rect.x == player_pos[0] + tile_size):
            return False
    for aura in auras:
        if aura.near_main is True and calm < DESIRED_CALM:
            return False
    return True


def check_action(popup_details, sprite, all_sprites, all_auras, mcf, inventory, tile_size, player_pos):
    if sprite.__class__ == objects.Box:
        # popup_details[0] = True
        # popup_details[1] = pygame.image.load("C:\\Users\\User\\Downloads\\Champion_Chest.webp")
        open_chest(inventory)
        all_sprites.remove(sprite)
    if sprite.__class__ == objects.Store:
        popup_details[0] = True
        popup_details[1] = pygame.image.load("C:\\Users\\User\\Downloads\\inside_store.jpg")
    if sprite.__class__ == objects.Gate:
        all_sprites.remove(sprite)
    if sprite.__class__ == objects.Fountain:
        mcf[0] += int((mcf[1] + mcf[2]) / 2)
        all_sprites.remove(sprite)
    if sprite.__class__ == objects.Portal:
        all_sprites.update("", tile_size, player_pos[0], player_pos[1], portal=True)
        all_auras.update("", tile_size, player_pos[0], player_pos[1], portal=True)


def open_chest(inventory):
    chance = random.randint(1, 100)
    if chance > 60:
        inventory[1].amount += 1
    else:
        inventory[0].amount += 1