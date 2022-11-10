# ---------------------------------------------------------------------------
# Laser Blast, Paint
#
# History
#  1 Nov 2022 Mike Christle     Created
# ---------------------------------------------------------------------------
# MIT Licence
# Copyright 2022 Mike Christle
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
# ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE
# USE OR OTHER DEALINGS IN THE SOFTWARE.
# ---------------------------------------------------------------------------

from Cell import Cell
from time import sleep
import GameState
import pygame


# To change the size of the display, set the SQUARE_SIZE constant.
# All other constants are calculated from this.
SQUARE_SIZE: int = 100
SQUARE_HALF = SQUARE_SIZE // 2
SCREEN_WIDTH = SQUARE_SIZE * 9
SCREEN_HEIGHT = SQUARE_SIZE * 8

PAD = SQUARE_SIZE // 10
PAD2 = PAD << 1
SCREEN_SIZE = SCREEN_WIDTH + PAD2, SCREEN_HEIGHT + PAD2
SCREEN_COOR = (0, 0, SCREEN_WIDTH + PAD2, SCREEN_HEIGHT + PAD2)

TAN_22 = 0.41421356237309503
MID = round((SQUARE_HALF - PAD) * TAN_22)
LINE_WIDTH = SQUARE_SIZE // 10
LASER_WIDTH = SQUARE_SIZE // 15

BLACK = '#000000'
GRAY = '#404040'
DARK_GRAY = '#202020'
SQUARE_COLORS = (GRAY, BLACK)
RED = '#FF0000'
GREEN = '#00DD00'
WHITE = '#FFFFFF'
BLUE = '#A0A0FF'

TEXT_X = (8 * SQUARE_SIZE) + SQUARE_HALF + PAD
TEXT_Y = (7 * SQUARE_SIZE) + SQUARE_HALF + PAD
TEXT_XY = TEXT_X, TEXT_Y
FONT_SIZE = SQUARE_SIZE // 2

BG_COOR = (((8 * SQUARE_SIZE) + PAD, PAD), (SQUARE_SIZE, 8 * SQUARE_SIZE))
BORDER0 = ((0, 0), (SCREEN_WIDTH + PAD, PAD))
BORDER1 = ((0, 0), (PAD, SCREEN_HEIGHT + PAD))
BORDER2 = ((0, SCREEN_HEIGHT + PAD), (SCREEN_WIDTH + PAD, PAD))
BORDER3 = ((SCREEN_WIDTH + PAD, 0), (PAD, SCREEN_HEIGHT + PAD2))


laser_color = False
laser_path = []
player_color = RED

pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE)
font = pygame.font.SysFont('Arial Bold', FONT_SIZE)
pygame.display.set_caption('Laser Blast      Press F1 to start a new game')


# ---------------------------------------------------------------------------
def get_grid_xy(x, y):
    """Convert from screen coordinates to grid coordinates"""

    x = (x - PAD) // SQUARE_SIZE
    y = (y - PAD) // SQUARE_SIZE
    if x < 0: x = 0
    if x > 8: x = 8
    if y < 0: y = 0
    if y > 7: y = 7
    return x, y


# ---------------------------------------------------------------------------
def paint_cursor():
    x = (GameState.cursor_x * SQUARE_SIZE) + PAD
    y = (GameState.cursor_y * SQUARE_SIZE) + PAD
    p0 = x + SQUARE_HALF, y
    p1 = x + SQUARE_HALF, y + SQUARE_SIZE
    pygame.draw.line(screen, WHITE, p0, p1)
    p0 = x, y + SQUARE_HALF
    p1 = x + SQUARE_SIZE, y + SQUARE_HALF
    pygame.draw.line(screen, WHITE, p0, p1)


# ---------------------------------------------------------------------------
def mirror_000(x0, y0, color):
    p0 = x0 + PAD, y0 + SQUARE_HALF
    p1 = x0 + SQUARE_SIZE - PAD, y0 + SQUARE_HALF
    pygame.draw.line(screen, color, p0, p1, width = LINE_WIDTH)


# ---------------------------------------------------------------------------
def mirror_022(x0, y0, color):
    p0 = x0 + PAD, y0 + SQUARE_HALF + MID
    p1 = x0 + SQUARE_SIZE - PAD, y0 + SQUARE_HALF - MID
    pygame.draw.line(screen, color, p0, p1, width = LINE_WIDTH)


# ---------------------------------------------------------------------------
def mirror_045(x0, y0, color):
    p0 = x0 + PAD, y0 + SQUARE_SIZE - PAD
    p1 = x0 + SQUARE_SIZE - PAD, y0 + PAD
    pygame.draw.line(screen, color, p0, p1, width = LINE_WIDTH)


# ---------------------------------------------------------------------------
def mirror_068(x0, y0, color):
    p0 = x0 + SQUARE_HALF + MID, y0 + PAD
    p1 = x0 + SQUARE_HALF - MID, y0 + SQUARE_SIZE - PAD
    pygame.draw.line(screen, color, p0, p1, width = LINE_WIDTH)


# ---------------------------------------------------------------------------
def mirror_090(x0, y0, color):
    p0 = x0 + SQUARE_HALF, y0 + PAD
    p1 = x0 + SQUARE_HALF, y0 + SQUARE_SIZE - PAD
    pygame.draw.line(screen, color, p0, p1, width = LINE_WIDTH)


# ---------------------------------------------------------------------------
def mirror_112(x0, y0, color):
    p0 = x0 + SQUARE_HALF - MID, y0 + PAD
    p1 = x0 + SQUARE_HALF + MID, y0 + SQUARE_SIZE - PAD
    pygame.draw.line(screen, color, p0, p1, width = LINE_WIDTH)


# ---------------------------------------------------------------------------
def mirror_135(x0, y0, color):
    p0 = x0 + PAD, y0 + PAD
    p1 = x0 + SQUARE_SIZE - PAD, y0 + SQUARE_SIZE - PAD
    pygame.draw.line(screen, color, p0, p1, width = LINE_WIDTH)


# ---------------------------------------------------------------------------
def mirror_158(x0, y0, color):
    p0 = x0 + PAD, y0 + SQUARE_HALF - MID
    p1 = x0 + SQUARE_SIZE - PAD, y0 + SQUARE_HALF + MID
    pygame.draw.line(screen, color, p0, p1, width = LINE_WIDTH)


# ---------------------------------------------------------------------------
def laser_up(x0, y0, color):
    x1 = x0 + SQUARE_HALF
    y1 = y0
    x2 = x0 + PAD
    y2 = y0 + SQUARE_SIZE - PAD
    x3 = x0 + SQUARE_SIZE - PAD
    y3 = y2
    points = ((x1, y1), (x2, y2), (x3, y3))
    pygame.draw.polygon(screen, color, points)


# ---------------------------------------------------------------------------
def laser_rt(x0, y0, color):
    x1 = x0 + SQUARE_SIZE
    y1 = y0 + SQUARE_HALF
    x2 = x0 + PAD
    y2 = y0 + PAD
    x3 = x0 + PAD
    y3 = y0 + SQUARE_SIZE - PAD
    points = ((x1, y1), (x2, y2), (x3, y3))
    pygame.draw.polygon(screen, color, points)


# ---------------------------------------------------------------------------
def laser_dn(x0, y0, color):
    x1 = x0 + SQUARE_HALF
    y1 = y0 + SQUARE_SIZE
    x2 = x0 + PAD
    y2 = y0 + PAD
    x3 = x0 + SQUARE_SIZE - PAD
    y3 = y2
    points = ((x1, y1), (x2, y2), (x3, y3))
    pygame.draw.polygon(screen, color, points)


# ---------------------------------------------------------------------------
def laser_lf(x0, y0, color):
    x1 = x0
    y1 = y0 + SQUARE_HALF
    x2 = x0 + SQUARE_SIZE - PAD
    y2 = y0 + PAD
    x3 = x2
    y3 = y0 + SQUARE_SIZE - PAD
    points = ((x1, y1), (x2, y2), (x3, y3))
    pygame.draw.polygon(screen, color, points)


# -----------------------------------------------------------------------
mirror_funcs = (mirror_000, mirror_022, mirror_045, mirror_068,
                mirror_090, mirror_112, mirror_135, mirror_158)
laser_funcs = (laser_up, None, laser_rt, None,
               laser_dn, None, laser_lf, None)


# -----------------------------------------------------------------------
def fire_laser():
    """
    Animate the firing of a laser.
    The laser path comes from the GameState.laser_path list
    in grid coordinates.
    """

    global laser_color

    for x, y in GameState.laser_path:
        x = x * SQUARE_SIZE + SQUARE_HALF + PAD
        y = y * SQUARE_SIZE + SQUARE_HALF + PAD
        laser_path.append((x, y))

    for c in range(20):
        paint()
        laser_color = not laser_color
        sleep(0.1)

    laser_path.clear()
    GameState.laser_path.clear()


# -----------------------------------------------------------------------
def paint():
    """Repaint the screen display."""

    selected_cell = None

    # Paint checker board
    color_idx = 0
    for y in range(8):
        color_idx ^= 1
        y0 = (y * SQUARE_SIZE) + PAD
        for x in range(8):
            color_idx ^= 1
            x0 = (x * SQUARE_SIZE) + PAD
            color = SQUARE_COLORS[color_idx]
            rect = pygame.Rect((x0, y0), (SQUARE_SIZE, SQUARE_SIZE))
            pygame.draw.rect(screen, color, rect)

    # Paint laser path
    if len(laser_path) > 0:
        color = WHITE if laser_color else BLUE
        pygame.draw.lines(screen, color, False, laser_path, width = LASER_WIDTH)

    # Paint mirrors and lasers
    for y in range(8):
        y0 = (y * SQUARE_SIZE) + PAD
        for x in range(8):
            x0 = (x * SQUARE_SIZE) + PAD
            cell = GameState.grid[y][x]
            if cell.actor == Cell.EMPTY:
                continue

            if cell.selected:
                color = WHITE
                selected_cell = cell
            elif cell.team == Cell.RED_TEAM:
                color = RED
            else: # Green Team
                color = GREEN

            if cell.actor == Cell.MIRROR:
                func = mirror_funcs[cell.angle]
            else: # Laser
                func = laser_funcs[cell.angle]
            func(x0, y0, color)

    # Paint action buttons on action panel
    pygame.draw.rect(screen, DARK_GRAY, BG_COOR)

    # Paint the action buttons
    if selected_cell is not None:
        if selected_cell.team == Cell.RED_TEAM:
            color = RED
        else: # Green Team
            color = GREEN

        x = (8 * SQUARE_SIZE) + PAD
        if selected_cell.actor == Cell.MIRROR:
            for y in range(8):
                func = mirror_funcs[y]
                func(x, (y * SQUARE_SIZE + PAD), color)
        else: # Laser
            for y in range(4):
                func = laser_funcs[y << 1]
                func(x, (y * SQUARE_SIZE) + PAD, color)
            text = font.render('FIRE', True, color)
            textRect = text.get_rect()
            textRect.center = (TEXT_X, TEXT_Y)
            screen.blit(text, textRect)

    # Paint the border
    color = RED if GameState.player == Cell.RED_TEAM else GREEN
    pygame.draw.rect(screen, color, BORDER0)
    pygame.draw.rect(screen, color, BORDER1)
    pygame.draw.rect(screen, color, BORDER2)
    pygame.draw.rect(screen, color, BORDER3)

    paint_cursor()
    pygame.display.flip()
