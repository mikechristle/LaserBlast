# ---------------------------------------------------------------------------
# Laser Blast, Game Logic
#
# History
#  1 Nov 2022 Mike Christle     Created
# 14 Nov 2022 Mike Christle     Add mirrors to the borders
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

import GameState

from Paint import fire_laser
from Cell import Cell


select_x = 0        # Coordinates of selected piece
select_y = 0
hit_x = -1          # Coordinates of piece hit by a laser beam
hit_y = -1
move_count = 0      # Count of moves for each payers turn


# ---------------------------------------------------------------------------
def init_game():
    """Initialize the board and game state for a new game."""

    global move_count

    # Clear all cells in the grid
    for line in GameState.grid:
        for cell in line:
            cell.clear()

    # Initial layout of red players mirrors and lasers
    GameState.grid[2][0].set(Cell.RED_TEAM, Cell.LASER, Cell.RIGHT)
    GameState.grid[5][0].set(Cell.RED_TEAM, Cell.LASER, Cell.RIGHT)
    GameState.grid[0][1].set(Cell.RED_TEAM, Cell.MIRROR, 6)
    GameState.grid[1][2].set(Cell.RED_TEAM, Cell.MIRROR, 6)
    GameState.grid[2][2].set(Cell.RED_TEAM, Cell.MIRROR, 2)
    GameState.grid[3][1].set(Cell.RED_TEAM, Cell.MIRROR, 2)
    GameState.grid[4][1].set(Cell.RED_TEAM, Cell.MIRROR, 6)
    GameState.grid[5][2].set(Cell.RED_TEAM, Cell.MIRROR, 6)
    GameState.grid[6][2].set(Cell.RED_TEAM, Cell.MIRROR, 2)
    GameState.grid[7][1].set(Cell.RED_TEAM, Cell.MIRROR, 2)

    # Initial layout of green players mirrors and lasers
    GameState.grid[2][7].set(Cell.GRN_TEAM, Cell.LASER, Cell.LEFT)
    GameState.grid[5][7].set(Cell.GRN_TEAM, Cell.LASER, Cell.LEFT)
    GameState.grid[0][6].set(Cell.GRN_TEAM, Cell.MIRROR, 2)
    GameState.grid[1][5].set(Cell.GRN_TEAM, Cell.MIRROR, 2)
    GameState.grid[2][5].set(Cell.GRN_TEAM, Cell.MIRROR, 6)
    GameState.grid[3][6].set(Cell.GRN_TEAM, Cell.MIRROR, 6)
    GameState.grid[4][6].set(Cell.GRN_TEAM, Cell.MIRROR, 2)
    GameState.grid[5][5].set(Cell.GRN_TEAM, Cell.MIRROR, 2)
    GameState.grid[6][5].set(Cell.GRN_TEAM, Cell.MIRROR, 6)
    GameState.grid[7][6].set(Cell.GRN_TEAM, Cell.MIRROR, 6)

    # The loser of last game gets first move
    if GameState.grn_laser_count == 0:
        GameState.player = Cell.RED_TEAM
    else:
        GameState.player = Cell.GRN_TEAM
    GameState.player = Cell.RED_TEAM

    # Reset counts
    move_count = 2
    GameState.red_laser_count = 2
    GameState.grn_laser_count = 2
    GameState.state = GameState.WAIT

    # Reset the cursor
    GameState.cursor_x = 0
    GameState.cursor_y = 0


# ---------------------------------------------------------------------------
def find_laser_path():
    """
    Trace the path of a laser beam starting with the selected laser.
    Set hit x and y if something is destroyed.
    """

    global hit_x, hit_y, select_x, select_y

    hit_x = hit_y = -1
    x = select_x
    y = select_y
    direction = GameState.grid[y][x].angle

             # 000 022 045 068 090 112 135 158
    new_dir = ((9,  3,  2,  1,  8,  7,  6,  5), # 0 N       8 = Hit mirror edge
               (3,  2,  8,  0,  7,  6,  9,  4), # 1 NE      9 = Hit laser
               (8,  1,  0,  7,  9,  5,  4,  3), # 2 E
               (1,  0,  9,  6,  5,  4,  8,  2), # 3 SE
               (9,  7,  6,  5,  8,  3,  2,  1), # 4 S
               (7,  6,  8,  4,  3,  2,  9,  0), # 5 SW
               (8,  5,  4,  3,  9,  1,  0,  7), # 6 W
               (5,  4,  9,  2,  1,  0,  8,  6)) # 7 NW

    while True:

        # Save current coordinates
        GameState.laser_path.append((x, y))

        # Get the current cell
        cell = GameState.grid[y][x]

        # If current cell is a mirror, get new direction of travel
        if cell.actor == Cell.MIRROR:
            direction = new_dir[direction][cell.angle]

        # Advance to next cell
        match direction:
            case GameState.N:
                y -= 1
            case GameState.NE:
                x += 1
                y -= 1
            case GameState.E:
                x += 1
            case GameState.SE:
                x += 1
                y += 1
            case GameState.S:
                y += 1
            case GameState.SW:
                y += 1
                x -= 1
            case GameState.W:
                x -= 1
            case GameState.NW:
                x -= 1
                y -= 1
            case 8: # Hit edge of a mirror
                hit_x = x
                hit_y = y
                return
            case 9: # Hit face of a mirror
                hit_mirror_face(x, y)
                return

        # If laser hits a border mirror
        match [direction, y, x]:
            case [GameState.NW, -1, -1]: # Top left corner
                hit_mirror_face(x, y)
                return
            case [GameState.NW, -1, _]: # Top side
                GameState.laser_path.append((x, y))
                GameState.laser_path.append((x + 1, y))
                y += 1
                direction = GameState.SW
            case [GameState.NW, _, -1]: # Left side
                GameState.laser_path.append((x, y))
                GameState.laser_path.append((x, y + 1))
                x += 1
                direction = GameState.NE

            case [GameState.NE, -1, GameState.square_count]: # Top right corner
                hit_mirror_face(x, y)
                return
            case [GameState.NE, -1, _]: # Top side
                GameState.laser_path.append((x, y))
                GameState.laser_path.append((x - 1, y))
                y += 1
                direction = GameState.SE
            case [GameState.NE, _, GameState.square_count]: # Right side
                GameState.laser_path.append((x, y))
                GameState.laser_path.append((x, y + 1))
                x -= 1
                direction = GameState.NW

            case [GameState.SW, GameState.square_count, -1]: # Bottom left corner
                hit_mirror_face(x, y)
                return
            case [GameState.SW, GameState.square_count, _]: # Bottom side
                GameState.laser_path.append((x, y))
                GameState.laser_path.append((x + 1, y))
                y -= 1
                direction = GameState.NW
            case [GameState.SW, _, -1]: # Left side
                GameState.laser_path.append((x, y))
                GameState.laser_path.append((x, y - 1))
                x += 1
                direction = GameState.SE

            case [GameState.SE, GameState.square_count, GameState.square_count]: # Bottom right corner
                hit_mirror_face(x, y)
                return
            case [GameState.SE, GameState.square_count, _]: # Bottom side
                GameState.laser_path.append((x, y))
                GameState.laser_path.append((x - 1, y))
                y -= 1
                direction = GameState.NE
            case [GameState.SE, _, GameState.square_count]: # Right side
                GameState.laser_path.append((x, y))
                GameState.laser_path.append((x, y - 1))
                x -= 1
                direction = GameState.SW

            case [GameState.N, -1, _]: # Top side
                hit_mirror_face(x, y)
                return
            case [GameState.S, GameState.square_count, _]: # Bottom side
                hit_mirror_face(x, y)
                return
            case [GameState.W, _, -1]: # Left side
                hit_mirror_face(x, y)
                return
            case [GameState.E, _, GameState.square_count]: # Right side
                hit_mirror_face(x, y)
                return

            # If laser beam hits a laser gun
        cell = GameState.grid[y][x]
        if cell.actor == Cell.LASER:
            select_x = x
            select_y = y
            hit_mirror_face(x, y)
            return


# ---------------------------------------------------------------------------
def hit_mirror_face(x, y):
    global hit_x, hit_y

    GameState.laser_path.append((x, y))
    hit_x = select_x
    hit_y = select_y
    if GameState.grid[select_y][select_x].team == Cell.RED_TEAM:
        GameState.red_laser_count -= 1
    else:
        GameState.grn_laser_count -= 1


# ---------------------------------------------------------------------------
def click():
    """Process player actions."""

    # If in wait state
    if GameState.state == GameState.WAIT:
        click_wait()

    # If in action state and clicked on board
    elif GameState.cursor_x < 8:
        click_move()

    # If in action state and clicked on right most column
    else:
        click_action()


# ---------------------------------------------------------------------------
def click_wait():
    """Process selection of a game piece."""

    global select_x, select_y

    if GameState.cursor_x < 8:
        cell = GameState.grid[GameState.cursor_y][GameState.cursor_x]
        if cell.team == GameState.player:
            cell.selected = True
            select_x = GameState.cursor_x
            select_y = GameState.cursor_y
            GameState.state = GameState.ACTION


# ---------------------------------------------------------------------------
def click_action():
    """Process the rotation of a game piece, or firing the laser."""

    global move_count

    selected = GameState.grid[select_y][select_x]

    # If a mirror was selected
    # And new angle is not the same current angle
    if selected.actor == Cell.MIRROR and selected.angle != GameState.cursor_y:
        # Change the angle of selected cell
        selected.angle = GameState.cursor_y
        selected.selected = False
        move_count -= 1
        action_taken()

    # IF laser selected
    # And fire laser button pressed
    elif GameState.cursor_y == 7:
        selected.selected = False
        find_laser_path()
        fire_laser()

        # If something was hit, remove it from board
        if hit_x != -1:
            GameState.grid[hit_y][hit_x].clear()

        move_count -= 1
        action_taken()

    # IF laser selected
    # Rotate the laser
    elif GameState.cursor_y < 4:
        y = GameState.cursor_y << 1
        # And new angle is not the same current angle
        if selected.angle != y:
            selected.angle = y
            selected.selected = False
            move_count -= 1
            action_taken()


# ---------------------------------------------------------------------------
def click_move():
    """Process the moving of a game piece."""

    global move_count

    selected = GameState.grid[select_y][select_x]
    cell = GameState.grid[GameState.cursor_y][GameState.cursor_x]

    # Move a red or green piece
    dx = abs(select_x - GameState.cursor_x)
    dy = abs(select_y - GameState.cursor_y)

    # If click on selected piece, deselect the piece
    if dx == 0 and dy == 0:
        selected.selected = False
        action_taken()

    # If click on empty cell
    elif cell.actor == Cell.EMPTY:
        # Move one space
        if dx < 2 and dy < 2:
            move_count -= 1
            selected.move_to(cell)
            action_taken()
        # Move two spaces
        elif move_count == 2 and dx < 3 and dy < 3:
            move_count -= 2
            selected.move_to(cell)
            action_taken()


# ---------------------------------------------------------------------------
def action_taken():
    """Update the game state if an action is taken."""

    global move_count

    GameState.state = GameState.WAIT
    match [move_count, GameState.player]:
        case [0, Cell.RED_TEAM]:
            move_count = 2
            GameState.player = Cell.GRN_TEAM
        case [0, Cell.GRN_TEAM]:
            move_count = 2
            GameState.player = Cell.RED_TEAM

    if GameState.red_laser_count == 0 or GameState.grn_laser_count == 0:
        GameState.state = GameState.END
