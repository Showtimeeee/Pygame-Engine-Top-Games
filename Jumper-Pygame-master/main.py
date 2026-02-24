import pygame as pg
import random
import os
from pygame import mixer
import json


mixer.init()
pg.init()


WIDTH = 500
HEIGHT = 700

screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption('Jumper')

# game fps
clock = pg.time.Clock()
fps = 60

# sound
pg.mixer.music.load('sound/8BitDreamscapeTheWholeOther.mp3')
pg.mixer.music.set_volume(0.5)
pg.mixer.music.play(-1, 0.0)
jump_sound = pg.mixer.Sound('sound/jumpik.mp3')
jump_sound.set_volume(0.3)
death_sound = pg.mixer.Sound('sound/kapelki.mp3')
death_sound.set_volume(0.5)

# scroll
scroll_thresh = 200

# gravitation
gravity = 1

max_platforms = 10

# scroll line
scroll = 0

bg_scroll = 0

# colors
game_color = (95, 10, 110)
white_color = (255, 255, 255)
black_color = (0, 0, 0)
purple_color = (185, 37, 156)

# font
font_mini = pg.font.SysFont('Open Sans', 30)
font_big = pg.font.SysFont('Monaco', 50)
#
game_over = False

# start score
score = 0

# hight scrore
hight_scrore = 0

# file to score
if os.path.exists('score_j.txt'):
    with open('score_j.txt', 'r') as file:
        hight_scrore = json.load(file)
else:
    hight_scrore = 0

player_image = pg.image.load('images/playerb5.png').convert_alpha()
bg_image = pg.image.load('images/bgvektor.jpg').convert_alpha()
platform_image = pg.image.load('images/wood111z.png').convert_alpha()

# text
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

# score textpanel
def score_panel():
    pg.draw.rect(screen, purple_color, (0, 0, WIDTH, 30))
    pg.draw.line(screen, game_color, (0, 30), (WIDTH, 30), 2)
    draw_text('Score: ' + str(score), font_big, game_color, 0, 0)


# drawing background
def draw_bg(bg_scroll):
    screen.blit(bg_image, (0, 0 + bg_scroll))
    screen.blit(bg_image, (0, -200))


class Player:
    def __init__(self, x, y):
        # shape, size player
        self.image = pg.transform.scale(player_image, (45, 60))
        self.width = 40
        self.height = 60
        self.rect = pg.Rect(0, 0, self.width, self.height)
        self.rect.center = (x, y)
        self.vel_y = 0
        self.flip = False

    def move(self):
        # change of coordinates
        scroll = 0
        dx = 0
        dy = 0
        # buttons
        key = pg.key.get_pressed()
        if key[pg.K_a]:
            dx = -10
            self.flip = True
        if key[pg.K_d]:
            dx += 10
            self.flip = False

        # gravity vel
        self.vel_y += gravity
        dy += self.vel_y

        # screen window
        if self.rect.left + dx < 0:
            dx = -self.rect.left
        if self.rect.right + dx > WIDTH:
            dx = WIDTH - self.rect.right

        # collision platform
        for platform in platform_group:
            if platform.rect.colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                if self.rect.bottom < platform.rect.centery:
                    if self.vel_y > 0:
                        dy = 0
                        self.rect.bottom = platform.rect.top
                        self.vel_y = -20
                        jump_sound.play()

        if self.rect.top <= scroll_thresh:
            # if jump
            if self.vel_y < 0:
                scroll = -dy

        # new pos
        self.rect.x += dx
        self.rect.y += dy + scroll

        return scroll

    def draw(self):
        screen.blit(pg.transform.flip(self.image, self.flip, False), (self.rect.x -3, self.rect.y - 1))


class Platform(pg.sprite.Sprite):
    def __init__(self, x, y, width, moving):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.transform.scale(platform_image, (width, 10))
        self.moving = moving
        self.move_counter = random.randint(0, 50)
        self.direction = random.choice([-1, 1])
        self.speed = random.randint(1, 2)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    # update platform pos
    def update(self, scroll):

        # moving platform
        if self.moving == True:
            self.move_counter += 1
            self.rect.x += self.direction * self.speed

        # platform direction if moved
        if self.move_counter >= 100 or self.rect.left < 0 or self.rect.right > WIDTH:
            self.direction *= -1
            self.move_counter = 0

        self.rect.y += scroll
        # if platform gone to screen
        if self.rect.top > HEIGHT:
            self.kill()


jumper = Player(WIDTH // 2, HEIGHT - 150)

# platform sprite
platform_group = pg.sprite.Group()
platform = Platform(WIDTH // 2, HEIGHT - 50, 80, False)
platform_group.add(platform)

run = True
while run:

    clock.tick(fps)

    if game_over == False:
        scroll = jumper.move()

        # draw background
        bg_scroll += scroll
        if bg_scroll >= 600:
            bg_scroll = 0
        draw_bg(bg_scroll)

        # add platforms, size, location
        if len(platform_group) < max_platforms:
            p_w = random.randint(40, 60)
            p_x = random.randint(0, WIDTH - p_w)
            # moving platform
            p_type = random.randint(1, 2)
            if p_type == 1 and score > 500:
                p_moving = True
            else:
                p_moving = False
            p_y = platform.rect. y - random.randint(80, 120)
            platform = Platform(p_x, p_y, p_w, p_moving)
            platform_group.add(platform)

        platform_group.update(scroll)

        # +score
        if scroll > 0:
            score += scroll

        # draw sprites
        platform_group.draw(screen)
        jumper.draw()

        # draw score
        score_panel()

        # if game over
        if jumper.rect.top > HEIGHT:
            game_over = True
            death_sound.play()

    else:
        draw_text('Score: ' + str(score), font_big, white_color,140, 50 )
        draw_text('Game Over', font_big, white_color, 140, 100)
        draw_text('Press SPACE', font_big, white_color, 120, 350 )

        # update records write file
        if score > hight_scrore:
            hight_scrore = score

            with open('score_j.txt', 'w') as file:
                json.dump(hight_scrore, file)

        # if game over press SPACE
        key = pg.key.get_pressed()
        if key[pg.K_SPACE]:
            # reset
            game_over = False
            score = 0
            scroll = 0
            jumper.rect.center = (WIDTH // 2, HEIGHT - 100)
            # reset platforms
            platform_group.empty()
            # add new platforms
            platform = Platform(WIDTH // 2 - 50, HEIGHT - 50, 100, 0)
            platform_group.add(platform)

    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False

    pg.display.update()

pg.quit()
