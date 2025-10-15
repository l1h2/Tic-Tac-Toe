import pygame as pg

from utils import PlayerType, States, Wins

from .board.board import Board
from .player import Player, Players


class Game:
    """
    ### Represents the main game loop.

    #### Attributes:
    - `FPS (int)`: The frames per second of the game.

    #### Methods:
    - `run() -> None`: Runs the main game loop.
    """

    FPS = 30

    def __init__(self, X: Player, O: Player, ai_hints: bool = False):
        self._board = Board(ai_hints)
        self._X = X
        self._O = O
        self._current_player = X
        self._winner = None
        self._winning_line = None
        self._win_type = None
        self._running = False
        self._turn = 0

    def run(self) -> None:
        """
        Runs the main game loop.
        """
        self._load()
        self._running = True

        while self._running:
            if self._current_player.type == PlayerType.COMPUTER:
                self._computer_turn()
            self._handle_events()
            pg.display.update()
            self._clock.tick(self.FPS)

    def _load(self) -> None:
        """Loads the game window and assets."""
        pg.init()
        self._clock = pg.time.Clock()
        self._board.setup()

    def _computer_turn(self) -> None:
        """Plays a move for the computer player."""
        self._play_move(*self._current_player.move(self._board))

    def _handle_events(self) -> None:
        """Handles the game events."""
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self._running = False
            elif event.type == pg.MOUSEBUTTONUP:
                self._play_move(*self._get_move(event.pos))

    def _get_move(self, click_pos: tuple[float, float]) -> tuple[int, int]:
        """Returns the row and column of the move based on the click position."""
        x, y = click_pos
        row = int(y // (self._board.HEIGHT // 3))
        col = int(x // (self._board.WIDTH // 3))
        return (row, col)

    def _play_move(self, row: int, col: int) -> None:
        """Plays a move on the board."""
        if not (0 <= row <= 2 and 0 <= col <= 2):
            return
        if not self._board.update(row, col, self._current_player.player):
            return

        self._turn += 1
        self._check_win(row, col)
        self._end_turn()

    def _check_win(self, row: int, col: int) -> None:
        """Checks if the current player has won the game."""
        board = self._board.board_2d
        if (
            self._check_row(board, row)
            or self.check_col(board, col)
            or self.check_diags(board, row, col)
        ):
            self._winner = self._current_player.win
            return

        self._check_draw()

    def _check_row(self, board: list[list[Players | None]], row: int) -> bool:
        """Checks if a row has all the same player's marks."""
        if not all(board[row][i] == self._current_player.player for i in range(3)):
            return False

        self._winning_line = ((0, row), (2, row))
        self._win_type = Wins.ROW
        return True

    def check_col(self, board: list[list[Players | None]], col: int) -> bool:
        """Checks if a column has all the same player's marks."""
        if not all(board[i][col] == self._current_player.player for i in range(3)):
            return False

        self._winning_line = ((col, 0), (col, 2))
        self._win_type = Wins.COL
        return True

    def check_diags(
        self, board: list[list[Players | None]], row: int, col: int
    ) -> bool:
        """Checks if a diagonal has all the same player's marks."""
        if row == col and all(
            board[i][i] == self._current_player.player for i in range(3)
        ):
            self._winning_line = ((0, 0), (2, 2))
            self._win_type = Wins.DIAG
            return True

        if row + col == 2 and all(
            board[i][2 - i] == self._current_player.player for i in range(3)
        ):
            self._winning_line = ((0, 2), (2, 0))
            self._win_type = Wins.DIAG_2
            return True

        return False

    def _check_draw(self) -> None:
        """Checks if the game is a draw."""
        if self._turn == 9:
            self._winner = States.DRAW

    def _end_turn(self) -> None:
        """Ends the current player's turn and switches to the next player."""
        if not self._winner:
            self._current_player = (
                self._O if self._current_player == self._X else self._X
            )
            self._board.draw_status(self._current_player.turn)
        else:
            self._end_game()

    def _end_game(self) -> None:
        """Ends the game and displays the winner."""
        self._board.draw_status(self._winner)  # type: ignore
        if self._winner != States.DRAW:
            self._board.draw_winning_line(*self._winning_line, self._win_type)  # type: ignore
        pg.display.update()
        pg.time.wait(1000)
        self._reset_game()

    def _reset_game(self) -> None:
        """Resets the game to the initial state."""
        self._current_player = self._X
        self._winner = None
        self._winning_line = None
        self._win_type = None
        self._turn = 0
        self._board.reset()
