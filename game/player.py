import pygame as pg

from config import GameBoard, Players, PlayerType, States
from models import MODELS, Models


class Player:
    """
    ### Represents a player in the game.

    #### Attributes:
    - `player (Players)`: The player.
    - `type (PlayerType)`: The type of the player.
    - `brain (Models)`: The model used by the player to make decisions.
    - `turn (States)`: The state of the player's turn.
    - `win (States)`: The state of the player's win.

    #### Methods:
    - `move(board: GameBoard) -> tuple[int, int]`: Returns the move for a computer player.
    """

    def __init__(self, player: Players, type: PlayerType, brain: Models | None = None):
        self.player = player
        self.type = type
        self.brain = MODELS[brain] if brain else None
        if player == Players.X:
            self.turn = States.X_TURN
            self.win = States.X_WIN
        else:
            self.turn = States.O_TURN
            self.win = States.O_WIN

    def move(self, board: GameBoard) -> tuple[int, int]:
        """
        Returns the move for a computer player.

        Args:
            board (GameBoard): The current game board.

        Returns:
            tuple[int, int]: The move of the player.
        """
        pg.time.wait(500)
        move = self.brain(board, self.player)
        return move
