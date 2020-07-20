import pygame as pg
from pygame.locals import *


def init_pygame():
    pg.init()
    pg.font.init()

    pg.mouse.set_visible(0)
    pg.display.set_caption('Racing')

    return pg.display.set_mode((1920, 1080), FULLSCREEN)


def quit_pygame():
    pg.quit()