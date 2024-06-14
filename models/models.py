import enum
from typing import TYPE_CHECKING, Callable

import numpy as np
import torch

from utils import GameBoard, Players, States

from .minimax import minimax_algo
from .neural_net import TicTacToeNet

if TYPE_CHECKING:
    from game import Board


def random(board: GameBoard, _) -> tuple[int, int]:
    """
    Returns a random empty position on the board.

    Args:
        board (GameBoard): The current 2D game board.
        _ (Any): Ignored argument.

    Returns:
        tuple[int, int]: The coordinates of a random empty position on the board.
    """
    empty_positions = np.argwhere(np.equal(board, None))
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
        return random(board.board_2d, player)
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
        return random(board.board_2d, player)
    else:
        return minimax(board, player)


def neural_net(board: "Board", _: Players) -> tuple[int, int]:
    """
    Returns the best move for the current player using a neural network.

    Args:
        board (Board): The game board object.
        _ (Any): Ignored argument.

    Returns:
        tuple[int, int]: The coordinates of the best move.
    """
    file = "data/models/mlp_model.pth"
    net = TicTacToeNet()
    net.load_state_dict(torch.load(file))
    net.eval()
    state = torch.tensor([board.flat_board], dtype=torch.float32)
    move = net.select_move(state)
    return move if board.check_square(*move) is None else random(board.board_2d, _)


class Models(enum.Enum):
    EASY = 0
    MEDIUM = 1
    HARD = 2
    IMPOSSIBLE = 3
    NEURAL_NET = 4


MODELS: dict[Models, Callable[["Board", Players], tuple[int, int]]] = {
    Models.EASY: random,
    Models.MEDIUM: medium,
    Models.HARD: hard,
    Models.IMPOSSIBLE: minimax,
    Models.NEURAL_NET: neural_net,
}
