from utils import Players, States


class BitBoard:
    """
    ### Represents the game state using bit boards.

    #### Attributes:
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
        self._X_bit_board = 0
        self._O_bit_board = 0
        if flat_board:
            self._get_board_from_list(flat_board)

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
        return not ((self._X_bit_board | self._O_bit_board) & (1 << shift))

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
            self._X_bit_board |= 1 << shift
        else:
            self._O_bit_board |= 1 << shift

    def clear_move(self, row: int, col: int) -> None:
        """
        Clears a move from the bit boards.

        Args:
            row (int): The row of the move.
            col (int): The column of the move.
        """
        shift = row * 3 + col
        self._X_bit_board &= ~(1 << shift)
        self._O_bit_board &= ~(1 << shift)

    def clear(self) -> None:
        """
        Clears the bit boards.
        """
        self._X_bit_board = 0
        self._O_bit_board = 0

    def check_win(self) -> Players | States | None:
        """
        Checks if a player has won the game.

        Returns:
            Players | States | None: The winning player or state.
        """
        for condition in self.WINNING_STATES:
            if self._X_bit_board & condition == condition:
                return Players.X
            if self._O_bit_board & condition == condition:
                return Players.O

        if self._X_bit_board | self._O_bit_board == 0b111111111:
            return States.DRAW

        return None

    def _get_board_from_list(self, flat_board: list[int]) -> None:
        """
        Sets the bit boards from a list representation.

        Args:
            flat_board (list[int]): The flat board representation.
        """
        for i, player in enumerate(flat_board):
            if player == 1:
                self._X_bit_board |= 1 << i
            elif player == -1:
                self._O_bit_board |= 1 << i
