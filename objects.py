# objects.py
import pygame.sprite

RED = (255, 0, 0)
BOX_PATH = "icons\\closed-box.png"
OPEN_BOX_PATH = "icons\\opened-box.png"
PORTAL_PATH = "icons\\portal.webp"
GATE_PATH = "icons\\gate.png"
FOUNTAIN_PATH = "icons\\fountain.png"
GRASS_PATH = "icons\\grass.jpg"
INVENTORY_SLOT_PATH = "icons\\InventorySlot.png"
MAIN_CHAR_PATH = "icons\\main_char.png"
MONK_PATH = "icons\\monk.png"
MONK_AURA_PATH = "icons\\monk-aura.jpg"
STORE_PATH = "icons\\store.png"
WALL_PATH = "icons\\wall.png"
NO_TEXTURE_PATH = "icons\\notexture.png"
DIAGONAL_ARROW_PATH = "icons\\diagonal_arrow.png"
SIDE_ARROW_PATH = "icons\\side_arrow.png"


class MapObj(pygame.sprite.Sprite): # a super class for all the map objects
    def __init__(self):
        super().__init__()
        self.near_main = False

    def update(self, direct, size, player_x, player_y, portal=False, portal_properties=None):
        if direct == "UP":
            self.rect.y += size
        if direct == "DOWN":
            self.rect.y -= size
        if direct == "LEFT":
            self.rect.x += size
        if direct == "RIGHT":
            self.rect.x -= size
        if portal and portal_properties is not None:
            if len(portal_properties) == 2:
                self.rect.x += portal_properties[0]*size
                self.rect.y += portal_properties[1]*size
        if player_x + player_y - size <= self.rect.x + self.rect.y <= player_x + player_y + size and (self.rect.x == player_x or self.rect.y == player_y): # checks if the player is near the current map object
            self.near_main = True
        else:
            self.near_main = False


class Box(MapObj): # class of boxes/chests
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.image.load(BOX_PATH)
        self.image = pygame.transform.scale(self.image, (width, height))
        self.opened = False
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self, direct, size, player_x, player_y, portal=False, portal_properties=None, map_use=False, map_end=False):
        super().update(direct, size, player_x, player_y, portal, portal_properties)
        if map_use:
            self.rect.x = (self.rect.x + player_x) / 2
            self.rect.y = (self.rect.y + player_y) / 2
            self.image = pygame.transform.scale(self.image, (self.image.get_width()/2, self.image.get_height()/2))
        if map_end:
            self.rect.x = 2 * self.rect.x - player_x
            self.rect.y = 2 * self.rect.y - player_y
            if self.opened:
                self.image = pygame.transform.scale(pygame.image.load(OPEN_BOX_PATH), (self.image.get_width() * 2, self.image.get_height() * 2))
            else:
                self.image = pygame.transform.scale(pygame.image.load(BOX_PATH), (self.image.get_width() * 2, self.image.get_height() * 2))


class Store(MapObj):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.image.load(STORE_PATH)
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self, direct, size, player_x, player_y, portal=False, portal_properties=None, map_use=False, map_end=False):
        super().update(direct, size, player_x, player_y, portal, portal_properties)
        if map_use:
            self.rect.x = (self.rect.x + player_x) / 2
            self.rect.y = (self.rect.y + player_y) / 2
            self.image = pygame.transform.scale(self.image, (self.image.get_width()/2, self.image.get_height()/2))
        if map_end:
            self.rect.x = 2 * self.rect.x - player_x
            self.rect.y = 2 * self.rect.y - player_y
            self.image = pygame.transform.scale(pygame.image.load(STORE_PATH), (self.image.get_width() * 2, self.image.get_height() * 2))


class Wall(MapObj): # a class for the map borders or walls
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.image.load(WALL_PATH)
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self, direct, size, player_x, player_y, portal=False, portal_properties=None, map_use=False, map_end=False):
        super().update(direct, size, player_x, player_y, portal, portal_properties)
        if map_use:
            self.rect.x = (self.rect.x + player_x) / 2
            self.rect.y = (self.rect.y + player_y) / 2
            self.image = pygame.transform.scale(self.image, (self.image.get_width()/2, self.image.get_height()/2))
        if map_end:
            self.rect.x = 2 * self.rect.x - player_x
            self.rect.y = 2 * self.rect.y - player_y
            self.image = pygame.transform.scale(pygame.image.load(WALL_PATH), (self.image.get_width() * 2, self.image.get_height() * 2))


class Gate(MapObj):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.image.load(GATE_PATH)
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self, direct, size, player_x, player_y, portal=False, portal_properties=None, map_use=False, map_end=False):
        super().update(direct, size, player_x, player_y, portal, portal_properties)
        if map_use:
            self.rect.x = (self.rect.x + player_x) / 2
            self.rect.y = (self.rect.y + player_y) / 2
            self.image = pygame.transform.scale(self.image, (self.image.get_width()/2, self.image.get_height()/2))
        if map_end:
            self.rect.x = 2 * self.rect.x - player_x
            self.rect.y = 2 * self.rect.y - player_y
            self.image = pygame.transform.scale(pygame.image.load(GATE_PATH), (self.image.get_width() * 2, self.image.get_height() * 2))


class Monk(MapObj):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.image.load(MONK_PATH)
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.monk_auras = pygame.sprite.Group()
        for i in range(-2, 3):
            for j in range(-2, 3):
                i
                aura = MonkAura(x+width*i, y+height*j, width, height)
                self.monk_auras.add(aura)

    def update(self, direct, size, player_x, player_y, portal=False, portal_properties=None, map_use=False, map_end=False):
        super().update(direct, size, player_x, player_y, portal, portal_properties)
        if map_use:
            self.rect.x = (self.rect.x + player_x) / 2
            self.rect.y = (self.rect.y + player_y) / 2
            self.image = pygame.transform.scale(self.image, (self.image.get_width()/2, self.image.get_height()/2))
        if map_end:
            self.rect.x = 2 * self.rect.x - player_x
            self.rect.y = 2 * self.rect.y - player_y
            self.image = pygame.transform.scale(pygame.image.load(MONK_PATH), (self.image.get_width() * 2, self.image.get_height() * 2))


class MonkAura(MapObj):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.image.load(MONK_AURA_PATH)
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self, direct, size, player_x, player_y, portal=False, portal_properties=None, map_use=False, map_end=False):
        super().update(direct, size, player_x, player_y, portal, portal_properties)
        if player_x == self.rect.x and player_y == self.rect.y:
            self.near_main = True
        else:
            self.near_main = False
        if map_use:
            self.rect.x = (self.rect.x + player_x) / 2
            self.rect.y = (self.rect.y + player_y) / 2
            self.image = pygame.transform.scale(self.image, (self.image.get_width()/2, self.image.get_height()/2))
        if map_end:
            self.rect.x = 2 * self.rect.x - player_x
            self.rect.y = 2 * self.rect.y - player_y
            self.image = pygame.transform.scale(pygame.image.load(MONK_AURA_PATH), (self.image.get_width() * 2, self.image.get_height() * 2))


class Fountain(MapObj):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.image.load(FOUNTAIN_PATH)
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self, direct, size, player_x, player_y, portal=False, portal_properties=None, map_use=False, map_end=False):
        super().update(direct, size, player_x, player_y, portal, portal_properties)
        if map_use:
            self.rect.x = (self.rect.x + player_x) / 2
            self.rect.y = (self.rect.y + player_y) / 2
            self.image = pygame.transform.scale(self.image, (self.image.get_width()/2, self.image.get_height()/2))
        if map_end:
            self.rect.x = 2 * self.rect.x - player_x
            self.rect.y = 2 * self.rect.y - player_y
            self.image = pygame.transform.scale(pygame.image.load(FOUNTAIN_PATH), (self.image.get_width() * 2, self.image.get_height() * 2))


class Portal(MapObj):
    def __init__(self, x, y, width, height, distance_x, distance_y):
        super().__init__()
        self.image = pygame.image.load(PORTAL_PATH)
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.distance_x = distance_x
        self.distance_y = distance_y

    def update(self, direct, size, player_x, player_y, portal=False, portal_properties=None, map_use=False, map_end=False):
        super().update(direct, size, player_x, player_y, portal, portal_properties)
        if player_x == self.rect.x and player_y == self.rect.y:
            self.near_main = True
        else:
            self.near_main = False
        if map_use:
            self.rect.x = (self.rect.x + player_x) / 2
            self.rect.y = (self.rect.y + player_y) / 2
            self.image = pygame.transform.scale(self.image, (self.image.get_width()/2, self.image.get_height()/2))
        if map_end:
            self.rect.x = 2 * self.rect.x - player_x
            self.rect.y = 2 * self.rect.y - player_y
            self.image = pygame.transform.scale(pygame.image.load(PORTAL_PATH), (self.image.get_width() * 2, self.image.get_height() * 2))


class MainChar(pygame.sprite.Sprite): # a class for the main character
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image_right = pygame.image.load(MAIN_CHAR_PATH)
        self.image_left = pygame.transform.flip(self.image_right, True, False)
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
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.image.load(NO_TEXTURE_PATH)
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

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

    def update(self, direct, size, player_x, player_y, portal=False, portal_properties=None):
        super().update(direct, size, player_x, player_y, portal, portal_properties)


class Grass(MapObj):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.image.load(GRASS_PATH)
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self, direct, size, player_x, player_y, portal=False, portal_properties=None, map_use=False, map_end=False):
        super().update(direct, size, player_x, player_y, portal, portal_properties)
        if map_use:
            self.rect.x = (self.rect.x + player_x) / 2
            self.rect.y = (self.rect.y + player_y) / 2
            self.image = pygame.transform.scale(self.image, (self.image.get_width()/2, self.image.get_height()/2))
        if map_end:
            self.rect.x = 2 * self.rect.x - player_x
            self.rect.y = 2 * self.rect.y - player_y
            self.image = pygame.transform.scale(pygame.image.load(GRASS_PATH), (self.image.get_width() * 2, self.image.get_height() * 2))