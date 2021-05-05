import sys

import pygame
import pygame.locals

import config
import constants
import game


def draw_board(window, state):
    pygame.draw.rect(window, (0, 0, 255),
                     pygame.Rect(config.BORDER, config.BORDER, config.Board.WIDTH, config.Board.HEIGHT))

    offset_x = config.BORDER + config.Board.BORDER
    offset_y = config.BORDER + config.Board.BORDER

    for row_i in range(config.Dimensions.ROWS):
        for col_i in range(config.Dimensions.COLS):
            x = offset_x + (config.GAP + config.HOLE_WIDTH) * col_i
            y = offset_y + (config.GAP + config.HOLE_HEIGHT) * row_i
            player = state.board[row_i][col_i]
            rect = pygame.Rect(x, y, config.HOLE_WIDTH, config.HOLE_HEIGHT)

            paint_user_color(window, player, rect)
            if col_i == state.col_selection and row_i == state.find_row_selection():
                paint_cursor(window, state, rect)


def paint_user_color(window, player, rect):
    pygame.draw.ellipse(window, config.Player.COLOR[player], rect)


def paint_cursor(window, state, rect):
    pygame.draw.ellipse(window, config.Player.COLOR[state.current_player], rect, config.Board.SELECTION_THICKNESS)


def handle_key_down(state, key):
    if key == pygame.locals.K_LEFT:
        state.move_left()
    elif key == pygame.locals.K_RIGHT:
        state.move_right()
    elif key == pygame.locals.K_SPACE:
        state.play()


def main():
    pygame.init()

    window = pygame.display.set_mode((config.Board.WIDTH + config.BORDER * 2, config.Board.HEIGHT + config.BORDER * 2),
                                     0,
                                     32)
    pygame.display.set_caption('CONNECT 4EVER')
    state = game.Game()

    while True:
        winner = None
        if state.is_over(constants.PLAYER1):
            winner = constants.PLAYER1
        if state.is_over(constants.PLAYER2):
            winner = constants.PLAYER2

        for event in pygame.event.get():
            if event.type == pygame.locals.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and winner is None:
                handle_key_down(state, event.key)

        draw_board(window, state)

        if winner is not None:
            print(f"fim: {winner}")
        pygame.display.update()


if __name__ == '__main__':
    main()
