# ---------------------------------------------------------------------------
# Laser Blast
#
# History
#  1 Nov 2022 Mike Christle     Created
# 14 Nov 2022 Mike Christle     Add mirrors to the borders
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

import sys, pygame
import GameState

from Cell import Cell
from Paint import paint, get_grid_xy
from GameLogic import init_game, click

init_game()
pygame.joystick.init()
joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
paint()

while True:

    # Get all pygame events
    for event in pygame.event.get():
        match [event.type, GameState.player]:

            # Exit if window is closed
            case [pygame.QUIT, _]:
                sys.exit()

            # If F1 is pressed, start new game
            case [pygame.KEYDOWN, _] if event.key == pygame.K_F1:
                init_game()
                paint()

            # If green player, handle keyboard events
            case [pygame.KEYDOWN, Cell.GRN_TEAM]:
                match event.key:
                    case pygame.K_UP if GameState.cursor_y > 0:
                        GameState.cursor_y -= 1
                    case pygame.K_RIGHT if GameState.cursor_x < 9:
                        GameState.cursor_x += 1
                    case pygame.K_LEFT if GameState.cursor_x > 0:
                        GameState.cursor_x -= 1
                    case pygame.K_DOWN if GameState.cursor_y < 8:
                        GameState.cursor_y += 1
                    case pygame.K_RETURN | pygame.K_SPACE:
                        click()
                paint()

            # If red player, handle controller 1 button events
            case [pygame.JOYBUTTONDOWN, Cell.RED_TEAM]:
                if event.joy == 1 and event.button < 4:
                    click()
                    paint()

            # If green player, handle controller 0 button events
            case [pygame.JOYBUTTONDOWN, Cell.GRN_TEAM]:
                if event.joy == 0 and event.button < 4:
                    click()
                    paint()

            # If red player, handle controller 1 axis events
            case [pygame.JOYAXISMOTION, Cell.RED_TEAM]:
                match [event.joy, event.axis, int(event.value)]:
                    case [1, 4, -1] if GameState.cursor_y > 0:
                        GameState.cursor_y -= 1
                    case [1, 4, 1] if GameState.cursor_y < 8:
                        GameState.cursor_y += 1
                    case [1, 0, -1] if GameState.cursor_x > 0:
                        GameState.cursor_x -= 1
                    case [1, 0, 1] if GameState.cursor_x < 9:
                        GameState.cursor_x += 1
                paint()

            # If green player, handle controller 0 axis events
            case [pygame.JOYAXISMOTION, Cell.GRN_TEAM]:
                match [event.joy, event.axis, int(event.value)]:
                    case [0, 4, -1] if GameState.cursor_y > 0:
                        GameState.cursor_y -= 1
                    case [0, 4, 1] if GameState.cursor_y < 8:
                        GameState.cursor_y += 1
                    case [0, 0, -1] if GameState.cursor_x > 0:
                        GameState.cursor_x -= 1
                    case [0, 0, 1] if GameState.cursor_x < 9:
                        GameState.cursor_x += 1
                paint()

            # If red player, handle motion events
            case [pygame.MOUSEMOTION, Cell.RED_TEAM]:
                x, y = pygame.mouse.get_pos()
                x, y = get_grid_xy(x, y)
                if x != GameState.cursor_x or y != GameState.cursor_y:
                    GameState.cursor_x = x
                    GameState.cursor_y = y
                    paint()

            # If red player, handle mouse button events
            case [pygame.MOUSEBUTTONUP, Cell.RED_TEAM] if event.button == 1:
                click()
                paint()
