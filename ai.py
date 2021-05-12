import copy
import math

import config
import constants
import game
import utils


def possible_moves(game_state: game.Game):
    return [move for move in range(config.Dimensions.COLS) if not game_state.is_col_full(move)]


def min_max(game_state: game.Game, maximizing_player, depth, alpha, beta):
    is_maximizing = maximizing_player == game_state.current_player

    if depth <= 0 or game_state.is_board_full():
        value = board_evaluation(game_state)
        return value if is_maximizing else -value

    if game_state.winner:
        return math.inf if is_maximizing else -math.inf

    val = -math.inf if is_maximizing else math.inf
    for c in possible_moves(game_state):
        copy_state = copy.deepcopy(game_state)
        copy_state.play(c)
        if is_maximizing:
            val = max(min_max(copy_state, maximizing_player, depth - 1, alpha, beta), val)
            alpha = max(alpha, val)
            if alpha >= beta:
                break
        else:
            val = min(min_max(copy_state, maximizing_player, depth - 1, alpha, beta), val)
            beta = min(beta, val)
            if beta <= alpha:
                break

    return val


def exec_best_move(game_state: game.Game):
    best_score = -math.inf
    best_move = None
    maximizing_player = game_state.current_player
    for c in possible_moves(game_state):
        copy_state = copy.deepcopy(game_state)
        copy_state.play(c)
        score = min_max(copy_state, maximizing_player, config.THINKING_DEPTH, -math.inf, math.inf)
        if score > best_score:
            best_score = score
            best_move = c

    if best_move is not None:
        game_state.play(best_move)
    else:
        game_state.play(possible_moves(game_state)[0])


def board_evaluation(state: game.Game):
    curr_player = state.current_player
    total = 0

    total += max_points_in_all(state.board, curr_player)
    total += max_points_in_all(utils.get_columns(state.board), curr_player)
    total += max_points_in_all(utils.diagonals(state.board), curr_player)

    return total


def max_points_in_all(lists, player):
    max_found = 0
    for sub_list in lists:
        max_found = max(max_found, points_counter(sub_list, player))
    return max_found


def points_counter(values, target):
    best_found = 1
    for window in windows(values, 4):
        if count_seq(window, target) == 4:
            return math.inf
        if count_seq(window, target) == 3 and count_seq(window, constants.EMPTY):
            best_found = max(9, best_found)
        if count_seq(window, target) == 2 and count_seq(window, constants.EMPTY) == 2:
            best_found = max(3, best_found)
        if count_seq(window, target) == 1 and count_seq(window, constants.EMPTY) == 3:
            best_found = max(2, best_found)

    return best_found


def count_seq(arr, target):
    count = 0
    m = 0
    for i in arr:
        if i == target:
            count += 1
        else:
            m = max(count, m)
            count = 0

    return max(m, count)


def windows(arr, size):
    if len(arr) < size:
        return None
    width = len(arr)
    for c in range(width - size + 1):
        yield arr[c:c + size]
