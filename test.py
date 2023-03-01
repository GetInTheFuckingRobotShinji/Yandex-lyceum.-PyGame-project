import pygame as pg
import sys

pg.init()
sc = pg.display.set_mode((400, 300))

sound1 = pg.mixer.Sound('data/mp.mp3')
sound2 = pg.mixer.Sound('data/vinni-pux-3654654.mp3')

while 1:
    for i in pg.event.get():
        if i.type == pg.QUIT:
            sys.exit()

        if i.type == pg.MOUSEBUTTONUP:
            if i.button == 1:
                sound1.play()
            elif i.button == 3:
                sound2.play()

    pg.time.delay(20)