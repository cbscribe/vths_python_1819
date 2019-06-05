import pygame as pg
import random, math

WIDTH = 640
HEIGHT = 480
FPS = 60
BUBBLESIZE = 20
BOARDWIDTH = 16
BOARDHEIGHT = 14
GREEN = (14, 183, 63)
BLUE = (55, 121, 179)
RED = (255, 84, 76)
YELLOW = (221, 232, 63)
PURPLE = (128, 0, 128)
ORANGE = (255, 128, 0)
CYAN = (0, 255, 255)
colors = [RED, GREEN, BLUE, YELLOW, CYAN, ORANGE]
neighbor_positions = [[(1, 0), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1)],
                      [(1, 0), (1, 1), (0, 1), (-1, 0), (0, -1), (1, -1)]]

class Bubble(pg.sprite.Sprite):
    def __init__(self, color, dir=0):
        super().__init__(bubbles)
        self.rect = pg.Rect(0, 0, BUBBLESIZE, BUBBLESIZE)
        self.rect.center = (WIDTH/2, HEIGHT-30)
        self.speed = 10
        self.color = color
        self.dir = dir
        self.moving = True
        self.radius = BUBBLESIZE

    def draw(self):
        pg.draw.circle(screen, self.color, self.rect.center, BUBBLESIZE)
        pg.draw.circle(screen, (0, 0, 0), self.rect.center, BUBBLESIZE, 1)
   
    def update(self):
        if not self.moving:
            return
        self.rect.x += self.speed * math.cos(self.dir)
        self.rect.y += self.speed * -math.sin(self.dir)
        if self.rect.x < 0 or self.rect.x > WIDTH-BUBBLESIZE/2:
            self.dir = 3.14 - self.dir
        if self.rect.y <= 0:
            board.add(self)
        hits = pg.sprite.spritecollide(self, bubbles, False,
                                        pg.sprite.collide_circle)
        for hit in hits:
            if hit == self: break
            self.moving = False
            board.add(self)
            break

class Board:
    def __init__(self):
        self.bubbles = [[None] * BOARDWIDTH for _ in range(BOARDHEIGHT)]
        for row in range(5):
            for col in range(BOARDWIDTH):
                b = Bubble(random.choice(colors))
                b.moving = False
                b.rect.center = self.set_position(row, col)
                self.bubbles[row][col] = b
                b.row = row
                b.col = col
                
    def set_position(self, row, col):
        x = BUBBLESIZE * 2 * col + 5 + BUBBLESIZE * (row % 2)
        y = 20 + BUBBLESIZE * 2 * row - row * 5
        return x, y
        
    def set_grid(self, x, y):
        row = int((y - 20) / (BUBBLESIZE * 2 - 5))
        col = int((x - 5 - BUBBLESIZE * (row % 2)) / (BUBBLESIZE * 2))
        return row, col
        
    def add(self, bubble):
        y, x = self.set_grid(bubble.rect.centerx + BUBBLESIZE,
                             bubble.rect.centery + BUBBLESIZE)
        self.bubbles[y][x] = bubble
        bubble.rect.center = self.set_position(y, x)
        bubble.row = y
        bubble.col = x
        cluster = self.find_cluster(bubble, True, True)
        if len(cluster) >= 3:
            for b in cluster:
                self.bubbles[b.row][b.col] = None
                b.kill()
            for c in self.find_floaters():
                for b in c:
                    self.bubbles[b.row][b.col] = None
                    b.kill()
        
    def get_neighbors(self, b):
        neighbors = []
        for pos in neighbor_positions[b.row % 2]:
            nx = b.col + pos[0]
            ny = b.row + pos[1]
            if nx >= 0 and nx < BOARDWIDTH and ny >= 0 and ny < BOARDHEIGHT:
                if self.bubbles[ny][nx]:
                    neighbors.append(self.bubbles[ny][nx])
        return neighbors
        
    def reset_state(self):
        for bubble in bubbles: bubble.checked = False
        
    def find_cluster(self, b, match_color, reset):
        if reset: self.reset_state()
        target = b
        to_process = [target]
        target.checked = True
        cluster = []
        while len(to_process) > 0:
            current = to_process.pop()
            if not current: continue
            if not match_color or (current.color == target.color):
                cluster.append(current)
                for n in self.get_neighbors(current):
                    if not n.checked:
                        to_process.append(n)
                        n.checked = True
        return cluster
        
    def find_floaters(self):
        self.reset_state()
        floaters = []
        for row in range(BOARDHEIGHT):
            for col in range(BOARDWIDTH):
                b = self.bubbles[row][col]
                if b and not b.checked:
                    cluster = self.find_cluster(b, False, False)
                    if len(cluster) <= 0: continue
                    floating = True
                    for tile in cluster:
                        if tile.row == 0:
                            floating = False
                            break
                    if floating:
                        floaters.append(cluster)
        return floaters
                
class Arrow(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.angle = 0
        self.arrow = pg.image.load("Downloads/Arrow.png")
        self.arrow = pg.transform.rotozoom(self.arrow, 0, 1.0)
        self.image = self.arrow.copy()
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH/2, HEIGHT-30)
    def update(self):
        mposx, mposy = pg.mouse.get_pos()
        self.angle = -math.atan2(mposy-self.rect.centery, mposx-self.rect.centerx)
        self.image = pg.transform.rotozoom(self.arrow,
                       math.degrees(self.angle), 1)
        self.rect = self.image.get_rect(center=self.rect.center)
        
pg.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
clock = pg.time.Clock()
pg.mouse.set_visible(False)

arrow = Arrow()
nextcolor = random.choice(colors)
bubbles = pg.sprite.Group()
board = Board()
score = 0
while True:
    clock.tick(FPS)
    for event in pg.event.get():
        if event.type == pg.QUIT: pg.quit()
        if event.type == pg.MOUSEBUTTONDOWN:
            Bubble(nextcolor, arrow.angle)
            nextcolor = random.choice(colors)
    arrow.update()
    bubbles.update()
    screen.fill((255, 255, 255))
    screen.blit(arrow.image, arrow.rect)
    pg.draw.circle(screen, nextcolor, arrow.rect.center, 13)
    for bubble in bubbles: bubble.draw()
    pg.display.flip()