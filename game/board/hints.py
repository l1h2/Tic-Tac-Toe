import pygame as pg


class Hints:
    def __init__(self, width: int, height: int):
        self._width = width
        self._height = height
        self._surface = pg.Surface((width, height), pg.SRCALPHA)
        self._clear_hints()

    @property
    def surface(self) -> pg.Surface:
        """The surface containing the hints."""
        return self._surface

    def draw_hints(
        self, best_move: tuple[int, int], move_probabilities: list[float]
    ) -> None:
        """
        Draws move hints on the board.

        Args:
            best_move (tuple[int, int]): The best move for the current player.
            move_probabilities (list[float]): The probabilities for each move.
        """
        self._clear_hints()
        self._draw_best_move_hint(best_move)
        self._draw_move_probabilities(move_probabilities)

    def _clear_hints(self) -> None:
        """Clears all hints from the board."""
        self._surface.fill((0, 0, 0, 0))

    def _draw_best_move_hint(self, best_move: tuple[int, int]) -> None:
        """Draws the best move hint on the board."""
        pos_x = best_move[1] * self._width / 3
        pos_y = best_move[0] * self._height / 3

        shape = (pos_x, pos_y, self._width / 3, self._height / 3)
        color = (0, 255, 0)
        line_width = 4

        pg.draw.rect(
            self._surface,
            color,
            shape,
            line_width,
        )

    def _draw_move_probabilities(self, move_probabilities: list[float]) -> None:
        """Draws the move probabilities on the board."""
        font = pg.font.Font(None, 14)
        x_offset = self._width / 3 - 30
        y_offset = 10

        for i in range(3):
            for j in range(3):
                prob = move_probabilities[i * 3 + j] * 100
                text = font.render(f"{prob:.0f}%", True, (0, 0, 0))

                pos_x = j * self._width / 3 + x_offset
                pos_y = i * self._height / 3 + y_offset

                self._surface.blit(text, (pos_x, pos_y))
