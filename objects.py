import pygame.sprite

RED = (255, 0, 0)


class MapObj(pygame.sprite.Sprite): # a super class for all the map objects
    def __init__(self):
        super().__init__()
        self.near_main = False

    def update(self, direct, size, player_x, player_y, portal=False):
        if direct == "UP":
            self.rect.y += size
        if direct == "DOWN":
            self.rect.y -= size
        if direct == "LEFT":
            self.rect.x += size
        if direct == "RIGHT":
            self.rect.x -= size
        if portal:
            self.rect.x += size * 20
        if player_x + player_y - size <= self.rect.x + self.rect.y <= player_x + player_y + size and (self.rect.x == player_x or self.rect.y == player_y):
            self.near_main = True
        else:
            self.near_main = False


class Box(MapObj): # class of boxes/chests
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.image.load("C:\\Users\\User\\Downloads\\images-removebg-preview.png")
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Store(MapObj):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.image.load("C:\\Users\\User\\Downloads\\store.jpeg")
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Wall(MapObj): # a class for the map borders or walls
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.image.load("C:\\Users\\User\\Downloads\\images.jpg")
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Gate(MapObj):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.image.load("C:\\Users\\User\\Downloads\\gate.png")
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Monk(MapObj):
    def __init__(self, x, y, width, height, tile_size):
        super().__init__()
        self.image = pygame.image.load("C:\\Users\\User\\Downloads\\monk-wiki_ver_1 (1).png")
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.monk_auras = pygame.sprite.Group()
        for i in range(-2, 3):
            for j in range(-2, 3):
                aura = MonkAura(x+tile_size*i, y+tile_size*j, width, height)
                self.monk_auras.add(aura)


class MonkAura(MapObj):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.image.load("C:\\Users\\User\\Downloads\\mist_temp.jpg")
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self, direct, size, player_x, player_y, portal=False):
        super().update(direct, size, player_x, player_y, portal)
        if player_x == self.rect.x and player_y == self.rect.y:
            self.near_main = True
        else:
            self.near_main = False


class Fountain(MapObj):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.image.load("C:\\Users\\User\\Downloads\\fountain.jpeg")
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Portal(MapObj):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.image.load("C:\\Users\\User\\Downloads\\Portal.webp")
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self, direct, size, player_x, player_y, portal=False):
        super().update(direct, size, player_x, player_y, portal)
        if player_x == self.rect.x and player_y == self.rect.y:
            self.near_main = True
        else:
            self.near_main = False


class MainChar(pygame.sprite.Sprite): # a class for the main character
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.image.load(
            "C:\\Users\\User\\Downloads\\15a9edbe62af9aafdc4dee2f5a5e9420-removebg-preview.png")
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class InventorySlot(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.image.load("C:\\Users\\User\\Downloads\\inventory_slot.jpg")
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class InventoryItem(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, image_path="C:\\Users\\User\\Downloads\\notexture.png"):
        super().__init__()
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.amount = 0
