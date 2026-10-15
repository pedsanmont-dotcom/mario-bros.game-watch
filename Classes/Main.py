"""
Main entry point for the Mario Bros Game & Watch game.
Creates the game board and starts the Pyxel game loop.
"""
import constants
from Board import Board

# Creating the board object will also initialize pyxel
board = Board(constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT)


