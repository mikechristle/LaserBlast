# ---------------------------------------------------------------------------
# Laser Blast, Paint
#
# History
#  1 Nov 2022 Mike Christle     Created
# 15 Nov 2022 Mike Christle     Switch to 9x9 square grid
#                               Allow laser cannons to fire diagonally
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
from math import sqrt
import GameState
import pygame


# To change the size of the display, set the SQUARE_SIZE constant.
# All other constants are calculated from this.
SQUARE_SIZE = 100
SQUARE_HALF = SQUARE_SIZE // 2
SCREEN_WIDTH = SQUARE_SIZE * 10
SCREEN_HEIGHT = SQUARE_SIZE * 9

PAD = SQUARE_SIZE // 10
PAD2 = PAD << 1
SCREEN_SIZE = SCREEN_WIDTH + PAD2, SCREEN_HEIGHT + PAD2
SCREEN_COOR = (0, 0, SCREEN_WIDTH + PAD2, SCREEN_HEIGHT + PAD2)

TAN_22 = 0.41421356237309503
MID = round((SQUARE_HALF - PAD) * TAN_22)
LINE_WIDTH = SQUARE_SIZE // 10
LASER_WIDTH = SQUARE_SIZE // 15
LASER_CIRCLE_RADIUS = SQUARE_SIZE >> 2
LASER_P1 = int(sqrt(0.5 * SQUARE_HALF * SQUARE_HALF))
LASER_P23 = int(sqrt(0.5 * (SQUARE_HALF >> 1) ** 2))

BLACK = '#000000'
GRAY = '#404040'
DARK_GRAY = '#202020'
SQUARE_COLORS = (GRAY, BLACK)
RED = '#FF0000'
GREEN = '#00DD00'
WHITE = '#FFFFFF'
BLUE = '#A0A0FF'

TEXT_X = (9 * SQUARE_SIZE) + SQUARE_HALF + PAD
TEXT_Y = (8 * SQUARE_SIZE) + SQUARE_HALF + PAD
TEXT_XY = TEXT_X, TEXT_Y
FONT_SIZE = SQUARE_SIZE // 2

BG_COOR = (((9 * SQUARE_SIZE) + PAD, PAD), (SQUARE_SIZE, 9 * SQUARE_SIZE))
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
pygame.display.set_caption('Laser Blast   V2.1   Press F1 to start a new game')


# ---------------------------------------------------------------------------
def laser_path_append(x, y):
    x = (x * SQUARE_SIZE) + SQUARE_HALF + PAD
    y = (y * SQUARE_SIZE) + SQUARE_HALF + PAD
    laser_path.append((x, y))


# ---------------------------------------------------------------------------
def get_grid_xy(x, y):
    """Convert from screen coordinates to grid coordinates"""

    x = (x - PAD) // SQUARE_SIZE
    y = (y - PAD) // SQUARE_SIZE
    if x < 0: x = 0
    if x > 9: x = 9
    if y < 0: y = 0
    if y > 8: y = 8
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
def paint_mirror(x, y, color, angle):
    """Paint a mirror."""

    x = (x * SQUARE_SIZE) + PAD
    y = (y * SQUARE_SIZE) + PAD

    match angle:
        case 0:
            p0 = x + PAD, y + SQUARE_HALF
            p1 = x + SQUARE_SIZE - PAD, y + SQUARE_HALF
        case 1:
            p0 = x + PAD, y + SQUARE_HALF + MID
            p1 = x + SQUARE_SIZE - PAD, y + SQUARE_HALF - MID
        case 2:
            p0 = x + PAD, y + SQUARE_SIZE - PAD
            p1 = x + SQUARE_SIZE - PAD, y + PAD
        case 3:
            p0 = x + SQUARE_HALF + MID, y + PAD
            p1 = x + SQUARE_HALF - MID, y + SQUARE_SIZE - PAD
        case 4:
            p0 = x + SQUARE_HALF, y + PAD
            p1 = x + SQUARE_HALF, y + SQUARE_SIZE - PAD
        case 5:
            p0 = x + SQUARE_HALF - MID, y + PAD
            p1 = x + SQUARE_HALF + MID, y + SQUARE_SIZE - PAD
        case 6:
            p0 = x + PAD, y + PAD
            p1 = x + SQUARE_SIZE - PAD, y + SQUARE_SIZE - PAD
        case _:
            p0 = x + PAD, y + SQUARE_HALF - MID
            p1 = x + SQUARE_SIZE - PAD, y + SQUARE_HALF + MID

    pygame.draw.line(screen, color, p0, p1, width = LINE_WIDTH)


# ---------------------------------------------------------------------------
def paint_laser(x, y, color, angle):
    """Paint a laser cannon."""

    x = (x * SQUARE_SIZE) + PAD + SQUARE_HALF
    y = (y * SQUARE_SIZE) + PAD + SQUARE_HALF

    match angle:
        case 0:
            p1 = (x, y - SQUARE_HALF)
            p2 = (x - LASER_CIRCLE_RADIUS, y)
            p3 = (x + LASER_CIRCLE_RADIUS, y)
        case 1:
            p1 = (x + LASER_P1, y - LASER_P1)
            p2 = (x - LASER_P23, y - LASER_P23)
            p3 = (x + LASER_P23, y + LASER_P23)
        case 2:
            p1 = (x + SQUARE_HALF, y)
            p2 = (x, y - LASER_CIRCLE_RADIUS)
            p3 = (x, y + LASER_CIRCLE_RADIUS)
        case 3:
            p1 = (x + LASER_P1, y + LASER_P1)
            p2 = (x + LASER_P23, y - LASER_P23)
            p3 = (x - LASER_P23, y + LASER_P23)
        case 4:
            p1 = (x, y + SQUARE_HALF)
            p2 = (x - LASER_CIRCLE_RADIUS, y)
            p3 = (x + LASER_CIRCLE_RADIUS, y)
        case 5:
            p1 = (x - LASER_P1, y + LASER_P1)
            p2 = (x + LASER_P23, y + LASER_P23)
            p3 = (x - LASER_P23, y - LASER_P23)
        case 6:
            p1 = (x - SQUARE_HALF, y)
            p2 = (x, y - LASER_CIRCLE_RADIUS)
            p3 = (x, y + LASER_CIRCLE_RADIUS)
        case _:
            p1 = (x - LASER_P1, y - LASER_P1)
            p2 = (x + LASER_P23, y - LASER_P23)
            p3 = (x - LASER_P23, y + LASER_P23)

    pygame.draw.polygon(screen, color, (p1, p2, p3))
    pygame.draw.line(screen, BLACK, (x, y), p1, width = 3)
    pygame.draw.circle(screen, color, (x, y), LASER_CIRCLE_RADIUS)


# -----------------------------------------------------------------------
def fire_laser():
    """
    Animate the firing of a laser.
    The laser path comes from the GameState.laser_path list
    in grid coordinates.
    """

    global laser_color

    for _ in range(20):
        paint()
        laser_color = not laser_color
        sleep(0.1)

    laser_path.clear()


# -----------------------------------------------------------------------
def paint():
    """Repaint the screen display."""

    selected_cell = None

    # Paint checker board
    for y in range(9):
        y0 = (y * SQUARE_SIZE) + PAD
        for x in range(9):
            x0 = (x * SQUARE_SIZE) + PAD
            color_idx = (x + y) & 1
            color = SQUARE_COLORS[color_idx]
            rect = pygame.Rect((x0, y0), (SQUARE_SIZE, SQUARE_SIZE))
            pygame.draw.rect(screen, color, rect)

    # Paint laser path
    if len(laser_path) > 0:
        color = WHITE if laser_color else BLUE
        pygame.draw.lines(screen, color, False, laser_path, width = LASER_WIDTH)

    # Paint mirrors and lasers
    for y in range(9):
        for x in range(9):
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
                paint_mirror(x, y, color, cell.angle)
            else: # Laser
                paint_laser(x, y, color, cell.angle)

    # Paint action buttons on action panel
    pygame.draw.rect(screen, DARK_GRAY, BG_COOR)

    # Paint the action buttons
    if selected_cell is not None:
        if selected_cell.team == Cell.RED_TEAM:
            color = RED
        else: # Green Team
            color = GREEN

        if selected_cell.actor == Cell.MIRROR:
            for y in range(8):
                paint_mirror(9, y, color, y)
        else: # Laser
            for y in range(8):
                paint_laser(9, y, color, y)
            text = font.render('FIRE', True, color)
            rect = text.get_rect()
            rect.center = (TEXT_X, TEXT_Y)
            screen.blit(text, rect)

    # Paint the border
    color = RED if GameState.player == Cell.RED_TEAM else GREEN
    pygame.draw.rect(screen, color, BORDER0)
    pygame.draw.rect(screen, color, BORDER1)
    pygame.draw.rect(screen, color, BORDER2)
    pygame.draw.rect(screen, color, BORDER3)

    paint_cursor()
    pygame.display.flip()
