from pygame import *
mixer.init()
from time import time as timer
init()
from time import time as time_count
from random import*
# Window
window = display.set_mode((700, 600))
display.set_caption("Space Shooter")
background = transform.scale(image.load("galaxy.jpg"), (700, 600))

mixer.music.load("space.ogg")
#mixer.music.play()
# Timer
clock = time.Clock()

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), size)
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def draw_sprite(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

shot_time = time_count() # Засікти час

class Player(GameSprite):
    def update(self, bullets): # bullets - список куль
        global shot_time
        # Реалізування руху по клавішах
        pressed_keys = key.get_pressed()
        if pressed_keys[K_w]:
            self.rect.y -= self.speed
        if pressed_keys[K_s]:
            self.rect.y += self.speed
        if pressed_keys[K_a]:
            self.rect.x -= self.speed
        if pressed_keys[K_d]:
            self.rect.x += self.speed

        if pressed_keys[K_SPACE]:
            if time_count() - shot_time >= 0.5: # Якщо пройшла секунда
                bullet_x = self.rect.x + 28
                bullets.add(Bullet("bullet.png", bullet_x, self.rect.y, (10, 20), 10))
                shot_time = time_count() # Засікти заново

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed # Рухатися вгору
        self.draw_sprite()

class Enemy(GameSprite):
    def update(self): # Ця функція буде для руху і обробки чогось
        global lives
        self.rect.y += self.speed
        self.draw_sprite()
        if self.rect.y > 600:
            self.kill()
            lives -= 1

def draw_label(score):
    image = font.SysFont("Century Gothic", 20).render("Ворогів вбито " + str(score), True, (255, 255, 255))
    window.blit(image, (20, 50))

lives = 3 # Встановити життя на 3

heart = transform.scale(image.load("heart.png"), (20, 20))

def draw_heart():
    global heart
    x = 50
    for i in range(lives): # Повторити стільки разів, скільки життів у нас
        window.blit(heart, (x, 20))
        x += 30

player = Player("rocket.png", 200, 500, (65, 90), 5)
bullet = Bullet("bullet.png", 223, 450, (20, 20), 5)

game = True
score = 0

bullets = sprite.Group()

enemies_group = sprite.Group()
# Створення ворогів
enemy1 = Enemy("ufo.png", 0, 0, (80, 50), 1)
enemy2 = Enemy("ufo.png", 140, 0, (80, 50), 1)
enemy3 = Enemy("ufo.png", 500, 0, (80, 50), 1)

# Додавання ворогів у групу спрайтів
enemies_group.add(enemy1, enemy2, enemy3)

while game:
    if len(enemies_group) < 7: #Якщо кількість елементів у групі < 7:
        enemy = Enemy("ufo.png", randint(0, 600), 0, (80, 50), 1)

        for s in enemies_group.sprites():
            if s.rect.colliderect(enemy.rect):
                new_enemy = Enemy('ufo.png', randint(0, 600), -100, (80, 50), 1)
        enemies_group.add(enemy)

    # Exit on cross
    for e in event.get():
        if e.type == QUIT:
            game = False

    sprite.groupcollide(bullets, enemies_group, True, True)        
    window.blit(background, (0, 0))
    for bullet in bullets:
        bullets.update()   
        bullet.draw_sprite()
        if bullet.rect.y <= -20:
            bullets.remove(bullet)
    player.update(bullets)
    player.draw_sprite()
    draw_heart()
    enemies_group.update()
    draw_label(score)
    display.update()
    clock.tick(60)