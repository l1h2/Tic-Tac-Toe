import enum

import numpy as np

from config import GameBoard, Players, States

from .minimax import minimax_algo


class Models(enum.Enum):
    EASY = 0
    MEDIUM = 1
    HARD = 2
    IMPOSSIBLE = 3


def random(board: GameBoard, _) -> tuple[int, int]:
    """
    Returns a random empty position on the board.

    Args:
        board (GameBoard): The current game board.
        _ (Any): Ignored argument.

    Returns:
        tuple[int, int]: The coordinates of a random empty position on the board.
    """
    empty_positions = np.argwhere(np.equal(board, None))
    return tuple(empty_positions[np.random.choice(empty_positions.shape[0])])


def minimax(board: GameBoard, player: Players) -> tuple[int, int]:
    """
    Returns the best move for the current player using the minimax algorithm.

    Args:
        board (GameBoard): The current game board.
        player (Players): The current player.

    Returns:
        tuple[int, int]: The coordinates of the best move.
    """
    opponent = Players.X if player == Players.O else Players.O
    scores = {player: 10, opponent: -10, States.DRAW: 0}
    return minimax_algo(
        board,
        player,
        opponent,
        player,
        0,
        scores,
        -np.inf,
        np.inf,
    )


def medium(board: GameBoard, player: Players) -> tuple[int, int]:
    """
    Chooses between the best move with a 50% chance.

    Args:
        board (GameBoard): The current game board.
        player (Players): The current player.

    Returns:
        tuple[int, int]: The coordinates of the selected move.
    """
    if np.random.rand() < 0.5:
        return random(board, player)
    else:
        return minimax(board, player)


def hard(board: GameBoard, player: Players) -> tuple[int, int]:
    """
    Chooses between the best move with a 80% chance.

    Args:
        board (GameBoard): The current game board.
        player (Players): The current player.

    Returns:
        tuple[int, int]: The coordinates of the selected move.
    """
    if np.random.rand() < 0.2:
        return random(board, player)
    else:
        return minimax(board, player)


MODELS = {
    Models.EASY: random,
    Models.MEDIUM: medium,
    Models.HARD: hard,
    Models.IMPOSSIBLE: minimax,
}
