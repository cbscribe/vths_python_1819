import pygame
import random

width = 480
height = 600
fps = 60
gravity = 0.15
flap = 3
speed = 2.5
gap = 150

bird_img = [pygame.image.load("Downloads/bird1.png"),
            pygame.image.load("Downloads/bird2.png"),
            pygame.image.load("Downloads/bird3.png")]
pipe_img_top = pygame.image.load("Downloads/pipe_top.png")
pipe_img_bottom = pygame.image.load("Downloads/pipe_bottom.png")
ground_img = pygame.image.load("Downloads/ground.png")
background = pygame.image.load("Downloads/background.png")
background = pygame.transform.rotozoom(background, 0, 2)
go_img = pygame.image.load("Downloads/gameover.png")

def draw_text(text, size, color, x, y):
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect)

class Bird(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(all_sprites)
        self.image = bird_img[0]
        self.frame = 0
        #self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.center = (width/2, height/2)
        self.vy = 0
        self.alive = True
    def update(self):
        self.frame += 1
        if self.frame > 2: self.frame = 0
        self.image = bird_img[self.frame]
        self.vy += gravity
        self.rect.y += self.vy
        if self.rect.bottom > height-50:
            self.rect.bottom = height-50
            self.vy = 0
        if self.rect.top < 0:
            self.rect.top = 0
            self.vy = 0
            
class Pipe(pygame.sprite.Sprite):
    def __init__(self, location, ypos):
        super().__init__(all_sprites, pipes)
        if location == "top":
            self.image = pipe_img_top
        else:
            self.image = pipe_img_bottom
        #self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect()
        self.rect.x = width + 50
        self.passed = False
        if location == "top":
            self.rect.bottom = ypos
        else:
            self.rect.top = ypos
    def update(self):
        self.rect.x -= speed
        if self.rect.left < 0:
            self.kill()

pygame.init()
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
while True:
    all_sprites = pygame.sprite.Group()
    pipes = pygame.sprite.Group()
    bird = Bird()
    score = 0
    pygame.time.set_timer(pygame.USEREVENT, 2000)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                if bird.alive:
                    bird.vy -= flap
            if event.type == pygame.USEREVENT:
                y = random.randrange(50, height-gap*2)
                Pipe("top", y)
                Pipe("bottom", y+gap)
        all_sprites.update()
        for pipe in pipes:
            if pipe.rect.right < bird.rect.left and not pipe.passed:
                pipe.passed = True
                score += 0.5
        hit = pygame.sprite.spritecollide(bird, pipes, False)
        if hit:
            bird.alive = False
            #running = False
        screen.fill( (0, 155, 155 ))
        screen.blit(background, (0, -250))
        all_sprites.draw(screen)
        if not bird.alive:
            screen.blit(go_img, (width/2, height/2))
        draw_text(str(int(score)), 50, (255, 255, 255), width/2, 20)
        screen.blit(ground_img, (0, height-50))
        screen.blit(ground_img, (335, height-50))
        pygame.display.flip()
        clock.tick(fps) 
pygame.quit()   
