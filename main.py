import pygame
import objects
import random
import funcs


SCREEN_HEIGHT = 880
SCREEN_WIDTH = 880

pygame.init()
screen = pygame.display.set_mode((SCREEN_HEIGHT, SCREEN_WIDTH))
clock = pygame.time.Clock()
running = True
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
GRID_SIZE = 80
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
all_sprites = pygame.sprite.Group()
grid_boxes = [[random.randrange(1, 5, 1) for i in range(1000)] for i in range(1000)]
cur_boxes = [grid_boxes[i] for i in range(GRID_WIDTH // GRID_SIZE)]

for i in range(100):
    box = objects.Box(random.randint(-100, 100)*80, random.randint(-100, 100)*80, 80, 80)
    all_sprites.add(box)
    wall = objects.Wall((i-10)*80,160, 80, 80)
    all_sprites.add(wall)
main_char = objects.MainChar(400, 400, 80, 80)
main_chars = pygame.sprite.Group()
main_chars.add(main_char)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if funcs.check_position("UP", all_sprites):
                    all_sprites.update("UP", 80, 400, 400)
            if event.key == pygame.K_DOWN:
                if funcs.check_position("DOWN", all_sprites):
                    all_sprites.update("DOWN", 80, 400, 400)
            if event.key == pygame.K_LEFT:
                if funcs.check_position("LEFT", all_sprites):
                    all_sprites.update("LEFT", 80, 400, 400)
            if event.key == pygame.K_RIGHT:
                if funcs.check_position("RIGHT", all_sprites):
                    all_sprites.update("RIGHT", 80, 400, 400)
        screen.fill(WHITE)
        for x in range(80, SCREEN_WIDTH, GRID_SIZE):
            pygame.draw.line(screen, GRAY, (x, 0), (x, SCREEN_HEIGHT))
        for y in range(80, SCREEN_HEIGHT, GRID_SIZE):
            pygame.draw.line(screen, GRAY, (0, y), (SCREEN_WIDTH, y))
        opened = False
        for sprite in all_sprites:
            if sprite.__class__ == objects.Box and sprite.near_main == True:
                opened = True
        all_sprites.draw(screen)
        main_chars.draw(screen)
        if opened:
            open_box = pygame.image.load("C:\\Users\\User\\Downloads\\Champion_Chest.webp")
            screen.blit(open_box, (0, 0))
        pygame.display.flip()
