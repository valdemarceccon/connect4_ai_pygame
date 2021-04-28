import config

PLAYER1 = 1
PLAYER2 = 2
EMPTY = 0


def get_diags(arr):
    return None


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

    def is_over(self):
        lines = ["".join([str(c) for c in x]) for x in self.board]

        for line in lines:
            if str(PLAYER1) * 4 in line:
                return PLAYER1
            if str(PLAYER2) * 4 in line:
                return PLAYER2

        columns = ["".join([str(c) for c in x]) for x in map(list, zip(*self.board))]

        for col in columns:
            if str(PLAYER1) * 4 in col:
                return PLAYER1
            if str(PLAYER2) * 4 in col:
                return PLAYER2

        diags = get_diags(self.board)

        return None

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
