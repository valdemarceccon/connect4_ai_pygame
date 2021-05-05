import config
from constants import PLAYER1, PLAYER2, EMPTY


def diagonals(arr: list[list[int]]) -> (list[int], list[int]):
    h, w = len(arr), len(arr[0])
    d1 = [[arr[h - p + q - 1][q]
           for q in range(max(p - h + 1, 0), min(p + 1, w))]
          for p in range(h + w - 1)]
    d2 = [[arr[p - q][q]
           for q in range(max(p - h + 1, 0), min(p + 1, w))]
          for p in range(h + w - 1)]
    return d1, d2


def is_sublist(list1, list2):
    for x in range(len(list1)):
        if list1[x:x + len(list2)] == list2:
            return True
    return False


class Game:
    def __init__(self):
        self.board = [[EMPTY for _ in range(config.Dimensions.COLS)] for _ in range(config.Dimensions.ROWS)]
        self.current_player = PLAYER1
        self.col_selection = 0

    def find_row_selection(self):
        for row in range(len(self.board)):
            if self.board[row][self.col_selection] != EMPTY:
                return row - 1
        return len(self.board) - 1

    def play(self, col=None, player=None):
        if player is None:
            player = self.current_player
            self.toggle_player()

        if col is None:
            col = self.col_selection

        x = -1
        for row in range(len(self.board)):
            if self.board[row][col] == EMPTY:
                x = row
            else:
                break

        if x != -1:
            self.board[x][col] = player

    def is_over(self, player):
        rows = self.board
        columns = [[c for c in x] for x in map(list, zip(*self.board))]
        d1, d2 = diagonals(self.board)

        player_victory = [player for _ in range(4)]
        result = any([is_sublist(v, player_victory) for v in rows]) or any(
            [is_sublist(v, player_victory) for v in columns]) or any(
            [is_sublist(v, player_victory) for v in d1]) or any([is_sublist(v, player_victory) for v in d2])

        return result

    def move_left(self):
        self.col_selection -= 1
        if self.col_selection < 0:
            self.col_selection = config.Dimensions.COLS - 1

    def move_right(self):
        self.col_selection += 1
        if self.col_selection >= config.Dimensions.COLS:
            self.col_selection = 0

    def toggle_player(self):
        self.current_player = PLAYER2 if self.current_player == PLAYER1 else PLAYER1
