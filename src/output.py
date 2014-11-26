__author__ = 'dibyo'


import re


def extract_vars(puzzle_out):
    """ Extract the values of all variables from a successful assignment of
    values in a sudoku puzzle.

    :param output: the output string from the SAT solver
    :return: values of all variables in the sudoku puzzle
    """
    assignments = re.findall(r"ASSERT\( v(\d)(\d)_(\d)  = (TRUE|FALSE)  \);",
                             puzzle_out)

    puzzle_solve = [row[:] for row in [[1]*9] * 9]
    for i, j, pos, val in assignments:
        if val == "TRUE":
            puzzle_solve[int(i)][int(j)] += 2 ** int(pos)

    return puzzle_solve


def output_solution(puzzle_out):
    if puzzle_out.startswith("Satisfiable."):
        return extract_vars(puzzle_out)
    return None