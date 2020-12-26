import numpy as np
import noise
import random
import pygame as pg


class Board:
    def __init__(self, width=3, height=3, left=0, top=0, cell_size=30):
        self.width = width
        self.height = height
        self.board = np.zeros((height, width), dtype=np.uint8)
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def set_view(self, left, top, cell_size=None):
        self.left = left
        self.top = top
        if not None:
            self.cell_size = cell_size

    def render(self, screen):
        pass

    def get_cell(self, mouse_pos):
        pos_x, pos_y = (mouse_pos[0] - self.left) // self.cell_size, \
                       (mouse_pos[1] - self.top) // self.cell_size
        if self.width > pos_x > -1 and self.height > pos_y > -1:
            return pos_x, pos_y
        return None

    def on_click(self, cell_coords):
        if cell_coords is not None:
            x, y = cell_coords
            self.board[y][x] = 1

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        self.on_click(cell)

    def generate_world(self):
        base = random.randint(0, 100000000)
        for i in range(self.height):
            for j in range(self.width):
                noise_val = noise.pnoise2(j / self.width, i / self.height, 6, 0.5, 2, base)
                if noise_val < -0.05:
                    self.board[i][j] = 0
                elif noise_val < 0:
                    self.board[i][j] = 1
                else:
                    self.board[i][j] = 2


if __name__ == '__main__':
    SIZE = pg.FULLSCREEN
    screen = pg.display.set_mode((0, 0), SIZE)
    WiDTH, HEIGHT = screen.get_width(), screen.get_height()
    # fps and clock
    clock = pg.time.Clock()
    fps = 60
    # create Board
    board = Board()
    # cursor
    sprite = pg.sprite.Sprite()
    sprite.image = pg.image.load('images/arrow.png')
    pg.mouse.set_visible(False)
    # run
    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            if event.type == pg.MOUSEMOTION:
                screen.fill(pg.Color('black'))
                if event.pos[0] != 0 and event.pos[-1] != 0:
                    screen.blit(sprite.image, event.pos)
        clock.tick(fps)
        pg.display.flip()
    pg.quit()
