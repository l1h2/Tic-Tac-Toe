import pygame as pg

from utils import PlayerType, States, Wins

from .board import Board
from .player import Player


class Game:
    """
    ### Represents the main game loop.

    #### Attributes:
    - `FPS (int)`: The frames per second of the game.
    - `X (Player)`: The player object for X.
    - `O (Player)`: The player object for O.
    - `board (Board)`: The game board object.
    - `current_player (Player)`: The current player.
    - `winner (States)`: The winner of the game.
    - `winning_line (tuple[tuple[int, int], tuple[int, int]])`: The winning line on the board.
    - `win_type (Wins)`: The type of win.
    - `running (bool)`: The state of the game loop.
    - `turn (int)`: The current turn number.

    #### Methods:
    - `run() -> None`: Runs the main game loop.
    """

    FPS = 30

    def __init__(self, X: Player, O: Player, ai_hints: bool = False):
        self.board = Board(ai_hints)
        self.X = X
        self.O = O
        self.current_player = X
        self.winner = None
        self.winning_line = None
        self.win_type = None
        self.running = False
        self.turn = 0

    def run(self) -> None:
        """
        Runs the main game loop.
        """
        self.__load()
        self.running = True

        while self.running:
            if self.current_player.type == PlayerType.COMPUTER:
                self.__computer_turn()
            self.__handle_events()
            pg.display.update()
            self.clock.tick(self.FPS)

    def __load(self) -> None:
        """
        Loads the game window and assets.
        """
        pg.init()
        self.clock = pg.time.Clock()
        self.board.setup()

    def __computer_turn(self) -> None:
        """
        Plays a move for the computer player.
        """
        self.__play_move(*self.current_player.move(self.board))

    def __handle_events(self) -> bool:
        """
        Handles the game events.

        - `pg.QUIT`: Quits the game.
        - `pg.MOUSEBUTTONUP`: Plays a move on the board.
        """
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
            elif event.type == pg.MOUSEBUTTONUP:
                self.__play_move(*self.__get_move(event.pos))

    def __get_move(self, click_pos: tuple[float, float]) -> tuple[int, int]:
        """
        Returns the row and column of the move based on the click position.

        Args:
            click_pos (tuple[float, float]): The position of the click.

        Returns:
            tuple[int, int]: The row and column of the move.
        """
        x, y = click_pos
        row = y // (self.board.HEIGHT // 3)
        col = x // (self.board.WIDTH // 3)
        return (row, col)

    def __play_move(self, row: int, col: int) -> None:
        """
        Plays a move on the board.

        Args:
            row (int): The row of the move.
            col (int): The column of the move.
        """
        if not (0 <= row <= 2 and 0 <= col <= 2):
            return
        if not self.board.update(row, col, self.current_player.player):
            return

        self.turn += 1
        self.__check_win(row, col)
        self.__end_turn()

    def __check_win(self, row: int, col: int) -> None:
        """
        Checks if the current player has won the game.

        Args:
            row (int): The row of the last move.
            col (int): The column of the last move.
        """
        board = self.board.board_2d
        # Check row
        if all(board[row][i] == self.current_player.player for i in range(3)):
            self.winner = self.current_player.win
            self.winning_line = ((0, row), (2, row))
            self.win_type = Wins.ROW
            return
        # Check column
        if all(board[i][col] == self.current_player.player for i in range(3)):
            self.winner = self.current_player.win
            self.winning_line = ((col, 0), (col, 2))
            self.win_type = Wins.COL
            return
        # Check diagonals
        if row == col and all(
            board[i][i] == self.current_player.player for i in range(3)
        ):
            self.winner = self.current_player.win
            self.winning_line = ((0, 0), (2, 2))
            self.win_type = Wins.DIAG
            return
        if row + col == 2 and all(
            board[i][2 - i] == self.current_player.player for i in range(3)
        ):
            self.winner = self.current_player.win
            self.winning_line = ((0, 2), (2, 0))
            self.win_type = Wins.DIAG_2
            return
        # Check for draw
        if self.turn == 9:
            self.winner = States.DRAW

    def __end_turn(self) -> None:
        """
        Ends the current player's turn and switches to the next player.
        """
        if not self.winner:
            self.current_player = self.O if self.current_player == self.X else self.X
            self.board.draw_status(self.current_player.turn)
        else:
            self.__end_game()

    def __end_game(self) -> None:
        """
        Ends the game and displays the winner.
        """
        self.board.draw_status(self.winner)
        if self.winner != States.DRAW:
            self.board.draw_winning_line(*self.winning_line, self.win_type)
        pg.display.update()
        pg.time.wait(1000)
        self.__reset_game()

    def __reset_game(self) -> None:
        """
        Resets the game to the initial state.
        """
        self.current_player = self.X
        self.winner = None
        self.winning_line = None
        self.win_type = None
        self.turn = 0
        self.board.reset()
