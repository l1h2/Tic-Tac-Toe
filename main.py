import pygame as pg
import sys
import time
import numpy as np
from pygame.locals import *


def minimax(board, ai, player, depth, alpha, beta, winner, screen, width, height):
    turn = (depth % 2)
    scores = {
        player: -10,
        ai: 10,
        'Tie': 0
    }

    result = check_win('Test', board, winner, screen, width, height)
    if result is not None:
        return scores[result] - depth

    if turn == 0:
        best_score = -np.inf
        current_user = ai
    else:
        best_score = np.inf
        current_user = player

    for i in range(0, 3):
        for j in range(0, 3):
            if board[i][j] is None:
                board[i][j] = current_user
                score = minimax(board, ai, player, depth + 1, alpha, beta, winner, screen, width, height)
                board[i][j] = None

                if turn == 0 and depth > 0:
                    best_score = max(score, best_score)
                    alpha = max(alpha, score)

                elif depth > 0:
                    best_score = min(score, best_score)
                    beta = max(beta, score)

                if beta <= alpha:
                    break

                if score > best_score and depth == 0:
                    best_score = score
                    move = [i + 1, j + 1]

    if depth == 0:
        return move
    else:
        return best_score


def ai_move(board, ai, player, winner, screen, width, height):
    time.sleep(0.5)
    move = minimax(board, ai, player, 0, -np.inf, np.inf, winner, screen, width, height)

    return move


def check_win(input_type, board, winner, screen, width, height):
    # checking for winning rows
    for row in range(0, 3):
        if (board[row][0] == board[row][1] == board[row][2]) and (board[row][0] is not None):
            winner = board[row][0]
            if input_type == 'Move':
                pg.draw.line(screen, (250, 0, 0),
                             (0, (row + 1) * height / 3 - height / 6),
                             (width, (row + 1) * height / 3 - height / 6), 4)
            break
    # checking for winning columns
    for col in range(0, 3):
        if (board[0][col] == board[1][col] == board[2][col]) and (board[0][col] is not None):
            winner = board[0][col]
            if input_type == 'Move':
                pg.draw.line(screen, (250, 0, 0),
                             ((col + 1) * width / 3 - width / 6, 0),
                             ((col + 1) * width / 3 - width / 6, height), 4)
            break
    # check for diagonal winners
    if (board[0][0] == board[1][1] == board[2][2]) and (board[0][0] is not None):
        # game won diagonally left to right
        winner = board[0][0]
        if input_type == 'Move':
            pg.draw.line(screen, (250, 70, 70), (50, 50), (350, 350), 4)

    if (board[0][2] == board[1][1] == board[2][0]) and (board[0][2] is not None):
        # game won diagonally right to left
        winner = board[0][2]
        if input_type == 'Move':
            pg.draw.line(screen, (250, 70, 70), (350, 50), (50, 350), 4)

    # checks for draws
    if all([all(row) for row in board]) and winner is None:
        winner = 'Tie'

    return winner


def draw_xo(row, col, board, current_user, screen, x_img, o_img, width, height):

    if row == 1:
        posx = 30
    if row == 2:
        posx = width / 3 + 30
    if row == 3:
        posx = width / 3 * 2 + 30

    if col == 1:
        posy = 30
    if col == 2:
        posy = height / 3 + 30
    if col == 3:
        posy = height / 3 * 2 + 30

    board[row - 1][col - 1] = current_user

    if current_user == 'X':
        screen.blit(x_img, (posy, posx))
        current_user = 'O'

    else:
        screen.blit(o_img, (posy, posx))
        current_user = 'X'

    pg.display.update()
    return [current_user, board]


def play_turn(coord, board, current_user, winner, screen, x_img, o_img, width, height):
    current_user, board = draw_xo(coord[0], coord[1], board, current_user, screen, x_img, o_img, width, height)
    winner = check_win('Move', board, winner, screen, width, height)
    draw_status(winner, current_user, screen, width)

    return [current_user, board, winner]


def user_click(pos, width, height):
    x, y = pos

    if x < width / 3:
        col = 1
    elif x < width / 3 * 2:
        col = 2
    elif x < width:
        col = 3
    else:
        col = None

    if y < height / 3:
        row = 1
    elif y < height / 3 * 2:
        row = 2
    elif y < height:
        row = 3
    else:
        row = None

    return [row, col]


def draw_status(winner, current_user, screen, width):
    if winner is None:
        message = current_user + "'s Turn"
    elif winner == 'Tie':
        message = "Game Draw !"
    else:
        message = winner + " won !"

    font = pg.font.Font(None, 30)
    text = font.render(message, True, (255, 255, 255))

    screen.fill((0, 0, 0), (0, 400, 500, 100))
    text_rect = text.get_rect(center=(width / 2, 500 - 50))
    screen.blit(text, text_rect)
    pg.display.update()


def game_initiating_window(width, height, screen, initiating_window):
    line_color = (10, 10, 10)

    screen.blit(initiating_window, (0, 0))
    pg.display.update()
    time.sleep(1)
    screen.fill((255, 255, 255))

    pg.draw.line(screen, line_color, (width / 3, 0), (width / 3, height), 7)
    pg.draw.line(screen, line_color, (width / 3 * 2, 0), (width / 3 * 2, height), 7)
    pg.draw.line(screen, line_color, (0, height / 3), (width, height / 3), 7)
    pg.draw.line(screen, line_color, (0, height / 3 * 2), (width, height / 3 * 2), 7)


def main():
    current_user = 'X'
    ai = 'O'
    player = 'X'
    winner = None
    board = [[None] * 3, [None] * 3, [None] * 3]

    width = 400
    height = 400

    pg.init()

    fps = 30
    clock = pg.time.Clock()
    screen = pg.display.set_mode((width, height + 100), 0, 32)
    pg.display.set_caption("Tic Tac Toe")

    initiating_window = pg.image.load("assets/modified_cover.png")
    x_img = pg.image.load("assets/X_modified.png")
    o_img = pg.image.load("assets/O_modified.png")

    initiating_window = pg.transform.scale(initiating_window, (width, height + 100))
    x_img = pg.transform.scale(x_img, (80, 80))
    o_img = pg.transform.scale(o_img, (80, 80))

    game_initiating_window(width, height, screen, initiating_window)
    draw_status(winner, current_user, screen, width)

    while True:
        if current_user == ai and winner is None:
            move = ai_move(board, ai, player, winner, screen, width, height)
            current_user, board, winner = play_turn(move, board, current_user, winner, screen,
                                                    x_img, o_img, width, height)
        if winner:
            time.sleep(1)
            current_user = 'X'
            game_initiating_window(width, height, screen, initiating_window)
            winner = None
            board = [[None] * 3, [None] * 3, [None] * 3]
            draw_status(winner, current_user, screen, width)

        for event in pg.event.get():

            if event.type == QUIT:
                pg.quit()
                sys.exit()

            elif event.type == MOUSEBUTTONUP:
                row, col = user_click(pg.mouse.get_pos(), width, height)

                if row and col and board[row - 1][col - 1] is None:
                    current_user, board, winner = play_turn([row, col], board, current_user, winner, screen,
                                                            x_img, o_img, width, height)

        pg.display.update()
        clock.tick(fps)


main()
