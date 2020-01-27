import pygame as pg
import random
from sprites import *
from settings import *
from os import path


class Game:
    def __init__(self):
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True
        self.font_name = pg.font.match_font(FONT_NAME)
        self.load_data()
        self.body = {}

    def load_data(self):
        self.dir = path.dirname(__file__)
        with open(path.join(self.dir, HS_FILE), 'r') as f:
            try:
                self.highscore = int(f.read())
            except:
                self.highscore = 0

    def new(self):
        self.score = 0
        self.all_sprites = pg.sprite.Group()
        self.Head = pg.sprite.Group()
        self.Body = pg.sprite.Group()
        self.Fruit = pg.sprite.Group()
        # Initiate sprites
        self.head = Head(self)
        self.apple = Point(self, random.randrange(5, WIDTH - 5), random.randrange(5, HEIGHT - 5))
        for part in range(self.head.length):
            b = Body(self, part)
            b.rect.centerx = self.head.rect.centerx
            b.rect.centery = self.head.rect.centery + (10 * part) + 10
            self.all_sprites.add(b)
            self.Body.add(b)
            self.body[part] = b
        # Add sprites into respective groups
        self.Fruit.add(self.apple)
        self.all_sprites.add(self.apple)
        self.all_sprites.add(self.head)
        self.Head.add(self.head)

        self.run()

    def run(self):
        # Game Loop
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def update(self):
        # Game Loop - update
        self.all_sprites.update()
        dead = pg.sprite.spritecollide(self.head, self.Body, False)
        if dead:
            self.playing = False

        p = pg.sprite.spritecollide(self.head, self.Fruit, True)
        if p:
            self.score += 1
            self.head.length += 1
            self.apple.kill()
            self.apple = Point(self, random.randrange(5, WIDTH - 5),
                               random.randrange(5, HEIGHT - 5))
            self.Fruit.add(self.apple)
            self.all_sprites.add(self.apple)

            b = Body(self, self.head.length - 1)
            prev = self.body[self.head.length -
                             2].moves[len(self.body[self.head.length - 2].moves) - 1]
            if prev == 'up':
                b.rect.centerx = self.body[self.head.length - 2].rect.centerx
                b.rect.centery = self.body[self.head.length - 2].rect.centery + 10
                b.moves.append('up')

            if prev == 'down':
                b.rect.centerx = self.body[self.head.length - 2].rect.centerx
                b.rect.centery = self.body[self.head.length - 2].rect.centery - 10
                b.moves.append('down')

            if prev == 'right':
                b.rect.centerx = self.body[self.head.length - 2].rect.centerx - 10
                b.rect.centery = self.body[self.head.length - 2].rect.centery
                b.moves.append('right')

            if prev == 'left':
                b.rect.centerx = self.body[self.head.length - 2].rect.centerx + 10
                b.rect.centery = self.body[self.head.length - 2].rect.centery
                b.moves.append('left')

            self.all_sprites.add(b)
            self.Body.add(b)
            self.body[self.head.length - 1] = b

    def events(self):
        # Game Loop - events
        for event in pg.event.get():
            # check for closing window
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False

    def draw(self):
        # Game Loop - draw
        self.screen.fill(BGCOLOR)
        self.all_sprites.draw(self.screen)
        self.draw_text(str(self.score), 30, YELLOW, WIDTH / 2, 15)
        # *after* drawing everything, flip the display
        pg.display.flip()

    def draw_text(self, text, size, color, x, y):
        font = pg.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)

    def show_start_screen(self):
        self.screen.fill(BGCOLOR)
        self.draw_text(TITLE, 48, RED, WIDTH / 2, HEIGHT / 4)
        self.draw_text("Use arrows to move, and collect points", 30, BLUE, WIDTH / 2, HEIGHT / 2)
        self.draw_text("Press a key to play", 30, RED, WIDTH / 2, HEIGHT * 3 / 4)
        self.draw_text("High Score: " + str(self.highscore), 30, BLUE, WIDTH / 2, 15)
        pg.display.flip()
        self.wait_for_key()

    def show_go_screen(self):
        # game over/continue
        if not self.running:
            return
        self.screen.fill(BGCOLOR)
        self.draw_text("GAME OVER", 48, BLUE, WIDTH / 2, HEIGHT / 4)
        self.draw_text("Score: " + str(self.score), 30, RED, WIDTH / 2, HEIGHT / 2)
        self.draw_text("Press a key to play again", 30, BLUE, WIDTH / 2, HEIGHT * 3 / 4)
        if self.score > self.highscore:
            self.highscore = self.score
            self.draw_text("NEW HIGH SCORE!", 30, YELLOW, WIDTH / 2, HEIGHT / 2 + 40)
            with open(path.join(self.dir, HS_FILE), 'w') as f:
                f.write(str(self.score))
        else:
            self.draw_text("High Score: " + str(self.highscore),
                           30, YELLOW, WIDTH / 2, HEIGHT / 2 + 40)
        pg.display.flip()
        self.wait_for_key()

    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pg.KEYUP:
                    waiting = False


g = Game()
g.show_start_screen()
while g.running:
    g.new()
    g.show_go_screen()

pg.quit()
