# objects.py
import pygame.sprite

import objects

RED = (255, 0, 0)
TILE_SIZE = 80
SCREEN_HEIGHT = 880
SCREEN_WIDTH = 880
BOX_PATH = "icons\\closed-box.png"
OPEN_BOX_PATH = "icons\\opened-box.png"
SPECIAL_BOX_PATH = "icons\\special_box_close.png"
SPECIAL_OPEN_BOX_PATH = "icons\\special_box_open.png"
END_GATE_PATH = "icons\\end_gate.png"
END_PORTAL_PATH = "icons\\end_portal.png"
PORTAL_PATH = "icons\\portal.webp"
GATE_PATH = "icons\\gate.png"
FOUNTAIN_PATH = "icons\\fountain.png"
GRASS_PATH = "icons\\grass.jpg"
END_GRASS_PATH = "icons\\end_grass2.png"
INVENTORY_SLOT_PATH = "icons\\InventorySlot.png"
MAIN_CHAR_PATH = "icons\\main_char-new.png"
MAIN_CHAR_FRONT_PATH = "icons\\main_char-front.png"
MAIN_CHAR_BACK_PATH = "icons\\main_char-back.png"
MONK_PATH = "icons\\monk.png"
MONK_AURA_PATH = "icons\\monk-aura.jpg"
STORE_PATH = "icons\\store.png"
WALL_PATH = "icons\\wall.png"
NO_TEXTURE_PATH = "icons\\notexture.png"
DIAGONAL_ARROW_PATH = "icons\\diagonal_arrow.png"
SIDE_ARROW_PATH = "icons\\side_arrow.png"
MAIN_CHAR_RENDERED_POS = (400, 400)


class MapObj(pygame.sprite.Sprite): # a super class for all the map objects
    def __init__(self, obj_position, width, height, path):
        super().__init__()
        self.path = path
        self.image = pygame.image.load(path)
        self.image = pygame.transform.scale(self.image, (width, height))
        self.image_normal = self.image.copy()
        self.original_size = (width, height)
        self.rect = self.image.get_rect()
        self.near_main = False
        self.obj_position = obj_position
        self.is_shown = False
        self.map_use = False

    def update(self, main_position, all_rendered, rendered_grass, rendered_auras, map_use=False, map_end=False):
        height = SCREEN_HEIGHT // TILE_SIZE
        width = SCREEN_WIDTH // TILE_SIZE
        self.rect.x = MAIN_CHAR_RENDERED_POS[0] + (self.obj_position[0] - main_position[0])*TILE_SIZE
        self.rect.y = MAIN_CHAR_RENDERED_POS[1] + (self.obj_position[1] - main_position[1]) * TILE_SIZE
        if map_use or self.map_use:
            self.map_use = True
            height = SCREEN_HEIGHT // TILE_SIZE * 2
            width *= SCREEN_WIDTH // TILE_SIZE * 2
            self.rect.x = MAIN_CHAR_RENDERED_POS[0] + ((self.obj_position[0]-main_position[0])/2)*TILE_SIZE
            self.rect.y = MAIN_CHAR_RENDERED_POS[1] + ((self.obj_position[1]-main_position[1])/2)*TILE_SIZE
            self.image = pygame.transform.scale(self.image,
                                                (self.original_size[0] / 2, self.original_size[1] / 2))
        if map_end:
            self.map_use = False
            self.rect.x = self.rect.x * 2 - MAIN_CHAR_RENDERED_POS[0]
            self.rect.y = self.rect.y * 2 - MAIN_CHAR_RENDERED_POS[1]
            self.image = self.image_normal.copy()
        if main_position[0] - width//2 <= self.obj_position[0] <= main_position[0] + width//2 and main_position[1] - height//2 <= self.obj_position[1] <= main_position[1] + height//2:
            if not self.is_shown:
                if self.__class__ == objects.Grass or self.__class__ == objects.EndGrass:
                    rendered_grass.add(self)
                elif self.__class__ == objects.MonkAura:
                    rendered_auras.add(self)
                else:
                    all_rendered.add(self)
                self.is_shown = True
        elif self.is_shown:
            if self.__class__ == objects.Grass or self.__class__ == objects.EndGrass:
                rendered_grass.remove(self)
            elif self.__class__ == objects.MonkAura:
                rendered_auras.remove(self)
            else:
                all_rendered.remove(self)
            self.is_shown = False
        if self.is_shown:
            if self.obj_position[0] + self.obj_position[1]-1 <= main_position[0] + main_position[1] <= self.obj_position[0] + self.obj_position[1]+1 and (self.obj_position[0] == main_position[0] or self.obj_position[1] == main_position[1]):
                self.near_main = True
            else:
                self.near_main = False


class Box(MapObj): # class of boxes/chests
    def __init__(self, obj_position, width, height):
        super().__init__(obj_position, width, height, BOX_PATH)
        self.opened = False
        self.opened_image = pygame.transform.scale(pygame.image.load(OPEN_BOX_PATH), self.original_size)

    def update(self, main_position, all_rendered, rendered_grass, rendered_auras, map_use=False, map_end=False):
        super().update(main_position, all_rendered, rendered_grass, rendered_auras, map_use, map_end)
        if map_end:
            if self.opened:
                self.image = self.opened_image


class SpecialBox(MapObj):
    def __init__(self, obj_position, width, height):
        super().__init__(obj_position, width, height, SPECIAL_BOX_PATH)
        self.opened = False
        self.opened_image = pygame.transform.scale(pygame.image.load(SPECIAL_OPEN_BOX_PATH), self.original_size)

    def update(self, main_position, all_rendered, rendered_grass, rendered_auras, map_use=False, map_end=False):
        super().update(main_position, all_rendered, rendered_grass, rendered_auras, map_use, map_end)
        if map_end:
            if self.opened:
                self.image = self.opened_image


class EndGate(MapObj):
    def __init__(self, obj_position, width, height):
        super().__init__(obj_position, width, height, END_GATE_PATH)

    def update(self, main_position, all_rendered, rendered_grass, rendered_auras, map_use=False, map_end=False):
        super().update(main_position, all_rendered, rendered_grass, rendered_auras, map_use, map_end)


class Store(MapObj):
    def __init__(self, obj_position, width, height):
        super().__init__(obj_position, width, height, STORE_PATH)

    def update(self, main_position, all_rendered, rendered_grass, rendered_auras, map_use=False, map_end=False):
        super().update(main_position, all_rendered, rendered_grass, rendered_auras, map_use, map_end)


class Wall(MapObj): # a class for the map borders or walls
    def __init__(self, obj_position, width, height):
        super().__init__(obj_position, width, height, WALL_PATH)

    def update(self, main_position, all_rendered, rendered_grass, rendered_auras, map_use=False, map_end=False):
        super().update(main_position, all_rendered, rendered_grass, rendered_auras, map_use, map_end)


class Gate(MapObj):
    def __init__(self, obj_position, width, height):
        super().__init__(obj_position, width, height, GATE_PATH)

    def update(self, main_position, all_rendered, rendered_grass, rendered_auras, map_use=False, map_end=False):
        super().update(main_position, all_rendered, rendered_grass, rendered_auras, map_use, map_end)


class Monk(MapObj):
    def __init__(self, obj_position, width, height):
        super().__init__(obj_position, width, height, MONK_PATH)
        self.monk_auras = pygame.sprite.Group()
        for i in range(-2, 3):
            for j in range(-2, 3):
                i
                aura = MonkAura((obj_position[0] + i, obj_position[1] + j), width, height)
                self.monk_auras.add(aura)

    def update(self, main_position, all_rendered, rendered_grass, rendered_auras, map_use=False, map_end=False):
        super().update(main_position, all_rendered, rendered_grass, rendered_auras, map_use, map_end)


class MonkAura(MapObj):
    def __init__(self, obj_position, width, height):
        super().__init__(obj_position, width, height, MONK_AURA_PATH)

    def update(self, main_position, all_rendered, rendered_grass, rendered_auras, map_use=False, map_end=False):
        super().update(main_position, all_rendered, rendered_grass, rendered_auras, map_use, map_end)


class Fountain(MapObj):
    def __init__(self, obj_position, width, height):
        super().__init__(obj_position, width, height, FOUNTAIN_PATH)

    def update(self, main_position, all_rendered, rendered_grass, rendered_auras, map_use=False, map_end=False):
        super().update(main_position, all_rendered, rendered_grass, rendered_auras, map_use, map_end)


class EndPortal(MapObj):
    def __init__(self, obj_position, width, height):
        super().__init__(obj_position, width, height, END_PORTAL_PATH)

    def update(self, main_position, all_rendered, rendered_grass, rendered_auras, map_use=False, map_end=False):
        super().update(main_position, all_rendered, rendered_grass, rendered_auras, map_use, map_end)


class Portal(MapObj):
    def __init__(self, obj_position, width, height, position_to_tranfer):
        super().__init__(obj_position, width, height, PORTAL_PATH)
        self.distance_x = position_to_tranfer[0] - obj_position[0]
        self.distance_y = position_to_tranfer[1] - obj_position[1]

    def update(self, main_position, all_rendered, rendered_grass, rendered_auras, map_use=False, map_end=False):
        super().update(main_position, all_rendered, rendered_grass, rendered_auras, map_use, map_end)


class MainChar(pygame.sprite.Sprite): # a class for the main character
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image_right = pygame.image.load(MAIN_CHAR_PATH)
        self.image_left = pygame.transform.flip(self.image_right, True, False)
        self.image_front = pygame.image.load(MAIN_CHAR_FRONT_PATH)
        self.image_back = pygame.image.load(MAIN_CHAR_BACK_PATH)
        self.image = self.image_right
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self, map_use, map_end):
        if map_use:
            self.image = pygame.transform.scale(self.image, (self.image.get_width() / 2, self.image.get_height() / 2))
        if map_end:
            self.image = pygame.transform.scale(pygame.image.load(MAIN_CHAR_PATH), (self.image.get_width() * 2, self.image.get_height() * 2))


class InventorySlot(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.image.load(INVENTORY_SLOT_PATH)
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class InventoryItem(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, image_path=NO_TEXTURE_PATH):
        super().__init__()
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (width/2, height/2))
        self.rect = self.image.get_rect()
        self.rect.x = x+width/4
        self.rect.y = y+width/4
        self.amount = 0


class CompassArrow(MapObj):
    def __init__(self, obj_position, width, height):
        super().__init__(obj_position, width, height, NO_TEXTURE_PATH)

    def change_arrow(self, direction):
        width = self.image.get_width()
        height = self.image.get_height()
        if len(direction) == 2:
            self.image = pygame.image.load(DIAGONAL_ARROW_PATH)
            self.image = pygame.transform.scale(self.image, (width, height))
            if direction == 'dl':
                self.image = pygame.transform.rotate(self.image, 270)
            elif direction == 'ul':
                self.image = pygame.transform.rotate(self.image, 180)
            elif direction == 'ur':
                self.image = pygame.transform.rotate(self.image, 90)
        elif len(direction) == 1:
            self.image = pygame.image.load(SIDE_ARROW_PATH)
            self.image = pygame.transform.scale(self.image, (width, height))
            if direction == 'd':
                self.image = pygame.transform.rotate(self.image, 270)
            elif direction == 'l':
                self.image = pygame.transform.rotate(self.image, 180)
            elif direction == 'u':
                self.image = pygame.transform.rotate(self.image, 90)

    def update(self, main_position, all_rendered, rendered_grass, rendered_auras, map_use=False, map_end=False):
        super().update(main_position, all_rendered, rendered_grass, rendered_auras, map_use, map_end)


class EndGrass(MapObj):
    def __init__(self, obj_position, width, height):
        super().__init__(obj_position, width, height, END_GRASS_PATH)

    def update(self, main_position, all_rendered, rendered_grass, rendered_auras, map_use=False, map_end=False):
        super().update(main_position, all_rendered, rendered_grass, rendered_auras, map_use, map_end)


class Grass(MapObj):
    def __init__(self, obj_position, width, height):
        super().__init__(obj_position, width, height, GRASS_PATH)

    def update(self, main_position, all_rendered, rendered_grass, rendered_auras, map_use=False, map_end=False):
        super().update(main_position, all_rendered, rendered_grass, rendered_auras, map_use, map_end)


class TextBox(pygame.sprite.Sprite):
    def __init__(self, font: pygame.font.Font, text, position, rendered, screen, color=(255, 255, 255)):
        super().__init__()
        self.text = font.render(text, True, color)
        self.text = self.text.convert_alpha(screen)
        self.position = position
        self.rendered = rendered
        self.alpha = 255
        self.text.set_alpha(self.alpha)

    def update(self):
        if self.rendered:
            self.rendered = False
            '''
            self.on = False
            self.alpha -= 0.01
            if self.alpha <= 0:
                self.rendered = False
            self.text.set_alpha(self.alpha)'''
