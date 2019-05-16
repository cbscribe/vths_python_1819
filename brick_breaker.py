import pygame as pg
from random import randrange

WIDTH = 800
HEIGHT = 600
FPS = 60
BALL_SIZE = 10
BALL_SPEED = 5
BRICK_WIDTH = 32
BRICK_HEIGHT = 16
PADDLE_SIZE = 150

vec2 = pg.math.Vector2
pg.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
clock = pg.time.Clock()

class Paddle(pg.sprite.Sprite):
    def __init__(self):
        super().__init__(all_sprites)
        self.image = pg.Surface((PADDLE_SIZE, 15))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH/2, HEIGHT-50)
    def update(self):
        x, y = pg.mouse.get_pos()
        self.rect.centerx = x

class Ball(pg.sprite.Sprite):
    def __init__(self):
        super().__init__(all_sprites)
        self.image = pg.Surface((BALL_SIZE, BALL_SIZE))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect()
        self.pos = vec2(WIDTH/2, HEIGHT/2)
        self.vel = vec2(BALL_SPEED,
                            0).rotate(randrange(-135, -45))
        self.rect.center = self.pos
    def update(self):
        self.pos += self.vel
        self.rect.center = self.pos
all_sprites = pg.sprite.Group()
ball = Ball()
paddle = Paddle()
while True:
    clock.tick(FPS)
    for event in pg.event.get():
        if event.type == pg.QUIT: pg.quit()
    all_sprites.update()
    screen.fill((0, 0, 0))
    all_sprites.draw(screen)
    pg.display.flip()