import pygame as pg
from random import randint

pg.init()

WIDTH, HEIGHT = 900, 600
FPS = 60
# image 32pix
TILE = 30
# sound bg
bg_music = pg.mixer.Sound('sounds/engine.mp3')
bg_music.play(loops=-1)

window = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption('TANKS')
clock = pg.time.Clock()
# background_image
background_image = pg.image.load('images/greenbg.png')
# font
font_ui = pg.font.Font(None, 42)
# img bricks element
img_brick = pg.image.load('images/block/4.png')
# img_brick = [
#     pg.image.load('images/block/1.png'),
#     pg.image.load('images/block/2.png'),
#     pg.image.load('images/block/3.png'),
#     pg.image.load('images/block/4.png'),
#     pg.image.load('images/block/5.png'),
#     pg.image.load('images/block/6.png'),
# ]
# img player upgrade
img_tank = [
    pg.image.load('images/t1.png'),
    pg.image.load('images/t2.png'),
    pg.image.load('images/t3.png'),
    pg.image.load('images/t4.png')
]
# img explosion animation
img_bangs = [
    pg.image.load('images/expl/explosion1.png'),
    pg.image.load('images/expl/explosion2.png'),
    pg.image.load('images/expl/explosion3.png'),
    pg.image.load('images/expl/explosion4.png'),
    pg.image.load('images/expl/explosion5.png'),
    pg.image.load('images/expl/explosion6.png'),
    pg.image.load('images/expl/explosion7.png'),
    pg.image.load('images/expl/explosion8.png'),
    pg.image.load('images/expl/explosion9.png'),
    pg.image.load('images/expl/explosion10.png'),
    pg.image.load('images/expl/explosion11.png'),
    pg.image.load('images/expl/explosion12.png'),
    pg.image.load('images/expl/explosion13.png'),
    pg.image.load('images/expl/explosion14.png'),
    pg.image.load('images/expl/explosion15.png'),
    pg.image.load('images/expl/explosion16.png'),
    pg.image.load('images/expl/explosion17.png'),
    pg.image.load('images/expl/explosion18.png')
]

# img bonus
img_bonus = [
    pg.image.load('images/bonuses/starbonus.png'),
    pg.image.load('images/bonuses/t3.png')
]

# bonus upgrade
MOVE_SPEED = [1, 2, 2, 1, 2, 3, 3, 2]
BULLET_SPEED = [4, 5, 6, 5, 5, 5, 6, 7]
BULLET_DAMAGE = [1, 1, 2, 3, 2, 2, 3, 4]
SHOT_DELAY = [60, 50, 30, 40, 30, 25, 25, 30]


# x,y direction offset
DIRECTS = [[0, -1], [1, 0], [0, 1], [-1, 0]]


class Interface:
    def __init__(self):
        pass

    def update(self):
        pass

    # draw health points
    def draw(self):
        i = 0
        for obj in objects:
            if obj.type == 'tank':
                pg.draw.rect(window, obj.color, (5 + i * 70, 5, 22, 22))
                text = font_ui.render(str(obj.rank), 1, 'black')
                rect = text.get_rect(center=(5 + i * 70 + 11, 5 + 11))
                window.blit(text, rect)

                text = font_ui.render(str(obj.hp), 1, obj.color)
                rect = text.get_rect(center=(5 + i * 70 + 32, 5 + 11))
                window.blit(text, rect)
                i += 1


bang_sound = pg.mixer.Sound('sounds/fire.mp3')


class Tank:
    def __init__(self, color, px, py, direct, key_list):
        objects.append(self)
        self.type = 'tank'
        self.color = color
        self.rect = pg.Rect(px, py, TILE, TILE)
        self.direct = direct
        # speed tanks
        self.move_speed = 2
        # health player
        self.hp = 5
        # shot delay
        self.shot_timer = 2
        self.shot_delay = 40
        self.bullet_speed = 12
        self.bullet_damage = 1
        # key btn list
        self.key_left = key_list[0]
        self.key_right = key_list[1]
        self.key_up = key_list[2]
        self.key_down = key_list[3]
        self.key_shot = key_list[4]
        # tank upgrade
        self.rank = 0
        self.image = pg.transform.rotate(img_tank[self.rank], -self.direct * 90)
        self.rect = self.image.get_rect(center=self.rect.center)

    # movies, transorf img
    def update(self):
        self.image = pg.transform.rotate(img_tank[self.rank], -self.direct * 90)
        self.image = pg.transform.scale(self.image, (self.image.get_width() - 5,
                                                     self.image.get_height() -5))
        self.rect = self.image.get_rect(center=self.rect.center)
        # tank characteristics
        self.move_speed = MOVE_SPEED[self.rank]
        self.shot_delay = SHOT_DELAY[self.rank]
        self.bullet_speed = BULLET_SPEED[self.rank]
        self.bullet_damage = BULLET_DAMAGE[self.rank]

        # old pos if collicion tank
        old_x, old_y = self.rect.topleft
        if keys[self.key_left]:
            self.rect.x -= self.move_speed
            self.direct = 3
        elif keys[self.key_right]:
            self.rect.x += self.move_speed
            self.direct = 1
        elif keys[self.key_up]:
            self.rect.y -= self.move_speed
            self.direct = 0
        elif keys[self.key_down]:
            self.rect.y += self.move_speed
            self.direct = 2
        # tanks block blocks
        for obj in objects:
            if obj != self and obj.type == 'block' and self.rect.colliderect(obj.rect):
                self.rect.topleft = old_x, old_y

        # shooting
        if keys[self.key_shot] and self.shot_timer == 0:
            # speed bullets
            dx = DIRECTS[self.direct][0] * self.bullet_speed
            dy = DIRECTS[self.direct][1] * self.bullet_speed
            Bullet(self, self.rect.centerx, self.rect.centery, dx, dy, self.bullet_damage)
            self.shot_timer = self.shot_delay
            # sound
            self.bang_sound = pg.mixer.Sound('sounds/bullet-ricochet-01.mp3')
            self.bang_sound.set_volume(5)
            self.bang_sound.play()
        # shot delay(задержка выстрела)
        if self.shot_timer > 0:
            self.shot_timer -= 0.5

    def draw(self):
        window.blit(self.image, self.rect)

    def damage(self, value):
        # sound
        self.expl_sound = pg.mixer.Sound('sounds/expl.mp3')
        self.hp -= value
        if self.hp <= 0:

            # sound
            self.expl_sound.set_volume(5)
            self.expl_sound.play()
            objects.remove(self)
            print(self.color, 'dead')


class Bullet:
    def __init__(self, parent, px, py, dx, dy, damage):
        bullets.append(self)
        self.parent = parent
        self.px, self.py = px, py
        self.dx, self.dy = dx, dy
        self.damage = damage

    def update(self):
        # sound
        self.ricocheted_sound = pg.mixer.Sound('sounds/fire.mp3')
        self.ricocheted_sound.set_volume(5)

        self.px += self.dx
        self.py += self.dy
        # if pos bullet exited the screen
        if self.px < 0 or self.px > WIDTH or self.py < 0 or self.py > HEIGHT:
            bullets.remove(self)
        else:
            for obj in objects:
                # method checks the collision of the object with the coordinate True
                if obj != self.parent and obj.type != 'bang' and obj.type != 'bonus':
                    if obj.rect.collidepoint(self.px, self.py):
                        obj.damage(self.damage)
                        # if hits - bullets remove
                        bullets.remove(self)
                        # boom!
                        Bang(self.px, self.py)
                        self.ricocheted_sound.play()
                        break

    def draw(self):
        pg.draw.circle(window, 'white', (self.px, self.py), 2)


class Bang:
    def __init__(self, px, py):
        objects.append(self)
        self.type = 'bang'
        self.px, self.py = px, py
        self.frame = 0
        pass

    def update(self):
        # one frame one expl
        self.frame += 0.5
        if self.frame >= 18:
            objects.remove(self)

    def draw(self):
        # animation explosion
        image = img_bangs[int(self.frame)]
        rect = image.get_rect(center=(self.px, self.py))
        window.blit(image, rect)


class Block:
    def __init__(self, px, py, size):
        objects.append(self)
        self.type = 'block'
        self.rect = pg.Rect(px, py, size, size)
        # health block
        self.hp = 1

    def update(self):
        pass

    def draw(self):
        window.blit(img_brick, self.rect)

    def damage(self, value):
        self.hp -= value
        if self.hp <= value:
            objects.remove(self)


class Bonus:
    def __init__(self, px, py, bonusNum):
        objects.append(self)
        self.type = 'bonus'

        self.image = img_bonus[bonusNum]
        self.rect = self.image.get_rect(center=(px, py))

        self.timer = 600
        self.bonusNum = bonusNum

    def update(self):
        self.bang_sound = pg.mixer.Sound('sounds/pampambonus.mp3')
        self.bang_sound.set_volume(5)
        if self.timer > 0:
            self.timer -= 1
        else:
            objects.remove(self)

        for obj in objects:
            if obj.type == 'tank' and self.rect.colliderect(obj.rect):
                if self.bonusNum == 0:
                    if obj.rank < len(img_tank) - 1:
                        obj.rank += 1
                        # sound
                        self.bang_sound.play()
                        objects.remove(self)
                        break
                elif self.bonusNum == 1:
                    # sound
                    self.bang_sound.play()
                    obj.hp += 1
                    objects.remove(self)
                    break

    def draw(self):
        if self.timer % 30 < 15:
            window.blit(self.image, self.rect)


bullets = []
# obj - color tank, coordinates, direction, buttons
objects = []
Tank('green', 100, 275, 0, (pg.K_a, pg.K_d, pg.K_w, pg.K_s, pg.K_SPACE))
Tank('red', 650, 275, 0, (pg.K_LEFT, pg.K_RIGHT, pg.K_UP, pg.K_DOWN, pg.K_KP_ENTER))

Ui = Interface()

# block in window
Block(100, 100, TILE)

for b in range(80):
    while True:
        x = randint(0, WIDTH // TILE) * TILE
        y = randint(1, HEIGHT // TILE) * TILE
        rect = pg.Rect(x, y, TILE, TILE)
        finded = False
        for obj in objects:
            if rect.colliderect(obj.rect):
                finded = True

        if not finded:
            break

    Block(x, y, TILE)

bonusTimer = 360

play = True

while play:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            play = False
    # traffic control
    keys = pg.key.get_pressed()

    if bonusTimer > 0:
        bonusTimer -= 1
    else:
        Bonus(randint(50, WIDTH - 50), randint(50, HEIGHT - 50), randint(0, len(img_bonus) - 1))
        bonusTimer = randint(120, 240)

    # update obj
    for bullet in bullets:
        bullet.update()
    for obj in objects:
        obj.update()
    Ui.update()
    # background
    window.blit(background_image, (0, 0))

    # update obj
    for bullet in bullets:
        bullet.draw()
    for obj in objects:
        obj.draw()
    Ui.draw()

    pg.display.update()
    clock.tick(FPS)

pg.quit()