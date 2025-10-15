import pygame as pg

from models import MODELS, NEURAL_NETWORKS, Models, NeuralNetworks
from utils import Players, States, Wins

from .bit_board import BitBoard
from .hints import Hints


class Board:
    """
    ### Represents the game board.

    #### Attributes:
    - `WIDTH (int)`: The width of the game board.
    - `HEIGHT (int)`: The height of the game board.
    - `OFFSET (int)`: The offset for player image positions.
    - `EXTENDED_HEIGHT (int)`: The height of the game board and status screen.
    - `CAPTION (str)`: The caption of the game window.
    - `SPLASH_IMG (str)`: The path to the splash image.
    - `X_IMG (str)`: The path to the X image.
    - `O_IMG (str)`: The path to the O image.

    #### Properties:
    - `flat_board (list[int])`: The flattened game array.
    - `board_2d (list[list[Players | None]])`: The game array.
    - `bit_board (BitBoard)`: The bit board representation.
    - `winner (Players | States | None)`: The winner of the game or game state.

    #### Methods:
    - `setup() -> None`: Sets up the game window and assets.
    - `draw_status(state: States) -> None`: Draws the status message for the game.
    - `update(row: int, col: int, player: Players) -> bool`: Updates the game board with the player's move.
    - `check_square(row: int, col: int) -> Players | None`: Checks if the square is empty.
    - `play_move(row: int, col: int, player: Players) -> bool`: Plays a move on the board.
    - `clear_move(row: int, col: int) -> bool`: Clears a move from the board.
    - `draw_winning_line(start: tuple[int, int], end: tuple[int, int], win_type: Wins) -> None`: Draws the winning line on the board when a player wins.
    - `reset() -> None`: Resets the game board.
    """

    WIDTH = 400
    HEIGHT = 400
    OFFSET = 30
    EXTENDED_HEIGHT = HEIGHT + 100
    CAPTION = "Tic Tac Toe"
    SPLASH_IMG = "assets/modified_cover.png"
    X_IMG = "assets/X_modified.png"
    O_IMG = "assets/O_modified.png"

    def __init__(self, hints: bool = False, flat_board: list[int] | None = None):
        self._hints = Hints(self.WIDTH, self.HEIGHT) if hints else None
        self._game_surface = pg.Surface((self.WIDTH, self.HEIGHT)) if hints else None

        if flat_board is None:
            self._board_2d: list[list[Players | None]] = [
                [None] * 3,
                [None] * 3,
                [None] * 3,
            ]
            self._flat_board = [0] * 9
            self._bit_board = BitBoard()
        else:
            self._board_2d = [
                [self._get_player(flat_board[i + j]) for j in range(3)]
                for i in range(0, 9, 3)
            ]
            self._flat_board = flat_board
            self._bit_board = BitBoard(flat_board)

    @property
    def flat_board(self) -> list[int]:
        """The flattened game array."""
        return self._flat_board

    @property
    def board_2d(self) -> list[list[Players | None]]:
        """The 2D representation of the game board."""
        return self._board_2d

    @property
    def bit_board(self) -> BitBoard:
        """The bit board representation."""
        return self._bit_board

    @property
    def winner(self) -> Players | States | None:
        """The winner of the game or game state."""
        return self._bit_board.check_win()

    def setup(self) -> None:
        """
        Sets up the game window and assets.
        """
        self._initiate_window()
        self._load_assets()
        self.reset()

    def draw_status(self, state: States) -> None:
        """
        Draws the status message for the game.

        Args:
            state (States): The current state of the game.
        """
        font = pg.font.Font(None, 30)
        text = font.render(state.value, True, (255, 255, 255))
        height = self.EXTENDED_HEIGHT - self.HEIGHT
        center = (self.WIDTH / 2, self.HEIGHT + height / 2)

        self._screen.fill((0, 0, 0), (0, self.HEIGHT, self.WIDTH, height))
        text_rect = text.get_rect(center=center)
        self._screen.blit(text, text_rect)

    def update(self, row: int, col: int, player: Players) -> bool:
        """
        Updates the game board with the player's move.

        Args:
            row (int): The row of the move.
            col (int): The column of the move.
            player (Players): The player making the move.

        Returns:
            bool: True if the move is valid, False otherwise.
        """
        if not self.play_move(row, col, player):
            return False

        if not self._hints or not self._game_surface:
            self._draw_move(row, col, player)
            return True

        self._draw_move(row, col, player, self._game_surface)
        self._screen.blit(self._game_surface, (0, 0))

        if self.winner is None:
            next_player = Players.X if player == Players.O else Players.O
            self._draw_hints(next_player)

        return True

    def check_square(self, row: int, col: int) -> Players | None:
        """
        Checks if the square is empty.

        Args:
            row (int): The row of the square.
            col (int): The column of the square.

        Returns:
            Players | None: The player occupying the square or None.
        """
        return self._board_2d[row][col]

    def play_move(self, row: int, col: int, player: Players) -> bool:
        """
        Plays a move on the board.

        Args:
            row (int): The row of the move.
            col (int): The column of the move.
            player (Players): The player making the move.

        Returns:
            bool: True if the move is valid, False otherwise.
        """
        if self.check_square(row, col) is not None:
            return False

        self._board_2d[row][col] = player
        self._flat_board[row * 3 + col] = player.value
        self._bit_board.move(row, col, player)
        return True

    def clear_move(self, row: int, col: int) -> bool:
        """
        Clears a move from the board.

        Args:
            row (int): The row of the move.
            col (int): The column of the move.

        Returns:
            bool: True the move was cleared, False otherwise.
        """
        if self.check_square(row, col) is None:
            return False

        self._board_2d[row][col] = None
        self._flat_board[row * 3 + col] = 0
        self._bit_board.clear_move(row, col)
        return True

    def draw_winning_line(
        self, start: tuple[int, int], end: tuple[int, int], win_type: Wins
    ) -> None:
        """
        Draws the winning line on the board when a player wins.

        Args:
            start (tuple[int, int]): The starting position of the winning line.
            end (tuple[int, int]): The ending position of the winning line.
            win_type (Wins): The type of the winning line.
        """
        x_margin = self.WIDTH / 12
        y_margin = self.HEIGHT / 12
        x_center = self.WIDTH / 6
        y_center = self.HEIGHT / 6
        width = 4
        color = (255, 0, 0)

        if win_type == Wins.DIAG_2:
            start_coords = (
                start[0] + x_margin,
                (start[1] + 1) * self.WIDTH / 3 - y_margin,
            )
            end_coords = ((end[0] + 1) * self.WIDTH / 3 - x_margin, end[1] + y_margin)
        else:
            start_x = start[0] * self.WIDTH / 3 + (
                x_center if win_type == Wins.COL else x_margin
            )
            start_y = start[1] * self.WIDTH / 3 + (
                y_center if win_type == Wins.ROW else y_margin
            )
            end_x = (end[0] + 1) * self.WIDTH / 3 - (
                x_center if win_type == Wins.COL else x_margin
            )
            end_y = (end[1] + 1) * self.WIDTH / 3 - (
                y_center if win_type == Wins.ROW else y_margin
            )
            start_coords = (start_x, start_y)
            end_coords = (end_x, end_y)

        pg.draw.line(self._screen, color, start_coords, end_coords, width)

    def reset(self) -> None:
        """
        Resets the game board.
        """
        self._board_2d = [[None] * 3, [None] * 3, [None] * 3]
        self._flat_board = [0] * 9
        self._bit_board.clear()
        self._draw_splash()
        self._draw_board()
        if self._hints:
            self._draw_board(self._game_surface)
            self._draw_hints(Players.X)
        self.draw_status(States.X_TURN)

    def _initiate_window(self) -> None:
        """Initiates the window for the game."""
        self._screen = pg.display.set_mode((self.WIDTH, self.EXTENDED_HEIGHT), depth=32)
        pg.display.set_caption(self.CAPTION)

    def _load_assets(self) -> None:
        """Loads the assets for the game."""
        self._splash = pg.image.load(self.SPLASH_IMG)
        self._x = pg.image.load(self.X_IMG)
        self._o = pg.image.load(self.O_IMG)

        self._splash = pg.transform.scale(
            self._splash, (self.WIDTH, self.EXTENDED_HEIGHT)
        )
        self._x = pg.transform.scale(self._x, (80, 80))
        self._o = pg.transform.scale(self._o, (80, 80))

    def _draw_splash(self) -> None:
        """Draws the splash screen."""
        self._screen.blit(self._splash, (0, 0))
        pg.display.update()

    def _draw_board(self, target_screen: pg.Surface | None = None) -> None:
        """Draws the game board."""
        target_screen = target_screen if target_screen else self._screen
        line_color = (10, 10, 10)
        line_width = 7

        target_screen.fill((255, 255, 255))
        for i in range(1, 3):
            # Draw vertical lines
            pg.draw.line(
                target_screen,
                line_color,
                (self.WIDTH / 3 * i, 0),
                (self.WIDTH / 3 * i, self.HEIGHT),
                line_width,
            )

            # Draw horizontal lines
            pg.draw.line(
                target_screen,
                line_color,
                (0, self.HEIGHT / 3 * i),
                (self.WIDTH, self.HEIGHT / 3 * i),
                line_width,
            )

    def _draw_move(
        self,
        row: int,
        col: int,
        player: Players,
        target_screen: pg.Surface | None = None,
    ) -> None:
        """Draws the player's move on the board."""
        target_screen = target_screen if target_screen else self._screen
        pos_x = col * self.WIDTH / 3 + self.OFFSET
        pos_y = row * self.HEIGHT / 3 + self.OFFSET
        if player == Players.X:
            target_screen.blit(self._x, (pos_x, pos_y))
        elif player == Players.O:
            target_screen.blit(self._o, (pos_x, pos_y))

    def _draw_hints(self, player: Players) -> None:
        """Draws move hints on the board."""
        if not self._hints:
            return

        best_move = MODELS[Models.IMPOSSIBLE](self, player)
        move_probabilities = NEURAL_NETWORKS[NeuralNetworks.MLP](self, True)
        self._hints.draw_hints(best_move, move_probabilities)  # type: ignore
        self._screen.blit(self._hints.surface, (0, 0))

    def _get_player(self, num: int) -> Players | None:
        """Gets the player from the number representation."""
        if num == Players.X.value:
            return Players.X
        elif num == Players.O.value:
            return Players.O
        else:
            return None

    def __str__(self) -> str:
        board_2d_str = "2D Board:\n" + "\n".join(map(str, self._board_2d))
        flat_board_str = f"Flat Board:\n{self._flat_board}"
        return f"{board_2d_str}\n\n{flat_board_str}"
