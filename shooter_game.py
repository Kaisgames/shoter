from pygame import *
from random import randint
from time import time as timer

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        sprite.Sprite.__init__(self)

        self.image = transform.scale(
            image.load(player_image), (size_x, size_y))
        self.speed = player_speed

        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < win_width - 80:
            self.rect.x += self.speed

    def fire(self):
        batla = Bullet(img_ratatatata, self.rect.centerx, self.rect.top, 16, 16, -15)
        batlas.add(batla)

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost += 1
        
class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()

#class Asteroid(GameSprite):
#    def update(self):
#        self.rect.y += self.speed
#        if self.rect.y > win_height:
#            self.rect.x = randint(80, win_width - 80)
#            self.rect.y = 0
            
font.init()
font1 = font.SysFont('Arial', 36)
font2 = font.SysFont('Arial', 80)
win = font2.render("YOU WIN!!!", True, (0, 0, 255))
lose = font2.render('YOU LOSE', True, (196, 132, 13))


win_width = 700
win_height = 500

img_back = 'road.png'
img_hero = 'hero.png'
img_cop = 'cop.png'
img_ratatatata = 'bullet.png'
ast = "asteroid.png"

score = 0
lost = 0
goal = 30
life = 3
max_lose = 3

window = display.set_mode((win_width, win_height))
display.set_caption('Race')

mixer.init()
mixer.music.load('risk.mp3')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')

window = display.set_mode((win_width, win_height))
backround = transform.scale(image.load(img_back), (win_width, win_height))

car = Player(img_hero, 5, win_height - 100, 50, 100, 10)

cops = sprite.Group()
for i in range(1, 5):
    zluka = Enemy(img_cop, randint(80, win_width - 80), -40, 50, 100, randint(5, 15))
    cops.add(zluka)

#asteroids = sprite.Group()
#for i in range(1, 3):
#    asteroid = Asteroid(ast, randint(80, win_width - 80), -40, 40, 50, randint(1, 3))
#    asteroids.add(asteroid)

batlas = sprite.Group()

super_finish = False
run = True
FPS = 60
rel_time = False
num_fire = 0

while run:
    for i in event.get():
        if i.type == QUIT:
            run = False

        elif i.type == KEYDOWN:
            if i.key == K_SPACE:
                if num_fire < 5 and rel_time == False:
                    num_fire += 1
                    fire_sound.play()
                    car.fire()
                if num_fire >= 5 and rel_time == False:
                    last_time = timer()
                    rel_time = True

    if not super_finish:
        window.blit(backround, (0, 0))

        text =  font1.render('Score:' + str(lost) + '/30', 1, (0, 0, 0))
        window.blit(text, (10, 20))

        t_lose = font1.render('Wins:' + str(score), 1, (255, 255, 255))
        window.blit(t_lose, (10, 50))


        car.update()
        cops.update()
        batlas.update()
        #asteroid.update()
        car.reset()

        #asteroids.draw(window)
        cops.draw(window)
        batlas.draw(window)

        if rel_time == True:
            now_time = timer()

            if now_time - last_time < 2:
                reload = font2.render('Wait, reload...', 1, (150, 0, 0))
                window.blit(reload, (260, 460))
            else:
                num_fire = 0
                rel_time = False

        collides = sprite.groupcollide(cops, batlas, True, True)
        for i in collides:
            score += 1
            zluka = Enemy(img_cop, randint(80, win_width - 80), -40, 50, 100, randint(5, 15))
            cops.add(zluka)

        if sprite.spritecollide(car, cops, False): #or sprite.spritecollide(car, asteroids, False)
            sprite.spritecollide(car, cops, True)
            #sprite.spritecollide(car, asteroids, True)
            life -= 1

        if lost >= goal:
            super_finish = True
            window.blit(win, (200, 200))
            score += 1
            

        if life == 0:# or lost >= max_lose:
            super_finish = True
            window.blit(lose, (200, 200))

        if life == 3:
            life_color = (0, 150, 0)

        if life == 2:
            life_color = (150, 150, 0)

        if life == 1:
            life_color = (150, 0, 0)

        text_life = font1.render(str(life), 1, life_color)
        window.blit(text_life, (650, 10))

        

        display.update() 
    else:
        super_finish = False
        #score = 0
        lost = 0
        num_fire = 0
        life = 3
        for i in batlas:
            i.kill()
        for i in cops:
            i.kill()
        #for i in asteroids:
        #    i.kill()

        time.delay(FPS)
        for i in range(1, 5):
            zluka = Enemy(img_cop, randint(80, win_width - 80), -40, 50, 100, randint(5, 15))
            cops.add(zluka)
        #for i in range(1, 3):
        #    asteroid = Asteroid(ast, randint(80, win_width - 80), -40, 40, 50, randint(1, 3))
        #    asteroids.add(asteroid)
    time.delay(FPS)
                                      



