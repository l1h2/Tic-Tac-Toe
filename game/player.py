import pygame as pg

from models import MODELS, Models
from utils import Players, PlayerType, States

from .board.board import Board


class Player:
    """
    ### Represents a player in the game.

    #### Parameters:
    - `player (Players)`: The player (X or O).
    - `type (PlayerType)`: The type of the player (HUMAN or COMPUTER).
    - `brain (Models | None)`: The AI model for the computer player (defaults to Models.EASY).

    #### Properties:
    - `player (Players)`: The player (X or O).
    - `type (PlayerType)`: The type of the player (HUMAN or COMPUTER).
    - `turn (States)`: The state of the player's turn.
    - `win (States)`: The state of the player's win.

    #### Methods:
    - `move(board: Board) -> tuple[int, int]`: Returns the move for a computer player.
    """

    def __init__(self, player: Players, type: PlayerType, brain: Models = Models.EASY):
        self._player = player
        self._type = type
        self._brain = MODELS[brain]

        if player == Players.X:
            self._turn = States.X_TURN
            self._win = States.X_WIN
        else:
            self._turn = States.O_TURN
            self._win = States.O_WIN

    @property
    def player(self) -> Players:
        """The player (X or O)."""
        return self._player

    @property
    def type(self) -> PlayerType:
        """The type of the player (HUMAN or COMPUTER)."""
        return self._type

    @property
    def turn(self) -> States:
        """The state of the player's turn."""
        return self._turn

    @property
    def win(self) -> States:
        """The state of the player's win."""
        return self._win

    def move(self, board: Board) -> tuple[int, int]:
        """
        Returns the move for a computer player.

        Args:
            board (Board): The current game board.

        Returns:
            tuple[int, int]: The move of the player.
        """
        pg.time.wait(500)
        return self._brain(board, self.player)
