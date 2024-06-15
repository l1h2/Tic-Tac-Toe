import pygame as pg

from models import MODELS, NEURAL_NETWORKS, Models, NeuralNetworks
from utils import Players, States, Wins


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
    - `hints (Hints | None)`: The move hints object.
    - `board_2d (list[list[Players | None]])`: The game array.
    - `flat_board (list[int])`: The flattened game array.
    - `bit_board (BitBoard)`: The bit board representation.
    - `screen (pg.Surface)`: The game window.
    - `splash (pg.Surface)`: The splash image.
    - `X (pg.Surface)`: The X image.
    - `O (pg.Surface)`: The O image.

    #### Properties:
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
        self.hints = Hints(self.WIDTH, self.HEIGHT) if hints else None
        self.__game_surface = pg.Surface((self.WIDTH, self.HEIGHT)) if hints else None
        if flat_board is None:
            self.board_2d = [[None] * 3, [None] * 3, [None] * 3]
            self.flat_board = [0] * 9
            self.bit_board = BitBoard()
        else:
            self.board_2d = [
                [self.__get_player(flat_board[i + j]) for j in range(3)]
                for i in range(0, 9, 3)
            ]
            self.flat_board = flat_board
            self.bit_board = BitBoard(flat_board)

    @property
    def winner(self) -> Players | States | None:
        """
        Players | States | None: The winner of the game or game state.
        """
        return self.bit_board.check_win()

    def setup(self) -> None:
        """
        Sets up the game window and assets.
        """
        self.__initiate_window()
        self.__load_assets()
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
        if not self.play_move(row, col, player):
            return False

        if not self.hints:
            self.__draw_move(row, col, player)
            return True

        self.__draw_move(row, col, player, self.__game_surface)
        self.screen.blit(self.__game_surface, (0, 0))
        if self.winner is None:
            next_player = Players.X if player == Players.O else Players.O
            self.__draw_hints(next_player)
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
        return self.board_2d[row][col]

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

        self.board_2d[row][col] = player
        self.flat_board[row * 3 + col] = player.value
        self.bit_board.move(row, col, player)
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

        self.board_2d[row][col] = None
        self.flat_board[row * 3 + col] = 0
        self.bit_board.clear_move(row, col)
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
        self.board_2d = [[None] * 3, [None] * 3, [None] * 3]
        self.flat_board = [0] * 9
        self.bit_board.clear()
        self.__draw_splash()
        self.__draw_board()
        if self.hints:
            self.__draw_board(self.__game_surface)
            self.__draw_hints(Players.X)
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

    def __draw_splash(self) -> None:
        """
        Draws the splash screen.
        """
        self.screen.blit(self.splash, (0, 0))
        pg.display.update()

    def __draw_board(self, target_screen: pg.Surface | None = None) -> None:
        """
        Draws the game board.

        Args:
            target_screen (pg.Surface): The target screen to draw on. If None, the main screen is used.
        """
        target_screen = target_screen if target_screen else self.screen
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

    def __draw_move(
        self,
        row: int,
        col: int,
        player: Players,
        target_screen: pg.Surface | None = None,
    ) -> None:
        """
        Draws the player's move on the board.

        Args:
            row (int): The row of the move.
            col (int): The column of the move.
            player (Players): The player making the move.
            target_screen (pg.Surface): The target screen to draw on. If None, the main screen is used.
        """
        target_screen = target_screen if target_screen else self.screen
        pos_x = col * self.WIDTH / 3 + self.OFFSET
        pos_y = row * self.HEIGHT / 3 + self.OFFSET
        if player == Players.X:
            target_screen.blit(self.X, (pos_x, pos_y))
        elif player == Players.O:
            target_screen.blit(self.O, (pos_x, pos_y))

    def __draw_hints(self, player: Players) -> None:
        """
        Draws move hints on the board.

        Args:
            player (Players): The current player.
        """
        best_move = MODELS[Models.IMPOSSIBLE](self, player)
        move_probabilities = NEURAL_NETWORKS[NeuralNetworks.MLP](self, True)
        self.hints.draw_hints(best_move, move_probabilities)
        self.screen.blit(self.hints.surface, (0, 0))

    def __get_player(self, num: int) -> Players:
        """
        Gets the player from the number representation.

        Args:
            num (int): The player number.

        Returns:
            Players: The player.
        """
        if num == Players.X.value:
            return Players.X
        elif num == Players.O.value:
            return Players.O
        else:
            return None

    def __str__(self) -> str:
        board_2d_str = "2D Board:\n" + "\n".join(map(str, self.board_2d))
        flat_board_str = f"Flat Board:\n{self.flat_board}"
        return f"{board_2d_str}\n\n{flat_board_str}"


class BitBoard:
    """
    ### Represents the game state using bit boards.

    #### Attributes:
    - `X_bit_board (int)`: The bit board for player X.
    - `O_bit_board (int)`: The bit board for player O.
    - `WINNING_STATES (tuple[int])`: The winning states for the game.

    #### Methods:
    - `check_move(row: int, col: int) -> bool`: Checks if a move is valid.
    - `move(row: int, col: int, player: Players) -> None`: Sets a move on the bit boards.
    - `clear_move(row: int, col: int) -> None`: Clears a move from the bit boards.
    - `clear() -> None`: Clears the bit boards.
    - `check_win() -> Players | States | None`: Checks if a player has won the game.
    """

    WINNING_STATES = (
        [0b111 << (i * 3) for i in range(3)]  # Rows
        + [0b001001001 << i for i in range(3)]  # Columns
        + [0b100010001, 0b001010100]  # Diagonals
    )

    def __init__(self, flat_board: list[int] | None = None):
        self.X_bit_board = 0
        self.O_bit_board = 0
        if flat_board:
            self.__get_board_from_list(flat_board)

    def check_move(self, row: int, col: int) -> bool:
        """
        Checks if a move is valid.

        Args:
            row (int): The row of the move.
            col (int): The column of the move.

        Returns:
            bool: True if the move is valid, False otherwise.
        """
        shift = row * 3 + col
        return not ((self.X_bit_board | self.O_bit_board) & (1 << shift))

    def move(self, row: int, col: int, player: Players) -> None:
        """
        Sets a move on the bit boards.

        Args:
            row (int): The row of the move.
            col (int): The column of the move.
            player (Players): The player making the move.
        """
        shift = row * 3 + col
        if player == Players.X:
            self.X_bit_board |= 1 << shift
        else:
            self.O_bit_board |= 1 << shift

    def clear_move(self, row: int, col: int) -> None:
        """
        Clears a move from the bit boards.

        Args:
            row (int): The row of the move.
            col (int): The column of the move.
        """
        shift = row * 3 + col
        self.X_bit_board &= ~(1 << shift)
        self.O_bit_board &= ~(1 << shift)

    def clear(self) -> None:
        """
        Clears the bit boards.
        """
        self.X_bit_board = 0
        self.O_bit_board = 0

    def check_win(self) -> Players | States | None:
        """
        Checks if a player has won the game.

        Returns:
            Players | States | None: The winning player or state.
        """
        for condition in self.WINNING_STATES:
            if self.X_bit_board & condition == condition:
                return Players.X
            if self.O_bit_board & condition == condition:
                return Players.O

        if self.X_bit_board | self.O_bit_board == 0b111111111:
            return States.DRAW

        return None

    def __get_board_from_list(self, flat_board: list[int]) -> None:
        """
        Sets the bit boards from a list representation.

        Args:
            flat_board (list[int]): The flat board representation.
        """
        for i, player in enumerate(flat_board):
            if player == 1:
                self.X_bit_board |= 1 << i
            elif player == -1:
                self.O_bit_board |= 1 << i


class Hints:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.surface = pg.Surface((width, height), pg.SRCALPHA)
        self.__clear_hints()

    def draw_hints(
        self, best_move: tuple[int, int], move_probabilities: list[float]
    ) -> None:
        """
        Draws move hints on the board.

        Args:
            best_move (tuple[int, int]): The best move for the current player.
            move_probabilities (list[float]): The probabilities for each move.
        """
        self.__clear_hints()
        self.__draw_best_move_hint(best_move)
        self.__draw_move_probabilities(move_probabilities)

    def __clear_hints(self) -> None:
        """
        Clears all hints from the board.
        """
        self.surface.fill((0, 0, 0, 0))

    def __draw_best_move_hint(self, best_move: tuple[int, int]) -> None:
        """
        Draws the best move hint on the board.

        Args:
            best_move (tuple[int, int]): The best move for the current player.
        """
        pos_x = best_move[1] * self.width / 3
        pos_y = best_move[0] * self.height / 3

        shape = (pos_x, pos_y, self.width / 3, self.height / 3)
        color = (0, 255, 0)
        line_width = 4

        pg.draw.rect(
            self.surface,
            color,
            shape,
            line_width,
        )

    def __draw_move_probabilities(self, move_probabilities: list[float]) -> None:
        """
        Draws the move probabilities on the board.

        Args:
            move_probabilities (list[float]): The probabilities for each move.
        """
        font = pg.font.Font(None, 14)
        x_offset = self.width / 3 - 30
        y_offset = 10

        for i in range(3):
            for j in range(3):
                prob = move_probabilities[i * 3 + j] * 100
                text = font.render(f"{prob:.0f}%", True, (0, 0, 0))

                pos_x = j * self.width / 3 + x_offset
                pos_y = i * self.height / 3 + y_offset

                self.surface.blit(text, (pos_x, pos_y))
