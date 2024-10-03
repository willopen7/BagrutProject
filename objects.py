import pygame.sprite

RED = (255, 0, 0)


class MapObj(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.near_main = False

    def update(self, direct, size, main_x, main_y):
        if direct == "UP":
            self.rect.y += size
#            if main_y + size == self.rect.y and main_x == self.rect.x:
#                self.near_main = True
#            else:
#                self.near_main = False
        if direct == "DOWN":
            self.rect.y -= size
#            if main_y - size == self.rect.y:
#                self.near_main = True
#            else:
#                self.near_main = False
        if direct == "LEFT":
            self.rect.x += size
#            if main_x + size == self.rect.x:
#                self.near_main = True
#            else:
#                self.near_main = False
        if direct == "RIGHT":
            self.rect.x -= size
#            if main_x - size == self.rect.x:
#                self.near_main = True
#            else:
#                self.near_main = False
        if main_x + main_y - size <= self.rect.x + self.rect.y <= main_x + main_y + size and (self.rect.x == main_x or self.rect.y == main_y):
            self.near_main = True
        else:
            self.near_main = False


class Box(MapObj):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.image.load("C:\\Users\\User\\Downloads\\images-removebg-preview.png")
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    '''def update(self, direct, size, screen=None, main_pos=(400, 400), grid_size=80):
        super().update(direct, size)
        if main_pos[0] - grid_size <= self.rect.x <= main_pos[0] + grid_size and \
                main_pos[1] - grid_size <= self.rect.y <= main_pos[1] + grid_size:
            pass
            #pygame.Surface.blit("C:\\Users\\User\\Downloads\\Champion_Chest.webp", screen)'''


class Wall(MapObj):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.image.load("C:\\Users\\User\\Downloads\\images.jpg")
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class MainChar(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.image.load(
            "C:\\Users\\User\\Downloads\\15a9edbe62af9aafdc4dee2f5a5e9420-removebg-preview.png")
        self.image = pygame.transform.scale(self.image, (80, 80))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
