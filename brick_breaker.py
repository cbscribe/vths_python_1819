import pygame as pg
from random import randrange, choice, random

WIDTH = 800
HEIGHT = 600
FPS = 60
BALL_SIZE = 10
BALL_SPEED = 8
BRICK_WIDTH = 24
BRICK_HEIGHT = 12
PADDLE_SIZE = 100
TRAIL_LENGTH = 25
POW_CHANCE = 0.1

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
        super().__init__(all_sprites, balls)
        self.image = pg.Surface((BALL_SIZE, BALL_SIZE))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect()
        self.pos = vec2(WIDTH/2, HEIGHT/2)
        self.vel = vec2(BALL_SPEED,
                            0).rotate(randrange(-135, -45))
        self.rect.center = self.pos
        self.trail = [] 
    def update(self):
        if self.rect.y > HEIGHT:
            self.kill()
        if len(self.trail) > TRAIL_LENGTH:
            del self.trail[0]
        self.trail.append(self.rect.center)
        self.pos += self.vel
        self.rect.center = self.pos
        # left
        if self.pos.x < BALL_SIZE/2:
            self.pos.x = BALL_SIZE/2
            self.vel.x *= -1
        # right
        if self.pos.x > WIDTH - BALL_SIZE/2:
            self.pos.x = WIDTH - BALL_SIZE/2
            self.vel.x *= -1
        # top
        if self.pos.y < BALL_SIZE/2:
            self.pos.y = BALL_SIZE/2
            self.vel.y *= -1
    def draw_trail(self):
        next_pos = self.rect.center
        for num, pos in enumerate(reversed(self.trail)):
            pct = (TRAIL_LENGTH - num) / TRAIL_LENGTH
            color = (int(221*pct), int(232*pct), int(63*pct))
            pg.draw.line(screen, color, next_pos, pos, int(BALL_SIZE*pct))
            next_pos = pos

class Pow(pg.sprite.Sprite):
    def __init__(self, pos):
        super().__init__(all_sprites, pows)
        self.image = pg.Surface((16, 16)).convert_alpha()
        self.image.fill((0, 0, 0, 0))
        self.rect = self.image.get_rect()
        pg.draw.circle(self.image, (255, 0, 255), (8, 8), 8)
        self.pos = pos
        self.rect.center = self.pos
        self.type = choice(["slow", "multi", "grow", "super"])
    def update(self):
        self.pos.y += 3
        self.rect.y = self.pos.y
        if self.rect.top > HEIGHT: self.kill()

class Brick(pg.sprite.Sprite):    
    def __init__(self, x, y, color):
        super().__init__(all_sprites, bricks)
        self.image = pg.Surface((BRICK_WIDTH, BRICK_HEIGHT))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.midtop = (x, y)
        self.hit = False
        self.vy = -10
        self.vx = randrange(-5, 6)
    def update(self):
        if self.hit:
            self.vy += 0.5
            self.rect.x += self.vx
            self.rect.y += self.vy
        if self.rect.top > HEIGHT: self.kill()

GREEN = (14, 183, 63)
BLUE = (55, 121, 179)
RED = (255, 84, 76)
YELLOW = (221, 232, 63)
ORANGE = (255, 128, 0)
COLORS = [RED, ORANGE, YELLOW, GREEN, BLUE]
def spawn_bricks():
    for y in range(10):
        for x in range(30):
            Brick(24 + x * (2 + BRICK_WIDTH), 
                  50 +  y * (2 + BRICK_HEIGHT), COLORS[y//2])

def start_animation():
    anim_group = bricks.copy()
    for sprite in anim_group:
        sprite.target = sprite.rect.y
        sprite.rect.y -= HEIGHT
        sprite.start_time = randrange(500)
    start = pg.time.get_ticks()
    while len(anim_group) > 0:
        clock.tick(FPS)
        for event in pg.event.get(): pass
        for sprite in anim_group:
            if pg.time.get_ticks() - start > sprite.start_time:
                sprite.rect.y += (sprite.target - sprite.rect.y) * 0.15 + 1
                if sprite.rect.y == sprite.target:
                    anim_group.remove(sprite)
        screen.fill((0, 0, 0))
        all_sprites.draw(screen)
        pg.display.flip()

all_sprites = pg.sprite.Group()
bricks = pg.sprite.Group()
balls = pg.sprite.Group()
pows = pg.sprite.Group()
spawn_bricks()
start_animation()
ball = Ball()
paddle = Paddle()
slow_timer = 0
grow_timer = 0
super_timer = 0
super_ball = False
paused = True
while True:
    if pg.time.get_ticks() - super_timer > 5000:
        super_ball = False
    if pg.time.get_ticks() - slow_timer > 10000:
        BALL_SPEED = 8
    if pg.time.get_ticks() - grow_timer > 5000:
        paddle.image = pg.Surface((PADDLE_SIZE, 15))
        paddle.image.fill((255, 255, 255))
        paddle.rect = paddle.image.get_rect(center=paddle.rect.center)
    clock.tick(FPS)
    for event in pg.event.get():
        if event.type == pg.QUIT: pg.quit()
        # if event.type == pg.KEYDOWN and event.key == pg.K_SPACE: Ball()
        if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
            paused = not paused
    if not paused:
        all_sprites.update()
    # catch powerups
    pow_hits = pg.sprite.spritecollide(paddle, pows, True)
    for p in pow_hits:
        if p.type == "multi":
            Ball()
            Ball()
        if p.type == "slow":
            BALL_SPEED -= 1
            if BALL_SPEED < 1: BALL_SPEED = 1
            slow_timer = pg.time.get_ticks()
        if p.type == "grow":
            grow_timer = pg.time.get_ticks()
            paddle.image = pg.Surface((PADDLE_SIZE+25, 15))
            paddle.image.fill((255, 255, 255))
            paddle.rect = paddle.image.get_rect(center=paddle.rect.center)
        if p.type == "super":
            super_timer = pg.time.get_ticks()
            super_ball = True
    # bounce ball off paddle
    for ball in balls:
        paddle_hit = pg.sprite.collide_rect(paddle, ball)
        if paddle_hit:
            ball.vel.y *= -1
            # ball.rect.bottom = paddle.rect.top
            ball.pos.y = paddle.rect.top - BALL_SIZE/2
            dist = ball.rect.centerx - paddle.rect.centerx
            ball.vel.x = BALL_SPEED * dist * (1/25)
            ball.vel = ball.vel.normalize() * BALL_SPEED
    # bounce off bricks
    for ball in balls:
        brick_hits = pg.sprite.spritecollide(ball, bricks, False)
        for brick in brick_hits:
            bricks.remove(brick)
            brick.hit = True
            if random() < POW_CHANCE:
                Pow(vec2(ball.pos))
        if brick_hits:
            if super_ball:
                ball.vel.y *= 1
            else:
                ball.vel.y *= -1
    # next level
    if len(bricks) == 0:
        spawn_bricks()
        start_animation()
        ball.pos = (WIDTH/2, HEIGHT/2)
    # Game over
    if len(balls) == 0:
        pg.quit()
    screen.fill((0, 0, 0))
    for ball in balls:
        ball.draw_trail()
    all_sprites.draw(screen)
    pg.display.flip()
    