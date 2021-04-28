import game


class Board:
    BORDER = 10
    WIDTH = 800
    HEIGHT = 600
    SELECTION_THICKNESS = 10


class Dimensions:
    COLS = 7
    ROWS = 6


class Player:
    COLOR = {
        game.PLAYER1: (255, 255, 0),
        game.PLAYER2: (255, 0, 0),
        game.EMPTY: (255, 255, 255)
    }


GAP = 20
BORDER = 10
HOLE_WIDTH = (Board.WIDTH - (2 * Board.BORDER + (Dimensions.COLS - 1) * GAP)) / Dimensions.COLS
HOLE_HEIGHT = (Board.HEIGHT - (2 * Board.BORDER + (Dimensions.ROWS - 1) * GAP)) / Dimensions.ROWS
