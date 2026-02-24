import pygame as pg
from random import randint

pg.init()
WIDTH, HEIGHT = 800, 600
FPS = 60

bg_music = pg.mixer.Sound('sounds/bgmus.wav')
bg_music.set_volume(0.3)
bg_music.play(loops=-1)
mah_sound = pg.mixer.Sound('sounds/mah.wav')
mah_sound.set_volume(0.5)
fail_sound = pg.mixer.Sound('sounds/carrr.wav')
fail_sound.set_volume(0.5)

window = pg.display.set_mode((WIDTH, HEIGHT))
clock = pg.time.Clock()

pg.display.set_caption('Flappy crow')
pg.display.set_icon(pg.image.load('image/crow/raven.ico'))

font_score = pg.font.Font(None, 40)
font_game_over = pg.font.Font(None, 40)

img_bg = pg.image.load('image/bg/c.jpg')
img_crow = pg.image.load('image/crow/crowanim.png')
img_toprock = pg.image.load('image/rock/1.png')
img_botrock = pg.image.load('image/rock/2.png')

# player pos y, sy-speed, ay-jump
py, sy, ay = HEIGHT // 2, 0, 0
player = pg.Rect(WIDTH // 3, py, 40, 42)
state = 'start'
frame = 0
timer = 10
rocks = []
bgs = []
rock_scores = []
bgs.append(pg.Rect(0, 0, 288, 600))
lives = 3
scores = 0
rock_speed = 3
# rock gate
gate_size = 200
gate_pos = HEIGHT // 2

play = True
while play:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            play = False
    # controls
    press = pg.mouse.get_pressed()
    keys = pg.key.get_pressed()
    click = press[0] or keys[pg.K_SPACE]

    # timer
    if timer:
        timer -= 1

    # change frame
    frame = (frame + 0.1) % 4

    for i in range(len(bgs)-1, -1, -1):
        bg = bgs[i]
        bg.x -= rock_speed // 2
        # drop rocks if off window
        if bg.right < 0:
            bgs.remove(bg)

        # gluing picture for the background
        if bgs[len(bgs)-1].right <= WIDTH:
            bgs.append(pg.Rect(bgs[len(bgs)-1].right, 0, 288, 600))

    # obstacles
    for i in range(len(rocks)-1, -1, -1):
        rock = rocks[i]
        rock.x -= rock_speed
        # drop rocks if off window
        if rock.right < 0:
            rocks.remove(rock)
            if rock in rock_scores:
                rock_scores.remove(rock)

    # state parameters
    if state == 'start':
        if click and not timer and not len(rocks):
            mah_sound.play()
            state = 'play'
        # return pos
        py += (HEIGHT // 2 - py) * 0.1
        player.y = py
    elif state == 'play':
        if click:
            ay = -2
        else:
            ay = 0
        # player gravity
        py += sy
        sy = (sy + ay + 1) * 0.98
        player.y = py

        # add rocks, gate
        if not len(rocks) or rocks[len(rocks)-1].x < WIDTH - 200:
            rocks.append(pg.Rect(WIDTH, 0, 62, gate_pos - gate_size // 2))
            rocks.append(pg.Rect(WIDTH, gate_pos + gate_size // 2, 52, HEIGHT - gate_pos + gate_size // 2))
            # change pos gate algorithm
            gate_pos += randint(-100, 100)
            if gate_pos < gate_size:
                gate_pos = gate_size
            elif gate_pos > HEIGHT - gate_size:
                gate_pos = HEIGHT - gate_size

        # collision
        if player.top < 0 or player.bottom > HEIGHT:
            state = 'fail'

        for rock in rocks:
            if player.colliderect(rock):
                state = 'fail'
            # add scores after rock
            if rock.right < player.left and rock not in rock_scores:
                rock_scores.append(rock)
                scores += 5
                # score to speed
                rock_speed = 3 + scores // 100

    elif state == 'fail':
        fail_sound.play()
        # reset to start
        sy, ay = 0, 0
        # return gate pos
        gate_pos = HEIGHT // 2
        lives -= 1
        if lives:
            state = 'start'
            # delay before start 1 min
            timer = 60
        else:
            font_score = pg.font.Font(None, 60)
            state = 'game over'
            timer = 120
    else:
        py += sy
        sy = (sy + ay + 1) * 0.98
        player.y = py
        # if timer == 0
        if not timer:
            play = False

    # bg
    for bg in bgs:
        window.blit(img_bg, bg)

    # obstacle location
    for rock in rocks:
        if not rock.y:
            rect = img_botrock.get_rect(bottomleft=rock.bottomleft)
            window.blit(img_botrock, rect)
        else:
            rect = img_botrock.get_rect(topleft=rock.topleft)
            window.blit(img_toprock, rect)

    image = img_crow.subsurface(60 * int(frame), 0, 40, 50)
    # raven spin anim 'nose up'
    image = pg.transform.rotate(image, -sy * 2)
    window.blit(image, player)
    # scores text
    text = font_score.render('Score: ' + str(scores), 11, pg.Color('grey'))
    window.blit(text, (10, 10))
    # lives text
    text = font_score.render('Lives: ' + str(lives), 1, pg.Color('grey'))
    window.blit(text, (10, HEIGHT - 30))

    pg.display.update()
    clock.tick(FPS)

pg.quit()
