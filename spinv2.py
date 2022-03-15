import pygame
from pygame.locals import *
import random 

pygame.font.init() 
pygame.init()

#def fps
clock = pygame.time.Clock()
fps = 60

#colors
green = (0, 255, 0)
red = (255, 0, 0)
white = (255, 255, 255)

#game var
rows =5
cols = 5
game_over=0
score=0
high_score=0
alien_cooldown = 1000
last_alien_shot = pygame.time.get_ticks()

#screen
screen = pygame.display.set_mode((1200, 1000))
pygame.display.set_caption('Space Invaders')

#define fonts
font20 = pygame.font.SysFont('Constantia', 20)
font60 = pygame.font.SysFont('Constantia', 60)

#image bg
bg =pygame.image.load("img/r12.jpg")

def draw_bg():
    screen.blit(bg, (0, 0))

#draw text
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

#spaceship
class Spaceship(pygame.sprite.Sprite):
    def __init__(self, x, y, health):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("img/spship.png")
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.health_remaining = health
        self.health_start = health
        self.last_shot = pygame.time.get_ticks()
        

    def update(self):
        game_over=0
        cooldown = 500
        #key press
        key = pygame.key.get_pressed()
        if key[pygame.K_a] and self.rect.left > 0:
            self.rect.x += -10
        if key[pygame.K_d] and self.rect.right < 1200:
            self.rect.x += 10

        time_now = pygame.time.get_ticks()

        if key[pygame.K_SPACE] and time_now -self.last_shot > cooldown:
            bullet = Bullets(self.rect.centerx, self.rect.top)
            bullet_group.add(bullet)
            self.last_shot = time_now
        
        #draw health bar
        pygame.draw.rect(screen, red, (self.rect.x, (self.rect.bottom + 10), self.rect.width, 15))
        if self.health_remaining >0:
            pygame.draw.rect(screen, green, (self.rect.x, (self.rect.bottom + 10), (self.rect.width * (self.health_remaining/self.health_start)), 15))
        elif self.health_remaining <0:
            self.kill() 
            game_over=1
        return game_over        

#bullets
class Bullets(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("img/bullet.png")
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

    def update(self):
        self.rect.y -=5
        if self.rect.bottom < 0:
            self.kill()
        if pygame.sprite.spritecollide(self, alien_group, True):
            self.kill()
            
        

class Aliens(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("img/invd.png")
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.move_counter = 0
        self.move_direction = 1
    def update (self):
        self.rect.x += self.move_direction
        self.move_counter += 2
        if abs(self.move_counter)> 600:
            self.move_direction *= -1
            self.move_counter *= self.move_direction

#Aliens bullets
class Alien_Bullets(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("img/alien_bullet.png")
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

    def update(self):
        self.rect.y +=2
        if self.rect.top > 1200:
            self.kill()
        if pygame.sprite.spritecollide(self, spaceship_group, False):
            self.kill()
            spaceship.health_remaining -= 1
        if pygame.sprite.spritecollide(self, bunker_group, True):
            self.kill()
            
        

class Bunker(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([8, 8])
        self.image.fill(green)
        self.rect = self.image.get_rect()



spaceship_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
alien_group = pygame.sprite.Group()
alien_bullet_group = pygame.sprite.Group()
bunker_group = pygame.sprite.Group()

def create_aliens ():
    for row in range(rows):
        for col in range(cols):
            alien = Aliens(400 + col * 100, 100 + row * 70)
            alien_group.add(alien)

create_aliens()

def create_bunkers ():
    for bunk in range(4):
        for row in range(5):
            for col in range(10):
                bunker = Bunker()
                bunker.rect.x = (100 +(275 * bunk))+(10*col)
                bunker.rect.y = 650 + (10* row)
                bunker_group.add(bunker)

create_bunkers()

spaceship= Spaceship(600, 800, 3)
spaceship_group.add(spaceship)


run = True
play = False
while run:
    clock.tick(fps)
    time_now = pygame.time.get_ticks()
    draw_bg()
    #Highscore
    font = pygame.font.SysFont('Constantia', 40)
    text = font.render('Highscore: ' + str(high_score), False, white)
    textRect = text.get_rect()
    textRect.center = (160, 100)
    screen.blit(text, textRect)
    if play:
        #create alien bullets    
        if time_now - last_alien_shot > alien_cooldown and len(alien_bullet_group)<8 and len(alien_group)>0:
            attacking_alien = random.choice(alien_group.sprites())
            alien_bullet = Alien_Bullets(attacking_alien.rect.centerx, attacking_alien.rect.bottom)
            alien_bullet_group.add(alien_bullet)
            last_alien_shot = time_now

        if len(alien_group)==0:
            game_over=1    
        #draw
        spaceship_group.draw(screen)
        bullet_group.draw(screen)
        alien_group.draw(screen)
        alien_bullet_group.draw(screen)
        bunker_group.draw(screen)

        if game_over == 0:
            #Score
            score = 25 - len(alien_group)
            font = pygame.font.SysFont('Constantia', 40)
            text = font.render('Score: ' + str(score), False, white)
            textRect = text.get_rect()
            textRect.center = (120, 150)
            screen.blit(text, textRect)
            #update 
            game_over = spaceship.update()
            bullet_group.update()
            alien_group.update()
            alien_bullet_group.update()
            bunker_group.update()
            pygame.display.update()
            
        else:
            if score>high_score:
                high_score=score
            score = 0
            play = False

    else:
       draw_text('Press SPACE to start!',font60, white, 300, 500)
       key = pygame.key.get_pressed()
       if key[pygame.K_SPACE]: 
           play = True 
       game_over=0
       

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()      
       
    
    
        
pygame.quit()