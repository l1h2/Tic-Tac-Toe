from typing import TYPE_CHECKING

import numpy as np

from utils import Players, States

if TYPE_CHECKING:
    from game import Board


def minimax_algo(
    board: "Board",
    player: Players,
    opponent: Players,
    current_player: Players,
    depth: int,
    scores: dict[Players | States, int],
    alpha: int,
    beta: int,
) -> int | tuple[int, int]:
    """
    Returns the best score or the best move for the current player using the minimax algorithm.

    Args:
        board (Board): The game board object.
        player (Players): The maximizing player.
        opponent (Players): The minimizing player.
        current_player (Players): The current player.
        depth (int): The current depth of the search.
        scores (dict[Players  |  States, int]): The scores for each player and state.
        alpha (int): The alpha value.
        beta (int): The beta value.

    Returns:
        int | tuple[int, int]: The best score or the best move.
    """
    winner = board.bit_board.check_win()
    if winner is not None:
        depth_weight = depth if player == winner else -depth
        return scores[winner] - depth_weight

    if current_player == player:
        best_score = -np.inf
        next_player = opponent
    else:
        best_score = np.inf
        next_player = player

    for i in range(3):
        for j in range(3):
            if not board.bit_board.check_move(i, j):
                continue

            # Prioritize blocking moves when loss is imminent
            blocking_bonus = (
                0.1
                if current_player == player
                and is_blocking_move(board, i, j, next_player)
                else 0
            )

            board.bit_board.move(i, j, current_player)
            score = minimax_algo(
                board,
                player,
                opponent,
                next_player,
                depth + 1,
                scores,
                alpha,
                beta,
            )
            score += blocking_bonus
            board.bit_board.clear_move(i, j)

            if depth > 0:
                if current_player == player:
                    best_score = max(score, best_score)
                    alpha = max(alpha, score)
                else:
                    best_score = min(score, best_score)
                    beta = max(beta, score)

            if beta <= alpha:
                break

            if score > best_score and depth == 0:
                best_score = score
                move = (i, j)
        if beta <= alpha:
            break

    return move if depth == 0 else best_score


def is_blocking_move(board: "Board", row: int, col: int, opponent: Players) -> bool:
    """
    Return whether the move blocks the opponent's winning move.

    Args:
        board (Board): The game board object.
        row (int): The row of the move.
        col (int): The column of the move.
        opponent (Players): The opponent player.

    Returns:
        bool: Whether the move blocks the opponent's winning move.
    """
    board.bit_board.move(row, col, opponent)
    winner = board.bit_board.check_win()
    board.bit_board.clear_move(row, col)
    return winner and winner != States.DRAW
