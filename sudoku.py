import numpy
import random


def generate_filled_puzzle(puzzle):
    """
    :param puzzle - 2D array of a sudoku puzzle:
    :return boolean - boolean indicating if puzzle is solvable:
    """

    # Finds the first instance of an empty space in the puzzle
    empty_space = find_empty(puzzle)

    if not empty_space:
        return True
    else:
        row, col = empty_space

    # Goes though all possible numbers 1-9 and checks to see if it works
    # in that spot
    shuffled_numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    random.shuffle(shuffled_numbers)
    for num in shuffled_numbers:
        if check_valid(puzzle, num, empty_space):
            puzzle[row][col] = num

            # Recursive call to check the next empty spot in the puzzle
            if generate_filled_puzzle(puzzle):
                return True

            # if the guess does not work, we backtrack to last number
            puzzle[row][col] = 0
    return False


def solve_puzzle(puzzle):
    """
    :param puzzle - 2D array of a sudoku puzzle:
    :return boolean - boolean indicating if puzzle is solvable:
    """

    # Finds the first instance of an empty space in the puzzle
    empty_space = find_empty(puzzle)
    # print("1")

    if not empty_space:
        # print("2")
        return True
    else:
        # print("3")
        row, col = empty_space

    # Goes though all possible numbers 1-9 and checks to see if it works
    # in that spot
    for num in range(1, 10):
        # print("4")
        if check_valid(puzzle, num, empty_space):
            # print("5")
            puzzle[row][col] = num

            # Recursive call to check the next empty spot in the puzzle
            if solve_puzzle(puzzle):
                # print("6")
                return True

            # if the guess does not work, we backtrack to last number
            # print("7")
            puzzle[row][col] = 0
    # print("8")
    return False


def find_empty(puzzle):
    """
    :param puzzle - 2D array of a sudoku puzzle:
    :return tuple - the location of the first empty spot in the given puzzle:
    """
    for i in range(len(puzzle)):
        for j in range(len(puzzle[0])):
            if puzzle[i][j] == 0:
                return i, j
    return None


def check_valid(puzzle, num, position):
    """
    :param puzzle - 2D array of a sudoku puzzle:
    :param num - a number 1-9 that is the current guess at given position:
    :param position - a tuple of the current empty space being checked:
    :return boolean - :
    """
    # calls helper functions and returns True if num works in given position
    return check_col(puzzle, num, position) and \
           check_row(puzzle, num, position) and \
           check_square(puzzle, num, position)


def check_row(puzzle, num, position):
    """
     :param num:
     :param puzzle - 2D array of a sudoku puzzle:
     :param num - a number 1-9 that is the current guess at given position:
     :param position - a tuple of the current empty block:
     :return boolean - returns True if num is valid in the given position:
     """

    # Checks to see if num is already in the given row
    for j in range(len(puzzle[0])):
        if (puzzle[position[0]][j] == num) and (j != position[1]):
            return False
    return True


def check_col(puzzle, num, position):
    """
     :param puzzle - 2D array of a sudoku puzzle:
     :param num - a number 1-9 that is the current guess at given position:
     :param position - a tuple of the current empty block:
     :return boolean - returns True if num is valid in the given position:
     """

    # Checks to see if num is already in the given column
    for i in range(len(puzzle)):
        if (puzzle[i][position[1]] == num) and (i != position[0]):
            return False
    return True


def check_square(puzzle, num, position):
    """
     :param puzzle - 2D array of a sudoku puzzle:
     :param num - a number 1-9 that is the current guess at given position:
     :param position - a tuple of the current empty block:
     :return boolean - returns True if num is valid in the given position:
     """

    # Checks to see if num is already in the given square
    square_x = (position[1] // 3) * 3
    square_y = (position[0] // 3) * 3

    for i in range(square_y, square_y + 3):
        for j in range(square_x, square_x + 3):
            if (puzzle[i][j] == num) and ((i, j) != position):
                return False
    return True


def print_puzzle(puzzle):
    """
    :param puzzle - 2D array of a sudoku puzzle:
    :return None:
    """

    # Prints out the given sudoku puzzle
    for i in range(len(puzzle)):
        if ((i % 3) == 0) and (i != 0):
            print("- - - - - - - - - - - - - - -")
        for j in range(len(puzzle[0])):
            if ((j % 3) == 0) and (j != 0):
                print(" | ", end="")
            if j == 8:
                print(puzzle[i][j])
            else:
                print(str(puzzle[i][j]) + " ", end="")


test_randomness = {}
for i in range(20):
    solvable_puzzle = numpy.zeros((9, 9), dtype=int).tolist()
    generate_filled_puzzle(solvable_puzzle)
    print_puzzle(solvable_puzzle)
    print()
