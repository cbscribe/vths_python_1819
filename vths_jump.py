import pygame
import random

WIDTH = 800
HEIGHT = 640
FPS = 60
GRAVITY = 2
RUN_SPEED = 8
JUMP_SPEED = -30

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

mario_img = pygame.image.load("Downloads/mario_right.png")
mario_img = pygame.transform.rotozoom(mario_img, 0, 0.2)
mario_left = pygame.transform.flip(mario_img, True, False)
block_img = pygame.image.load("Downloads/grass_main_32x32.png")
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(all_sprites)
        self.image = mario_img #pygame.Surface((32, 64))
        #self.image.fill((250, 250, 50))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.vy = 0
        
    def jump(self):
        self.rect.y += 1
        hits = pygame.sprite.spritecollide(self, platforms, False)
        self.rect.y -= 1
        if hits:
            self.vy = JUMP_SPEED
            
    def update(self):
        self.vx = 0
        self.vy += GRAVITY
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            self.jump()
        if keys[pygame.K_RIGHT]:
            self.vx += RUN_SPEED
            self.image = mario_img
        if keys[pygame.K_LEFT]:
            self.vx -= RUN_SPEED
            self.image = mario_left
        self.rect.x += self.vx
        self.rect.y += self.vy
        if self.vy > 0:
            hits = pygame.sprite.spritecollide(self, platforms, False)
            if hits:
                self.vy = 0
                self.rect.bottom = hits[0].rect.top

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(all_sprites, platforms)
        self.image = block_img#pygame.Surface((32, 32))
        #self.image.fill( (14, 183, 63) )
        self.rect = self.image.get_rect(topleft=(x, y))

class Camera:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.camera = pygame.Rect(0, 0, width, height)
    def update(self, target):
        x = -target.rect.centerx + int(WIDTH/2)
        y = -target.rect.centery + int(HEIGHT/2)
        y = max(HEIGHT-self.height, y)
        self.camera = pygame.Rect(x, y, self.width, self.height)
    def apply(self, item):
        return item.rect.move(self.camera.topleft)

all_sprites = pygame.sprite.Group()
platforms = pygame.sprite.Group()
# for x in range(5, 20):
#     Platform(x*32, 550)
# player = Player(WIDTH/2, 400)
level = []
with open("level1.txt") as f:
    for line in f:
        level.append(line.strip())
for row, items in enumerate(level):
    for col, item in enumerate(items):
        if item == "#":
            Platform(col*32, row*32)
        if item == "$":
            player = Player(col*32, row*32)
camera = Camera(len(level[0])*32, len(level)*32)

running = True
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT: pygame.quit()
    all_sprites.update()
    camera.update(player)
    screen.fill((104, 229, 255))
    #all_sprites.draw(screen)
    for sprite in all_sprites:
        screen.blit(sprite.image, camera.apply(sprite))
    pygame.display.flip()