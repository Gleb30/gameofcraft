#Создай собственный Шутер!

from pygame import *
from random import randint
class GameSprite(sprite.Sprite):
    def __init__(self,player_image, player_x, player_y, width,height, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (width,height))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y ))

class Player(GameSprite):    
    def update(self):
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed

        if keys[K_d] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15,20,-15)
        bullets.add(bullet)


class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()

lost = 0 
score = 0

class Enemy(GameSprite):
    direction = "left"
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost = lost + 1

class Asteroid(GameSprite):
    direction = "left"
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > win_height:
            self.rect.x = randint(80,win_height - 80)
            self.rect.y = 0 
            
win_width = 700
win_height = 500

window = display.set_mode(
    (win_width, win_height)
)
display.set_caption('shooter')
background = transform.scale(
    image.load('2d.jpg'),
    (win_width,win_height)
    )   


mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')
clock = time.Clock()

img_player = 'rocket.png'
img_enemy = 'ufo.png'
img_bullet = 'bullet.png'
img_asteroid = 'asteroid.png'

font.init()
font_1 = font.SysFont('Arial',80)
font_2 = font.SysFont('Arial',80)
WIN = font_1.render("победа!",True,(255,255,255))
LOSE = font_2.render("Вы проиграли!",True,(180,0,0))

font1 = font.SysFont('Arial',36)
font2 = font.SysFont('Arial',40)
player = Player(img_player, 200,400,85,100,5)
monsters = sprite.Group()
asteroids = sprite.Group()
for i in range(1,6):
    monster = Enemy(img_enemy, randint(80,win_width - 80),-40,80,50, randint(1,4))
    monsters.add(monster)
for i in range(1,3):
    asteroid = Asteroid(img_asteroid,randint(80,win_width - 80),-40,80,50, randint(1,4))
    asteroids.add(asteroid)
bullets = sprite.Group()

FPS = 60
game = True
finish = False
while game:

    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                fire_sound.play()
                player.fire()


    if finish != True:
        window.blit(background,(0,0))
        text_lose = font1.render("Пропущено: "+ str(lost),1,(255,255,255))
        window.blit(text_lose,(10,50))
        text_score = font2.render("Счет: "+ str(score), 1,(255,255,255))
        window.blit(text_score,(10,20))
    

        
        player.update()
        player.reset()
        bullets.update()
        bullets.draw(window)
        monsters.update()
        monsters.draw(window)
        asteroids.update()
        asteroids.draw(window)


        collides = sprite.groupcollide(monsters,bullets, True, True)
        for c in collides:
            score = score + 1
            monster = Enemy(img_enemy, randint(80,win_width - 80),-40,80,50, randint(1,4))
            monsters.add(monster)

        
        if sprite.spritecollide(player,monsters, False) or lost >= 30 or sprite.spritecollide(player,asteroids, False):
            finish = True
            window.blit(LOSE, (200,200))
        if score >= 100:
            finish = True
            window.blit(WIN,(200,200))

    

    display.update()
    clock.tick(FPS)
