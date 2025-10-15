import os

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"

from .board.board import Board
from .game import Game
from .player import Player

__all__ = ["Board", "Game", "Player"]
