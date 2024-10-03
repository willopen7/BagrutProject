import pygame


def check_position(direction, sprites, main_pos=(400, 400), grid_size=80):
    for sprite in sprites:
        if (direction == 'UP' and main_pos[0] == sprite.rect.x and sprite.rect.y == main_pos[1] - grid_size) \
                or (direction == 'DOWN' and main_pos[0] == sprite.rect.x and sprite.rect.y == main_pos[1] + grid_size) \
                or (direction == 'LEFT' and main_pos[1] == sprite.rect.y and sprite.rect.x == main_pos[0] - grid_size) \
                or (direction == 'RIGHT' and main_pos[1] == sprite.rect.y and sprite.rect.x == main_pos[0] + grid_size):
            return False
    return True
