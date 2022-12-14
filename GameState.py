# ---------------------------------------------------------------------------
# Laser Blast, Game State
#
# History
#  1 Nov 2022 Mike Christle     Created
# 14 Nov 2022 Mike Christle     Add mirrors to the borders
# 15 Nov 2022 Mike Christle     Switch to 9x9 square grid
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


N  = 0
NE = 1
E  = 2
SE = 3
S  = 4
SW = 5
W  = 6
NW = 7

END = 0     # End of game, one player lost all lasers
WAIT = 1    # Waiting for the red player to select a piece
ACTION = 3  # Waiting for player to select an action

# State of play
state = WAIT
player = Cell.RED_TEAM

# The grid stores the state of the playing board
SQUARE_COUNT = 9
grid = [[Cell() for _ in range(SQUARE_COUNT)] for _ in range(SQUARE_COUNT)]

# Location of the cursor on the board
cursor_x = 0
cursor_y = 0

# Count of each players lasers
grn_laser_count = 0
red_laser_count = 0
