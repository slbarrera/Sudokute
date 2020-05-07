import pygame
import numpy as np
import random

def create_board():
    board = np.zeros((9, 9))
    board = board.tolist()

    rand_i = random.randint(0, 8)
    rand_j = random.randint(0, 8)
    rand_num = random.randint(1, 10)

base  = 3
side  = base*base

# pattern for a baseline valid solution
def pattern(r,c): return (base*(r%base)+r//base+c)%side

# randomize rows, columns and numbers (of valid base pattern)
from random import sample
def shuffle(s): return sample(s,len(s))
rBase = range(base)
rows  = [ g*base + r for g in shuffle(rBase) for r in shuffle(rBase) ]
cols  = [ g*base + c for g in shuffle(rBase) for c in shuffle(rBase) ]
nums  = shuffle(range(1,base*base+1))

# produce board using randomized baseline pattern
board = [ [nums[pattern(r,c)] for c in cols] for r in rows ]

squares = side*side
empties = squares * 3//4
for p in sample(range(squares),empties):
    board[p//side][p%side] = 0

numSize = len(str(side))
for line in board: print("["+"  ".join(f"{n or '.':{numSize}}" for n in line)+"]")


def solve_board(board):
    empty_space = find_empty(board)

    if not empty_space:
        return True
    else:
        row, col = empty_space

    for num in range(1, 10):
        if check_valid(board, num, empty_space):
            board[row][col] = num

            if solve_board(board):
                return True

            board[row][col] = 0

    return False


def find_empty(board):
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == 0:
                return (i, j)
    return None


def check_valid(board, num, position):
    return check_col(board, num, position) and check_row(board, num, position) \
           and check_square(board, num, position)


def check_row(board, num, position):
    for j in range(len(board[0])):
        if (board[position[0]][j] == num) and (j != position[1]):
            return False
    return True


def check_col(board, num, position):
    for i in range(len(board)):
        if (board[i][position[1]] == num) and (i != position[0]):
            return False
    return True


def check_square(board, num, position):
    square_x = (position[1] // 3) * 3
    square_y = (position[0] // 3) * 3

    for i in range(square_y, square_y + 3):
        for j in range(square_x, square_x + 3):
            if (board[i][j] == num) and ((i, j) != position):
                return False
    return True


def print_board(board):
    for i in range(len(board)):
        if ((i % 3) == 0) and (i != 0):
            print("- - - - - - - - - - - - - - -")
        for j in range(len(board[0])):
            if ((j % 3) == 0) and (j != 0):
                print(" | ", end="")
            if j == 8:
                print(board[i][j])
            else:
                print(str(board[i][j]) + " ", end="")

