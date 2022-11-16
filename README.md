# Laser Blast
Version 2.0

### Motivation
Why did I write this program, and why in Python? 
Well there were really two reasons. 
First I wanted to quickly test various game rules and strategies. 
Python and pygames made prototyping quick and easy. 
This is actually about the twentieth version of the game. 
Second I wanted to try the new match/case statements that were added in Python 3.10.
I found lots of uses for match/case and I really like it.

### Installation
This program requires Python 3.10 or later, and pygames.
I am currently running pygames 2.1.2.
To install, copy this file and the 5 source files to a directory on your computer.
To run enter: python LaserBlast.py

### Game Board
The game board consisting of an 9 by 9 grid with red and green game pieces.
The pointy circles are laser cannons, and the lines are double-sided mirrors.
The object of the game is to maneuver your laser cannons and mirrors so that you can fire your 
laser cannon and destroy your opponents' laser cannons.

### Making Moves
The color of the border indicates which players turn it is.
For each turn a player makes two moves. 
A single move can be:

- Moving a game piece one square in any direction to an empty square.
- Rotating a game piece.
- Firing a laser cannon.

First maneuver the white cross over the piece to be selected and click.
To move: maneuver the white cross to the destination square and click. 
To rotate: maneuver the cross to one of the images on the right side of the board and click.
To fire a laser: maneuver the cross to the FIRE text on the right side of the board and click. 
If you plan to move twice, you can do this in one step, this allows you to jump over other pieces.

### Firing the Laser
The laser cannons can be rotated to eight orientations. 
The mirrors can be rotated to eight orientations.
The four borders are also covered in mirrors.
This allows the laser beam to travel horizontally, vertically or diagonally.
If the beam hits square to the face of a mirror, it will bounce back and destroy the 
laser cannon that fired it.
If the beam hits the edge of a mirror, the mirror is destroyed.
Since the borders are mirrors, the laser beam will bounce around until something is destroyed.

### User Inputs
The red player can use either the mouse or game controller 1 for input. 
The green player can use the keyboard or game controller 0 for input.
The keyboard uses the arrow keys to move the cross and either ENTER or SPACE to select.
