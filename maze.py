#стimport pygame
from typing import Any
import pygame
WIDTH = 1200
HEIGHT = 700
SIZE = (WIDTH, HEIGHT)
FPS = 60


window = pygame.display.set_mode((800,500))
clock = pygame.time.Clock()
background = pygame.transform.scale(
                pygame.image.load("background.jpg"),
                SIZE)
pygame.display.set_caption("Лабіринт")
clock = pygame.time.Clock()
pygame.mixer.init()
pygame.mixer.music.load("jungles.ogg")
pygame.mixer.music.play()

class GameSprite(pygame.sprite.Sprite):
    def __init__(self, filename:str, size:tuple[int,int], coords: tuple[int,int], speed:int):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load(filename), size)
        self.rect = self.image.get_rect(center=coords)
        self.speed = speed
    def reset(self, window:pygame.Surface):
        window.blit(self.image, self.rect)

class Player(GameSprite):
    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and self.rect.y > 0:
            self.rect.y -= self.speed
        if keys[pygame.K_s] and self.rect.y < HEIGHT-self.rect.height:
            self.rect.y += self.speed
        if keys[pygame.K_d] and self.rect.x < WIDTH-self.rect.width:
            self.rect.x += self.speed
        if keys[pygame.K_a]:
            self.rect.x -= self.speed

class Enemy1(GameSprite):
    def update(self, x1:int, x2:int):

        self.rect.x += self.speed

        if self.rect.x >= x2 or self.rect.x <= x1:
            self.speed = -self.speed
class Enemy2(GameSprite):
    def update_vertical(self, y1:int, y2:int):

        self.rect.y += self.speed

        if self.rect.y >= y2 or self.rect.y <= y1:
            self.speed = -self.speed

class Wall:
    def __init__(self, coords:tuple[int,int], size:tuple[int,int], color:tuple[int,int,int]):
        self.rect = pygame.Rect(coords, size)
        self.color = color
    def draw(self,window:pygame.Surface, width= 0):
        pygame.draw.rect(window, self.color, self.rect, width=width)


player = Player("hero.png", (75,75), (85,90),5)
enemy1 = Enemy1("cyborg.png", (75,75), (700,250), 5)
enemy2 = Enemy2("cyborg.png", (75,75), (600,300), 5)
gold = GameSprite("treasure.png", (75,75), (700, 400), 5)
wall_0 = Wall((0,0),(WIDTH, HEIGHT), (10,240,10))

walls = [
    Wall((5,25),(215,10),(10,240,10)),
    Wall((215,25),(10,340),(10,240,10)),
    Wall((75,25),(20,10),(10,240,10)),
    Wall((215,300),(300,10),(10,240,10)),
    Wall((100,400),(10,100),(250,0,0)),
    Wall((10,190),(90,10),(10,240,10)),
    Wall((135,285),(90,10),(10,240,10))
]

game = True
finish = False
while game:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            print(event.pos)
    if not finish:
        window.blit(background, (0,0))
        player.update()
        enemy1.update(550,730)
        enemy2.update_vertical(185,430)
        player.reset(window)
        enemy2.reset(window)
        enemy1.reset(window)
        gold.reset(window)

        wall_0.draw(window, width=10)

        for w in walls:
            w.draw(window)

        if pygame.sprite.collide_rect(player, enemy1) or pygame.sprite.collide_rect(player, enemy2):
            finish = True  
            kick = pygame.mixer.Sound("kick.ogg")
            kick.play()
            pygame.font.init()
            font1 = pygame.font.Font(None, 48)
            text = font1.render("YOU DIED", True, (255,0,0))
            window.blit(text, (WIDTH//2 - 100,HEIGHT//2)) 

        if pygame.sprite.collide_rect(player, w):
            finish = True  
            kick = pygame.mixer.Sound("kick.ogg")
            kick.play()
            pygame.font.init()
            font1 = pygame.font.Font(None, 48)
            text = font1.render("YOU DIED", True, (255,0,0))
            window.blit(text, (WIDTH//2 - 100,HEIGHT//2)) 
        if pygame.sprite.collide_rect(player,gold):
            finish = True  
            kick = pygame.mixer.Sound("money.ogg")
            kick.play()
            pygame.font.init()
            font1 = pygame.font.Font(None, 48)
            text = font1.render("YOU WON", True, (0,0,255))
            window.blit(text, (WIDTH//2 - 100,HEIGHT//2)) 
            

    pygame.display.update()
    clock.tick(FPS)