import pygame
import random

width = 480
height = 640
fps = 60

pygame.init()
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

ship = pygame.image.load("Downloads/playerShip1_orange.png")
meteor = pygame.image.load("Downloads/meteorBrown_med1.png")
background = pygame.image.load("Downloads/starfield.png")
laser_sound = pygame.mixer.Sound("Downloads/pew.wav")
music = pygame.mixer.music.load("Downloads/frozenjam.ogg")

def draw_text(text, size, color, x, y):
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(all_sprites)
        self.image = pygame.transform.rotozoom(ship, 0, 0.75)
        #self.image.fill( (255, 128, 0) )
        self.rect = self.image.get_rect()
        self.rect.center = (width/2, height-75)
        self.cooldown = 250
        self.last_shot = 0
        
    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.cooldown:
            self.last_shot = now
            laser_sound.play()
            Bullet(self.rect.centerx-33, self.rect.top+22)
            Bullet(self.rect.centerx+33, self.rect.top+22)
            Bullet(self.rect.centerx, self.rect.top)
            
    def update(self):
        self.shoot()
        vx = 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            vx += 10
        if keys[pygame.K_LEFT]:
            vx -= 10
        self.rect.x += vx
        if self.rect.right > width: self.rect.right = width
        if self.rect.left < 0: self.rect.left = 0

class Mob(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(all_sprites, mobs)
        self.image = meteor
        #self.image.fill( (255, 0, 0) )
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0, width-40)
        self.rect.y = -50
        self.vy = random.randrange(2, 10)
    def update(self):
        self.rect.y += self.vy
        if self.rect.top > height:
            self.rect.y = -50
            self.rect.x = random.randrange(0, width-40)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(all_sprites, bullets)
        self.image = pygame.Surface((8, 40))
        self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect()
        self.rect.midbottom = (x, y)
    def update(self):
        self.rect.y += -15  # speed of the bullet
        if self.rect.bottom < 0:
            self.kill()

all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()
bullets = pygame.sprite.Group()
for i in range(10):
    Mob()
player = Player()
score = 0
pygame.mixer.music.play(loops=-1)
running = True
while running:
    clock.tick(fps)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    all_sprites.update()
    # check when bullets hit mobs
    bullet_hits = pygame.sprite.groupcollide(mobs, bullets, True, False)
    for mob in bullet_hits:
        score += 10
        Mob()
    # check when mobs hit player
    mob_hits = pygame.sprite.spritecollide(player, mobs, True)
    if mob_hits:
        running = False
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))
    all_sprites.draw(screen)
    draw_text(str(score), 50, (255, 255, 255), width/2, 20)
    pygame.display.flip()
pygame.quit()
