# ---------------------------------------------------------------------------
# Laser Blast, Cell
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
class Cell:
    EMPTY = 0
    MIRROR = 1
    LASER = 2

    NO_TEAM = 0
    RED_TEAM = 1
    GRN_TEAM = 2

    UP = 0
    RIGHT = 2
    DOWN = 4
    LEFT = 6

    _teams = ('None', 'Red', 'Green')
    _actors = ('Empty', 'Mirror', 'Laser')

    # -----------------------------------------------------------------------
    def __init__(self):
        self.actor = Cell.EMPTY
        self.team = Cell.NO_TEAM
        self.angle = 0
        self.selected = False

    # -----------------------------------------------------------------------
    def clear(self):
        self.actor = Cell.EMPTY
        self.selected = False

    # -----------------------------------------------------------------------
    def set(self, team, actor, angle):
        self.team = team
        self.actor = actor
        self.angle = angle
        self.selected = False

    # -----------------------------------------------------------------------
    # Move contents of a cell to a destination cell
    # cell0.move_to(cell1)
    # Contents of cell0 are copied to cell1, then cell0 is cleared
    # -----------------------------------------------------------------------
    def move_to(self, to):
        to.team = self.team
        to.actor = self.actor
        to.angle = self.angle
        to.selected = False
        self.actor = Cell.EMPTY
        self.selected = False

    # -----------------------------------------------------------------------
    def __repr__(self):
        team = Cell._teams[self.team]
        actor = Cell._actors[self.actor]
        return f'{team} {actor} {self.angle} {self.selected}'

