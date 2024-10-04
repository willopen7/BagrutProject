import pygame.sprite

RED = (255, 0, 0)


class MapObj(pygame.sprite.Sprite): # a super class for all the map objects
    def __init__(self):
        super().__init__()
        self.near_main = False

    def update(self, direct, size, main_x, main_y):
        if direct == "UP":
            self.rect.y += size
        if direct == "DOWN":
            self.rect.y -= size
        if direct == "LEFT":
            self.rect.x += size
        if direct == "RIGHT":
            self.rect.x -= size
        if main_x + main_y - size <= self.rect.x + self.rect.y <= main_x + main_y + size and (self.rect.x == main_x or self.rect.y == main_y):
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

    def update(self, direct, size, main_x, main_y):
        super().update(direct, size, main_x, main_y)
        if main_x == self.rect.x and main_y == self.rect.y:
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
