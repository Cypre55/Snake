import pygame as pg
from settings import *


class Head(pg.sprite.Sprite):
    def __init__(self, game):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.length = 10
        self.image = pg.Surface((10, 10))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.moves = ['up']
        self.curr_pos = self.rect.center

    def update(self):
        if self.rect.bottom < 0:
            self.rect.top = HEIGHT
        if self.rect.top > HEIGHT:
            self.rect.bottom = 0
        if self.rect.left > WIDTH:
            self.rect.right = 0
        if self.rect.right < 0:
            self.rect.left = WIDTH

        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            if self.moves[len(self.moves) - 1] != 'right':
                self.moves.append('left')

        if keys[pg.K_RIGHT]:
            if self.moves[len(self.moves) - 1] != 'left':
                self.moves.append('right')

        if keys[pg.K_UP]:
            if self.moves[len(self.moves) - 1] != 'down':
                self.moves.append('up')

        if keys[pg.K_DOWN]:
            if self.moves[len(self.moves) - 1] != 'up':
                self.moves.append('down')

        if self.moves[len(self.moves) - 1] == 'up':
            self.rect.centery += -10
        if self.moves[len(self.moves) - 1] == 'right':
            self.rect.centerx += 10
        if self.moves[len(self.moves) - 1] == 'down':
            self.rect.centery += 10
        if self.moves[len(self.moves) - 1] == 'left':
            self.rect.centerx += -10

        self.curr_pos = self.rect.center


class Body(pg.sprite.Sprite):
    def __init__(self, game, index):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.index = index
        self.image = pg.Surface((10, 10))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.moves = ["up"]

    def Follow(self):
        if self.index == 0:
            self.moves.append(self.game.head.moves[len(self.game.head.moves) - 1])
        else:
            self.moves.append(
                self.game.body[self.index - 1].moves[len(self.game.body[self.index - 1].moves) - 2])

        if self.moves[len(self.moves) - 1] == 'up':
            self.rect.centery += -10
        if self.moves[len(self.moves) - 1] == 'right':
            self.rect.centerx += 10
        if self.moves[len(self.moves) - 1] == 'down':
            self.rect.centery += 10
        if self.moves[len(self.moves) - 1] == 'left':
            self.rect.centerx += -10

    def update(self):
        if self.rect.bottom < 0:
            self.rect.top = HEIGHT
        if self.rect.top > HEIGHT:
            self.rect.bottom = 0
        if self.rect.left > WIDTH:
            self.rect.right = 0
        if self.rect.right < 0:
            self.rect.left = WIDTH
        self.Follow()
        self.curr_pos = self.rect.center


class Point(pg.sprite.Sprite):
    def __init__(self, game, posx, posy):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.image = pg.Surface((10, 10))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.posx = posx
        self.posy = posy
        self.rect.center = (posx, posy)

    def update(self):
        pass
