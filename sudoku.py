import numpy
import random
import requests
from bs4 import BeautifulSoup


def create_sudoku_puzzle():
    new_puzzle = numpy.zeros((9, 9), dtype=int).tolist()
    generate_filled_puzzle(new_puzzle)

    while True:
        temp_puzzle = new_puzzle.copy()
        for i in range(random.randint(15, 20)):
            while True:
                row = random.randint(0, 8)
                col = random.randint(0, 8)

                if temp_puzzle[row][col] != 0:
                    break
            temp_puzzle[row][col] = 0
            temp_puzzle[8 - row][8 - col] = 0
        if get_number_of_solutions(temp_puzzle) == 1:
            new_puzzle = temp_puzzle
            return new_puzzle



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


def get_number_of_solutions(puzzle):
    temp_puzzle = numpy.array(puzzle).flatten()
    string = ''.join(str(e) for e in temp_puzzle).replace("0", ".")

    url = "https://www.thonky.com/sudoku/solution-count?puzzle=" + string
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    results = soup.find('strong')
    get_num = results.get_text().split()

    for elem in get_num:
        if elem.isdigit():
            return int(elem)


def solve_puzzle(puzzle):
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
    for num in range(1, 10):
        if check_valid(puzzle, num, empty_space):
            puzzle[row][col] = num

            # Recursive call to check the next empty spot in the puzzle
            if solve_puzzle(puzzle):
                return True

            # if the guess does not work, we backtrack to last number
            puzzle[row][col] = 0
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


def main():
    puzzle = create_sudoku_puzzle()
    print_puzzle(puzzle)
    temp_puzzle = numpy.array(puzzle).flatten()
    string = ''.join(str(e) for e in temp_puzzle).replace("0", ".")

    url = "https://www.thonky.com/sudoku/solution-count?puzzle=" + string
    print(url)


if __name__ == "__main__":
    main()
