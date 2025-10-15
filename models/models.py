import enum
from collections.abc import Callable
from typing import TYPE_CHECKING

import numpy as np
import torch

from utils import Players

from .minimax import minimax
from .neural_net import TicTacToeNet

if TYPE_CHECKING:
    from game import Board


def random(board: "Board", _=None) -> tuple[int, int]:
    """
    Returns a random empty position on the board.

    Args:
        board (Board): The game board object.
        _ (Any): Ignored argument.

    Returns:
        tuple[int, int]: The coordinates of a random empty position on the board.
    """
    empty_positions = np.argwhere(np.equal(board.board_2d, None))  # type: ignore
    return tuple(empty_positions[np.random.choice(empty_positions.shape[0])])


def medium(board: "Board", player: Players) -> tuple[int, int]:
    """
    Chooses between the best move with a 50% chance.

    Args:
        board (Board): The game board object.
        player (Players): The current player.

    Returns:
        tuple[int, int]: The coordinates of the selected move.
    """
    if np.random.rand() < 0.5:
        return random(board)
    else:
        return minimax(board, player)


def hard(board: "Board", player: Players) -> tuple[int, int]:
    """
    Chooses between the best move with a 80% chance.

    Args:
        board (Board): The game board object.
        player (Players): The current player.

    Returns:
        tuple[int, int]: The coordinates of the selected move.
    """
    if np.random.rand() < 0.2:
        return random(board)
    else:
        return minimax(board, player)


def mlp(board: "Board", hint: bool = False) -> tuple[int, int] | list[float]:
    """
    Returns the best move for the current player using a neural network.

    Args:
        board (Board): The game board object.
        hint (bool): Whether to return the move or the probabilities.

    Returns:
        tuple[int, int]: The coordinates of the best move.
    """
    net = TicTacToeNet("data/models/mlp_model.pth")
    state = torch.tensor([board.flat_board], dtype=torch.float32)

    if hint:
        return net.get_move_probabilities(state)

    move = net.select_move(state)
    return move if board.check_square(*move) is None else random(board)


class Models(enum.Enum):
    """
    Enum class for the different models.

    Attributes:
        EASY (int): Random model.
        MEDIUM (int): Random with 50% or minimax model.
        HARD (int): Random with 20% chance or minimax model.
        IMPOSSIBLE (int): Minimax model.
    """

    EASY = 0
    MEDIUM = 1
    HARD = 2
    IMPOSSIBLE = 3


class NeuralNetworks(enum.Enum):
    MLP = 0


MODELS: dict[Models, Callable[["Board", Players], tuple[int, int]]] = {
    Models.EASY: random,
    Models.MEDIUM: medium,
    Models.HARD: hard,
    Models.IMPOSSIBLE: minimax,
}

NEURAL_NETWORKS: dict[
    NeuralNetworks, Callable[["Board", bool], tuple[int, int] | list[float]]
] = {NeuralNetworks.MLP: mlp}
