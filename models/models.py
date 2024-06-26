import enum
from typing import TYPE_CHECKING, Optional, Protocol

import numpy as np
import torch

from utils import Players, States

from .minimax import minimax_algo
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
    empty_positions = np.argwhere(np.equal(board.board_2d, None))
    return tuple(empty_positions[np.random.choice(empty_positions.shape[0])])


def minimax(board: "Board", player: Players) -> tuple[int, int]:
    """
    Returns the best move for the current player using the minimax algorithm.

    Args:
        board (Board): The game board object.
        player (Players): The current player.

    Returns:
        tuple[int, int]: The coordinates of the best move.
    """
    opponent = Players.X if player == Players.O else Players.O
    scores = {player: 20, opponent: -20, States.DRAW: 0}
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
        return random(board, player)
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
        return random(board, player)
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
    EASY = 0
    MEDIUM = 1
    HARD = 2
    IMPOSSIBLE = 3


class NeuralNetworks(enum.Enum):
    MLP = 0


class ModelProtocol(Protocol):
    def __call__(self, board: "Board", players: Players) -> tuple[int, int]: ...


class NeuralNetworkProtocol(Protocol):
    def __call__(
        self, board: "Board", hint: Optional[bool]
    ) -> tuple[int, int] | list[float]: ...


MODELS: dict[Models, ModelProtocol] = {
    Models.EASY: random,
    Models.MEDIUM: medium,
    Models.HARD: hard,
    Models.IMPOSSIBLE: minimax,
}

NEURAL_NETWORKS: dict[NeuralNetworks, NeuralNetworkProtocol] = {NeuralNetworks.MLP: mlp}
