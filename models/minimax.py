from typing import TYPE_CHECKING

import numpy as np

from utils import Players, States

if TYPE_CHECKING:
    from game import Board


def minimax(board: "Board", player: Players) -> tuple[int, int]:
    """
    Returns the best score or the best move for the current player using the minimax algorithm.

    Args:
        board (Board): The game board object.
        player (Players): The maximizing player.

    Returns:
        float | tuple[int, int]: The best score or the best move.
    """
    opponent = Players.X if player == Players.O else Players.O
    scores = {player: 20.0, opponent: -20.0, States.DRAW: 0.0}

    move: tuple[int, int] = (-1, -1)
    best_score = -np.inf

    for i in range(3):
        for j in range(3):
            if not board.bit_board.check_move(i, j):
                continue

            # Prioritize blocking moves when loss is imminent
            blocking_bonus = 0.1 if _is_blocking_move(board, i, j, opponent) else 0

            board.bit_board.move(i, j, player)
            score = _minimax_recursive(
                board,
                player,
                opponent,
                opponent,
                1,
                scores,
                -np.inf,
                np.inf,
            )
            score += blocking_bonus
            board.bit_board.clear_move(i, j)

            if score > best_score:
                best_score = score
                move = (i, j)

    return move


def _minimax_recursive(
    board: "Board",
    player: Players,
    opponent: Players,
    current_player: Players,
    depth: int,
    scores: dict[Players | States, float],
    alpha: float,
    beta: float,
) -> float:
    """Recursive helper function for the minimax algorithm with alpha-beta pruning."""
    winner = board.winner
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
                and _is_blocking_move(board, i, j, next_player)
                else 0
            )

            board.bit_board.move(i, j, current_player)
            score = _minimax_recursive(
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

            if current_player == player:
                best_score = max(score, best_score)
                alpha = max(alpha, score)
            else:
                best_score = min(score, best_score)
                beta = max(beta, score)

            if beta <= alpha:
                break

        if beta <= alpha:
            break

    return best_score


def _is_blocking_move(board: "Board", row: int, col: int, opponent: Players) -> bool:
    """Return whether the move blocks the opponent's winning move."""
    board.bit_board.move(row, col, opponent)
    winner = board.winner
    board.bit_board.clear_move(row, col)
    return winner is not None and winner != States.DRAW
