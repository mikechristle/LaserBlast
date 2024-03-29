# ---------------------------------------------------------------------------
# Laser Blast, Game Logic
#
# History
#  1 Nov 2022 Mike Christle     Created
# 14 Nov 2022 Mike Christle     Add mirrors to the borders
# 15 Nov 2022 Mike Christle     Switch to 9x9 square grid
#                               Allow laser cannons to fire diagonally
# 16 Jun 2023 Mike Christle     Clear board before new game
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

from Paint import fire_laser, laser_path_append
from Cell import Cell


# Initial location of mirrors
INIT_MIRRORS = ((1, 0, 6), (2, 1, 4), (1, 2, 2),
                (1, 3, 6), (2, 4, 4), (1, 5, 2),
                (1, 6, 6), (2, 7, 4), (1, 8, 2))

# New direction of beam after hitting a mirror
#          000 022 045 068 090 112 135 158
NEW_DIR = ((9,  3,  2,  1,  8,  7,  6,  5),  # 0 N       8 = Hit mirror edge
           (3,  2,  8,  0,  7,  6,  9,  4),  # 1 NE      9 = Hit laser
           (8,  1,  0,  7,  9,  5,  4,  3),  # 2 E
           (1,  0,  9,  6,  5,  4,  8,  2),  # 3 SE
           (9,  7,  6,  5,  8,  3,  2,  1),  # 4 S
           (7,  6,  8,  4,  3,  2,  9,  0),  # 5 SW
           (8,  5,  4,  3,  9,  1,  0,  7),  # 6 W
           (5,  4,  9,  2,  1,  0,  8,  6))  # 7 NW

select_x = 0        # Coordinates of selected piece
select_y = 0
hit_x = -1          # Coordinates of piece hit by a laser beam
hit_y = -1
move_count = 0      # Count of moves for each payers turn


# ---------------------------------------------------------------------------
def init_game():
    """Initialize the board and game state for a new game."""

    global move_count

    # Clear cells from previous game
    for row in GameState.grid:
        for cell in row:
            cell.clear()

    # Place laser cannons on grid
    x = GameState.SQUARE_COUNT - 1
    for y in range(1, GameState.SQUARE_COUNT, 3):
        GameState.grid[y][0].set(Cell.RED_TEAM, Cell.LASER, Cell.RIGHT)
        GameState.grid[y][x].set(Cell.GRN_TEAM, Cell.LASER, Cell.LEFT)

    # place mirrors on grid
    for x, y, angle in INIT_MIRRORS:
        GameState.grid[y][x].set(Cell.RED_TEAM, Cell.MIRROR, angle)
        x = x + 8 - (x << 1)
        if angle != 4: angle ^= 4
        GameState.grid[y][x].set(Cell.GRN_TEAM, Cell.MIRROR, angle)

    # The loser of last game gets first move
    if GameState.grn_laser_count == 0:
        GameState.player = Cell.RED_TEAM
    else:
        GameState.player = Cell.GRN_TEAM

    # Reset counts
    move_count = 2
    GameState.red_laser_count = 3
    GameState.grn_laser_count = 3
    GameState.state = GameState.WAIT

    # Reset the cursor
    GameState.cursor_x = 4
    GameState.cursor_y = 4


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

    while True:

        # Save current coordinates
        laser_path_append(x, y)

        # Get the current cell
        cell = GameState.grid[y][x]

        # If current cell is a mirror, get new direction of travel
        if cell.actor == Cell.MIRROR:
            direction = NEW_DIR[direction][cell.angle]

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
                laser_path_append(x, y)
                laser_path_append(x + 1, y)
                y += 1
                direction = GameState.SW
            case [GameState.NW, _, -1]: # Left side
                laser_path_append(x, y)
                laser_path_append(x, y + 1)
                x += 1
                direction = GameState.NE

            case [GameState.NE, -1, GameState.SQUARE_COUNT]: # Top right corner
                hit_mirror_face(x, y)
                return
            case [GameState.NE, -1, _]: # Top side
                laser_path_append(x, y)
                laser_path_append(x - 1, y)
                y += 1
                direction = GameState.SE
            case [GameState.NE, _, GameState.SQUARE_COUNT]: # Right side
                laser_path_append(x, y)
                laser_path_append(x, y + 1)
                x -= 1
                direction = GameState.NW

            case [GameState.SW, GameState.SQUARE_COUNT, -1]: # Bottom left corner
                hit_mirror_face(x, y)
                return
            case [GameState.SW, GameState.SQUARE_COUNT, _]: # Bottom side
                laser_path_append(x, y)
                laser_path_append(x + 1, y)
                y -= 1
                direction = GameState.NW
            case [GameState.SW, _, -1]: # Left side
                laser_path_append(x, y)
                laser_path_append(x, y - 1)
                x += 1
                direction = GameState.SE

            case [GameState.SE, GameState.SQUARE_COUNT, GameState.SQUARE_COUNT]: # Bottom right corner
                hit_mirror_face(x, y)
                return
            case [GameState.SE, GameState.SQUARE_COUNT, _]: # Bottom side
                laser_path_append(x, y)
                laser_path_append(x - 1, y)
                y -= 1
                direction = GameState.NE
            case [GameState.SE, _, GameState.SQUARE_COUNT]: # Right side
                laser_path_append(x, y)
                laser_path_append(x, y - 1)
                x -= 1
                direction = GameState.SW

            case [GameState.N, -1, _]: # Top side
                hit_mirror_face(x, y)
                return
            case [GameState.S, GameState.SQUARE_COUNT, _]: # Bottom side
                hit_mirror_face(x, y)
                return
            case [GameState.W, _, -1]: # Left side
                hit_mirror_face(x, y)
                return
            case [GameState.E, _, GameState.SQUARE_COUNT]: # Right side
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

    laser_path_append(x, y)
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
    elif GameState.cursor_x < 9:
        click_move()

    # If in action state and clicked on right most column
    else:
        click_action()


# ---------------------------------------------------------------------------
def click_wait():
    """Process selection of a game piece."""

    global select_x, select_y

    if GameState.cursor_x < 9:
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
    if selected.actor == Cell.MIRROR:
        if GameState.cursor_y < 8 and selected.angle != GameState.cursor_y:
            # Change the angle of selected cell
            selected.angle = GameState.cursor_y
            selected.selected = False
            move_count -= 1
            action_taken()

    # IF laser selected
    # And fire laser button pressed
    elif GameState.cursor_y == 8:
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
    elif GameState.cursor_y < 8:
        y = GameState.cursor_y
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

    if move_count == 0:
        move_count = 2
        GameState.cursor_x = 4
        GameState.cursor_y = 4
        match GameState.player:
            case Cell.RED_TEAM:
                GameState.player = Cell.GRN_TEAM
            case Cell.GRN_TEAM:
                GameState.player = Cell.RED_TEAM

    if GameState.red_laser_count == 0 or GameState.grn_laser_count == 0:
        GameState.state = GameState.END
