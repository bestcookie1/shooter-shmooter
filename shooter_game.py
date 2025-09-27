#Создай собственный Шутер!
import pygame
import random
import time as vremya
from random import randint

class GameSprite(pygame.sprite.Sprite): # !the main class
    def __init__(self, filename, x, y, width, height, speed):
        super().__init__()
        self.image = pygame.transform.scale(
            pygame.image.load(filename), (width, height)
        )
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed
    def draw(self):
        window.blit(self. image, self.rect)

class Player(GameSprite):# * our player
    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT] and self.rect.right < W:
            self.rect.x += self.speed
        elif keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
    def fire(self):
        bullets.add(
            Bullet("bullet.png",self.rect.centerx, self.rect.top, 10, 10, 5)
        )

false_count = 0


class Enemy(GameSprite):# TODO: angry aliens )
    def update(self):
        global false_count
        self.rect.y += self.speed
        if self.rect.y > H:
            self.speed = randint(1,2)
            self.rect.y =  randint(-300, 150)
            self.rect.x = randint(0, W)
            false_count += 1

class Asteroid(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > H:
            self.speed = 3
            self.rect.y = randint(-100,200)
            self.rect.x = randint(0, W)


class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()

bullets = pygame.sprite.Group()


pygame.init()

W, H = 700,500
FPS = 120



back = pygame.transform.scale(
    pygame.image.load("galaxy.jpg"), (W, H))

window = pygame.display.set_mode((W,H))
pygame.display.set_caption('shooter')

clock = pygame.time.Clock()

pygame.mixer.music.load('space.ogg')
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play()

ki = pygame.mixer.Sound('fire.ogg')

rocket = Player("rocket.png", 250, 400, 80, 100, 5)

font1 = pygame.font.SysFont('Arial', 30)
counter_false = font1.render(
    'Пропущено:' + str(false_count), True, (255, 255, 255)
    
)

life_count = 3
ccount = font1.render(
    str(life_count), True, (255,255,255)
)

die_count = 0
count= font1.render(
    'Счёт:' + str(die_count), True, (255, 255, 255)
)


aliens = pygame.sprite.Group()
aliens.add(
    Enemy("ufo.png", randint(0,W), randint(-300, 150), 60, 50,randint(1,2)),
    Enemy("ufo.png", randint(0,W), randint(-300, 150), 60, 50,randint(1,2)),
    Enemy("ufo.png", randint(0,W), randint(-300, 150), 60, 50,randint(1,2)),
    Enemy("ufo.png", randint(0,W), randint(-300, 150), 60, 50,randint(1,2)),
    Enemy("ufo.png",randint(0,W), randint(-300, 150), 60, 50,randint(1,2))
)

asteroids = pygame.sprite.Group()
asteroids.add(
    Asteroid("asteroid.png", randint(0,W), randint(-100,200), 70, 60, 3),
    Asteroid("asteroid.png", randint(0,W), randint(-100,200), 70, 60, 3)
)

num_fire = 0
rel_time = False

game = True

finish = False

while game:
    counter_false = font1.render(
    'Пропущено:' + str(false_count), True, (255, 255, 255))
    count= font1.render(
    'Счёт:' + str(die_count), True, (255, 255, 255)
)
    collides = pygame.sprite.groupcollide(
        bullets, aliens, True, True
    )
    for collide in collides:
        die_count += 1
        aliens.add(
            Enemy("ufo.png", randint(0,W), randint(-300, 150), 60, 50,randint(1,3))
        )
    collides2 = pygame.sprite.spritecollide(
        rocket, aliens, True
    )

    for collide in collides2:
            life_count -= 1
            ccount = font1.render(
                str(life_count), True, (255,255,255)
            )
            aliens.add(
            Enemy("ufo.png", randint(0,W), randint(-300, 150), 60, 50,randint(1,3))
        )


    collides3 = pygame.sprite.spritecollide(
        rocket, asteroids, True


            )
    for collide in collides3:
        life_count -= 1
        ccount = font1.render(
            str(life_count), True, (255,255,255)
        )
        asteroids.add(
        Asteroid("asteroid.png", randint(0,W), randint(-100,200), 70, 60, 3)
    )

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if num_fire < 5 and rel_time == False:
                    ki.play()
                    num_fire += 1
                    rocket.fire()
                if num_fire >= 5 and rel_time == False:
                    rel_time = True
                    start = vremya.time()
            if finish and event.key == pygame.K_r:
                finish = False
                false_count = 0
                die_count = 0
                aliens.empty()
                bullets.empty()
                aliens.add(
                Enemy("ufo.png", randint(0,W), randint(-300, 150), 60, 50,randint(1,3)),
                Enemy("ufo.png", randint(0,W), randint(-300, 150), 60, 50,randint(1,3)),
                Enemy("ufo.png", randint(0,W), randint(-300, 150), 60, 50,randint(1,3)),
                Enemy("ufo.png", randint(0,W), randint(-300, 150), 60, 50,randint(1,3)),
                Enemy("ufo.png",randint(0,W), randint(-300, 150), 60, 50,randint(1,3))
            )
                pygame.mixer.music.play()
    
    if not finish:
        rocket.update()
        bullets.update()
        aliens.update()
        asteroids.update()
        window.blit(back, (0,0))
        rocket.draw()
        bullets.draw(window)
        aliens.draw(window)
        asteroids.draw(window)
        window.blit(counter_false, (100, 50))
        window.blit(count, (100, 70))
        window.blit(ccount, (100, 90))
        if die_count == 3:
            finish = True
            Win = font1.render(
            'YOU WIN!', True, (255, 255, 255))
            window.blit(Win, (300,250))
            pygame.mixer.music.stop()

        if false_count == 10:
            finish = True
            lose = font1.render(
            'YOU LOSE!', True, (255, 255, 255))
            window.blit(lose, (300,250))
            pygame.mixer.music.stop()

        if life_count <= 0:
            finish = True
            lose = font1.render(
            'YOU LOSE!', True, (255, 255, 255))
            window.blit(lose, (300,250))
            pygame.mixer.music.stop()
        if rel_time:
            end = vremya.time()
            if end-start <= 3:
                wai = font1.render(
                    'Wait, reload...', True, (138, 0, 0))
                window.blit(wai, (300,250))
            else:
                num_fire = 0
                rel_time = False
                
            


    pygame.display.update()
    clock.tick(FPS)

