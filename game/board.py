import pygame as pg

from config import Players, States, Wins


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
    - `board (list[list[Players | None]])`: The game array.
    - `screen (pg.Surface)`: The game window.
    - `splash (pg.Surface)`: The splash image.
    - `X (pg.Surface)`: The X image.
    - `O (pg.Surface)`: The O image.

    #### Methods:
    - `setup() -> None`: Sets up the game window and assets.
    - `draw_board() -> None`: Draws the game board.
    - `draw_status(state: States) -> None`: Draws the status message for the game.
    - `update(row: int, col: int, player: Players) -> bool`: Updates the game board with the player's move.
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

    def __init__(self) -> None:
        self.board = [[None] * 3, [None] * 3, [None] * 3]

    def setup(self) -> None:
        """
        Sets up the game window and assets.
        """
        self.__initiate_window()
        self.__load_assets()

    def draw_board(self) -> None:
        """
        Draws the game board.
        """
        line_color = (10, 10, 10)
        line_width = 7

        self.screen.blit(self.splash, (0, 0))
        pg.display.update()
        pg.time.wait(1000)

        self.screen.fill((255, 255, 255))
        # Draw vertical lines
        for i in range(1, 3):
            pg.draw.line(
                self.screen,
                line_color,
                (self.WIDTH / 3 * i, 0),
                (self.WIDTH / 3 * i, self.HEIGHT),
                line_width,
            )
        # Draw horizontal lines
        for i in range(1, 3):
            pg.draw.line(
                self.screen,
                line_color,
                (0, self.HEIGHT / 3 * i),
                (self.WIDTH, self.HEIGHT / 3 * i),
                line_width,
            )

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

        self.screen.fill((0, 0, 0), (0, self.HEIGHT, self.WIDTH, height))
        text_rect = text.get_rect(center=center)
        self.screen.blit(text, text_rect)

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
        if self.board[row][col] is not None:
            return False

        self.board[row][col] = player
        self.__draw_move(row, col, player)
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
            start = (start[0] + x_margin, (start[1] + 1) * self.WIDTH / 3 - y_margin)
            end = ((end[0] + 1) * self.WIDTH / 3 - x_margin, end[1] + y_margin)
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
            start = (start_x, start_y)
            end = (end_x, end_y)

        pg.draw.line(self.screen, color, start, end, width)

    def reset(self) -> None:
        """
        Resets the game board.
        """
        self.board = [[None] * 3, [None] * 3, [None] * 3]
        self.draw_board()
        self.draw_status(States.X_TURN)

    def __initiate_window(self) -> None:
        """
        Initiates the window for the game.
        """
        self.screen = pg.display.set_mode((self.WIDTH, self.EXTENDED_HEIGHT), depth=32)
        pg.display.set_caption(self.CAPTION)

    def __load_assets(self) -> None:
        """
        Loads the assets for the game.
        """
        self.splash = pg.image.load(self.SPLASH_IMG)
        self.X = pg.image.load(self.X_IMG)
        self.O = pg.image.load(self.O_IMG)

        self.splash = pg.transform.scale(
            self.splash, (self.WIDTH, self.EXTENDED_HEIGHT)
        )
        self.X = pg.transform.scale(self.X, (80, 80))
        self.O = pg.transform.scale(self.O, (80, 80))

    def __draw_move(self, row: int, col: int, player: Players) -> None:
        """
        Draws the player's move on the board.

        Args:
            row (int): The row of the move.
            col (int): The column of the move.
            player (Players): The player making the move.
        """
        pos_x = col * self.WIDTH / 3 + self.OFFSET
        pos_y = row * self.HEIGHT / 3 + self.OFFSET
        if player == Players.X:
            self.screen.blit(self.X, (pos_x, pos_y))
        elif player == Players.O:
            self.screen.blit(self.O, (pos_x, pos_y))
