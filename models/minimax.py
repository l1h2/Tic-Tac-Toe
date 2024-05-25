import numpy as np

from config import GameBoard, Players, States


def minimax_algo(
    board: GameBoard,
    player: Players,
    opponent: Players,
    current_player: Players,
    depth: int,
    scores: dict[Players | States, int],
    alpha: int,
    beta: int,
) -> int | tuple[int, int]:
    """
    Returns the best score or the best move for the current player using the minimax algorithm.

    Args:
        board (GameBoard): The current game board.
        player (Players): The maximizing player.
        opponent (Players): The minimizing player.
        current_player (Players): The current player.
        depth (int): The current depth of the search.
        scores (dict[Players  |  States, int]): The scores for each player and state.
        alpha (int): The alpha value.
        beta (int): The beta value.

    Returns:
        int | tuple[int, int]: The best score or the best move.
    """
    winner = check_win(board)
    if winner is not None:
        return scores[winner] - depth

    if current_player == player:
        best_score = -np.inf
        next_player = opponent
    else:
        best_score = np.inf
        next_player = player

    for i in range(0, 3):
        for j in range(0, 3):
            if board[i][j] is not None:
                continue

            board[i][j] = current_player
            score = minimax_algo(
                board,
                player,
                opponent,
                next_player,
                depth + 1,
                scores,
                alpha,
                beta,
            )
            board[i][j] = None

            if depth > 0:
                if current_player == player:
                    best_score = max(score, best_score)
                    alpha = max(alpha, score)
                else:
                    best_score = min(score, best_score)
                    beta = max(beta, score)

            if beta <= alpha:
                break

            if score > best_score and depth == 0:
                best_score = score
                move = (i, j)
        if beta <= alpha:
            break

    return move if depth == 0 else best_score


def check_win(board: GameBoard) -> Players | States | None:
    """
    Checks if there is a winner or a draw.

    Args:
        board (GameBoard): The current game board.

    Returns:
        Players | States | None: The winner or None if there is no winner.
    """
    for i in range(3):
        # Check rows
        if board[i][0] is not None and board[i][0] == board[i][1] == board[i][2]:
            return board[i][0]
        # Check columns
        if board[0][i] is not None and board[0][i] == board[1][i] == board[2][i]:
            return board[0][i]

    # Check diagonals
    if board[0][0] is not None and board[0][0] == board[1][1] == board[2][2]:
        return board[0][0]
    if board[0][2] is not None and board[0][2] == board[1][1] == board[2][0]:
        return board[0][2]

    # Check for draw
    if all(board[i][j] is not None for i in range(3) for j in range(3)):
        return States.DRAW

    return None
