#!/usr/bin/env python
__author__ = 'dibyo'


import sys
import re


def extract_vars(stp_output):
    """ Extract the values of all variables from a successful assignment of
    values in a sudoku puzzle.

    :param stp_output: the output string from the puzzle solution
    :return: values of all variables in the sudoku puzzle
    """
    assignments = re.findall(r"ASSERT\( v(\d)(\d)_(\d)  = (TRUE|FALSE)  \);",
                             stp_output)

    puzzle_solve = [row[:] for row in [[1]*9] * 9]
    for i, j, pos, val in assignments:
        if val == "TRUE":
            puzzle_solve[int(i)][int(j)] += 2 ** int(pos)

    return puzzle_solve


def output_solution(stp_output):
    """ Output the solution of the sudoku puzzle if one exists,

    :param stp_output: the output string from the puzzle solution
    :return: the solution if one exists, else None
    """
    if stp_output.startswith("Satisfiable."):
        return extract_vars(stp_output)
    return None


def main(output_file):
    with open(output_file, 'r') as f:
        stp_output = f.read()
    solution =  output_solution(stp_output)
    if solution:
        for row in solution:
            print row


if __name__ == "__main__":
    if len(sys.argv) >= 2:
        main(sys.argv[1])