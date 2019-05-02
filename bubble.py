import pygame as pg
import random, math

WIDTH = 640
HEIGHT = 480
FPS = 60
BUBBLESIZE = 20
BOARDWIDTH = 16
BOARDHEIGHT = 14
RED      = (255, 0, 0)
GREEN    = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 128, 0)
PURPLE = (255, 0, 255)
CYAN = (0, 255, 255)
colors = [RED, GREEN, BLUE, YELLOW, ORANGE, PURPLE, CYAN]

class Bubble(pg.sprite.Sprite):
    def __init__(self, color, dir=0):
        super().__init__(bubbles)
        self.rect = pg.Rect(0, 0, BUBBLESIZE, BUBBLESIZE)
        self.rect.center = (WIDTH/2, HEIGHT-30)
        self.speed = 10
        self.color = color
        self.dir = dir
    def draw(self):
        pg.draw.circle(screen, self.color, self.rect.center, BUBBLESIZE)
        pg.draw.circle(screen, (0, 0, 0), self.rect.center, BUBBLESIZE, 1)
    def update(self):
        self.rect.x += self.speed * math.cos(self.dir)
        self.rect.y += self.speed * -math.sin(self.dir)
        if self.rect.x < 0 or self.rect.x > WIDTH-BUBBLESIZE/2:
            self.dir = 3.14 - self.dir
        
class Arrow(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.angle = 0
        self.arrow = pg.image.load("Downloads/Arrow.png")
        self.image = self.arrow.copy()
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH/2, HEIGHT-30)
    def update(self):
        mpos = pg.mouse.get_pos()[0] - self.rect.centerx
        self.angle = -math.atan2(-100, mpos)
        self.image = pg.transform.rotozoom(self.arrow,
                       math.degrees(self.angle), 1)
        self.rect = self.image.get_rect(center=self.rect.center)
        
pg.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
clock = pg.time.Clock()

arrow = Arrow()
nextcolor = random.choice(colors)
bubbles = pg.sprite.Group()
score = 0
while True:
    clock.tick(FPS)
    for event in pg.event.get():
        if event.type == pg.QUIT: pg.quit()
        if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
            Bubble(nextcolor, arrow.angle)
            nextcolor = random.choice(colors)
    arrow.update()
    bubbles.update()
    screen.fill((255, 255, 255))
    screen.blit(arrow.image, arrow.rect)
    pg.draw.circle(screen, nextcolor, arrow.rect.center, 13)
    for bubble in bubbles: bubble.draw()
    pg.display.flip()