import pygame

DESIRED_CALM = 50
def check_position(direction, sprites, auras, calm, player_pos=(400, 400), tile_size=80):  # checks the position of all sprites before moving them so that they won't collide with player
    for sprite in sprites:
        if (direction == 'UP' and player_pos[0] == sprite.rect.x and sprite.rect.y == player_pos[1] - tile_size) \
                or (direction == 'DOWN' and player_pos[0] == sprite.rect.x and sprite.rect.y == player_pos[1] + tile_size) \
                or (direction == 'LEFT' and player_pos[1] == sprite.rect.y and sprite.rect.x == player_pos[0] - tile_size) \
                or (direction == 'RIGHT' and player_pos[1] == sprite.rect.y and sprite.rect.x == player_pos[0] + tile_size):
            return False
    for aura in auras:
        if aura.near_main is True and calm < DESIRED_CALM:
            return False
    return True
