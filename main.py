import sys

import pygame
import pygame.freetype
import pygame.locals

import ai
import config
import game


def draw_board(window, game_state, col_selection):
    pygame.draw.rect(window, (0, 0, 255),
                     pygame.Rect(config.BORDER, config.BORDER, config.Board.WIDTH, config.Board.HEIGHT))

    offset_x = config.BORDER + config.Board.BORDER
    offset_y = config.BORDER + config.Board.BORDER

    for row_i in range(config.Dimensions.ROWS):
        for col_i in range(config.Dimensions.COLS):
            x = offset_x + (config.GAP + config.HOLE_WIDTH) * col_i
            y = offset_y + (config.GAP + config.HOLE_HEIGHT) * row_i
            player = game_state.board[row_i][col_i]
            rect = pygame.Rect(x, y, config.HOLE_WIDTH, config.HOLE_HEIGHT)

            paint_user_color(window, player, rect)
            if col_i == col_selection and row_i == game_state.find_next_row(col_selection):
                paint_cursor(window, game_state, rect)


def paint_user_color(window, player, rect):
    pygame.draw.ellipse(window, config.Player.COLOR[player], rect)


def paint_cursor(window, state, rect):
    pygame.draw.ellipse(window, config.Player.COLOR[state.current_player], rect, config.Board.SELECTION_THICKNESS)


def move_left(game_state, col):
    col -= 1
    if col < 0:
        col = config.Dimensions.COLS - 1

    if game_state.is_col_full(col):
        return move_left(game_state, col)

    return col


def move_right(game_state, col):
    col += 1
    if col >= config.Dimensions.COLS:
        col = 0
    if game_state.is_col_full(col):
        return move_right(game_state, col)
    return col


def handle_key_down(game_state, col, key):
    if not game_state.is_board_full():
        if key == pygame.locals.K_LEFT:
            return move_left(game_state, col)
        elif key == pygame.locals.K_RIGHT:
            return move_right(game_state, col)
        elif key == pygame.locals.K_SPACE:
            game_state.play(col)
            if not game_state.is_board_full() and game_state.is_col_full(col):
                return move_right(game_state, col)
    return col


def write_text_line(window, text, color, base_y):
    font = pygame.freetype.Font('Roboto-Regular.ttf', 60)
    text_obj, rect = font.render(text, color)
    base_x = config.Board.BORDER + config.GAP
    if base_y == 0:
        base_y = config.Board.HEIGHT / 4
    else:
        base_y += rect.y + config.GAP

    window.blit(text_obj, (base_x, base_y))

    return base_y + rect.y


def display_winner(window, winner, c1, c2):
    pygame.draw.rect(window, c1,
                     pygame.Rect(config.BORDER, config.BORDER, config.Board.WIDTH, config.Board.HEIGHT))
    text_height = 0
    if winner is None:
        winner = "nenhum"
    text_height = write_text_line(window, f"ACABOU, jogador {winner}", c2, text_height)
    text_height = write_text_line(window, f"ganhou", c2, text_height)
    text_height = write_text_line(window, "Precione R para", c2, text_height)
    write_text_line(window, "REINICIAR", c2, text_height)


def main():
    ai_player = None
    if len(sys.argv[1:]) > 0:
        print(sys.argv[1:])
        ai_player = int(sys.argv[2])

    pygame.init()

    window = pygame.display.set_mode((config.Board.WIDTH + config.BORDER * 2, config.Board.HEIGHT + config.BORDER * 2),
                                     0,
                                     32)
    pygame.display.set_caption('CONNECT 4EVER')
    state = game.Game()
    count = 0
    clock = pygame.time.Clock()
    c1, c2 = (255, 255, 255), (0, 0, 255)
    winner = None
    col_selection = 0

    while True:
        cur_player = state.current_player
        if not winner:
            winner = state.winner
            if winner:
                c1 = config.Player.COLOR[winner]

        if ai_player == cur_player and not winner:
            ai.exec_best_move(state)

        for event in pygame.event.get():
            if event.type == pygame.locals.QUIT:
                pygame.quit()
                sys.exit()
            else:
                if event.type == pygame.KEYDOWN and winner is None:
                    col_selection = handle_key_down(state, col_selection, event.key)
                if event.type == pygame.KEYDOWN and event.key == pygame.locals.K_r:
                    state = game.Game()
                    cur_player = state.current_player
                    winner = state.winner
                if event.type == pygame.KEYDOWN and event.key == pygame.locals.K_u:
                    state.undo_play()
                    state.undo_play()
                    winner = state.winner

        if not winner:
            draw_board(window, state, col_selection)

        if winner is not None or state.is_board_full():
            count += 1
            count = count % 10

            if not count:
                c1, c2 = c2, c1

            display_winner(window, winner, c1, c2)
        pygame.display.update()
        clock.tick(60)


if __name__ == '__main__':
    main()
