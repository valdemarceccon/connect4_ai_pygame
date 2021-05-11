import config
import constants
from constants import PLAYER1, PLAYER2, EMPTY
from utils import get_columns, diagonals, is_sublist


class Game:
    def __init__(self):
        self.board = [[EMPTY for _ in range(config.Dimensions.COLS)] for _ in range(config.Dimensions.ROWS)]
        self.current_player = PLAYER1
        self.winner = None
        self.moves = []

    def undo_play(self):
        if not self.moves:
            return

        move = self.moves.pop()

        for row in self.board:
            if row[move] != EMPTY:
                self.current_player = row[move]
                row[move] = EMPTY
                self.winner = None
                break

    def find_next_row(self, col):
        for row in range(len(self.board)):
            if self.board[row][col] != EMPTY:
                return row - 1
        return len(self.board) - 1

    def play(self, col, player=None):
        if col is None:
            return

        if player is None:
            player = self.current_player

        x = self.find_next_row(col)

        if x != -1:
            self.board[x][col] = player
            self.moves.append(col)

        if self.is_over(player):
            self.winner = player
        else:
            self.toggle_player()

    def is_col_full(self, col):
        return self.board[0][col] != constants.EMPTY

    def is_board_full(self):
        for c in range(config.Dimensions.COLS):
            if not self.is_col_full(c):
                return False
        return True

    def is_over(self, player):
        rows = self.board
        columns = get_columns(self.board)
        diags = diagonals(self.board)

        player_victory = [player for _ in range(4)]
        result = any([is_sublist(v, player_victory) for v in rows]) or any(
            [is_sublist(v, player_victory) for v in columns]) or any(
            [is_sublist(v, player_victory) for v in diags])

        return result

    def toggle_player(self):
        self.current_player = PLAYER2 if self.current_player == PLAYER1 else PLAYER1
