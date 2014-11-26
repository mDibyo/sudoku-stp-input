#!/usr/bin/env python
__author__ = 'dibyo'


from textwrap import dedent
from itertools import combinations
import sys
import json


def initialize_var(var):
    """ Create a variable with a given name. They can only take 9 different
    values that represent the nine digits in a sudoku puzzle.

    :param var: the name given to the variable
    :return: the input string for initializing the variable

    >>> print initialize_var("var")
    var_0, var_1, var_2, var_3 : BOOLEAN;
    ASSERT((var_3 AND NOT(var_0 OR var_1 OR var_2)) OR NOT(var_3));
    <BLANKLINE>
    """
    stp_input = """\
    $_0, $_1, $_2, $_3 : BOOLEAN;
    ASSERT(($_3 AND NOT($_0 OR $_1 OR $_2)) OR NOT($_3));
    """

    stp_input = stp_input.replace('$', var)
    return dedent(stp_input)


def equate_var(var, value):
    """ Equate the variable to the given value. This value can take on the 9
    different values in [1, 9] and represent the nine digits in a sudoku
    puzzle

    :param name: the name of the variable
    :param value: the value to which the variable must be equated
    :return: the input string for equating the variable to value

    >>> print equate_var("var", 5)
    ASSERT(NOT(var_3));
    ASSERT(var_2);
    ASSERT(NOT(var_1));
    ASSERT(NOT(var_0));
    <BLANKLINE>
    """
    value -= 1
    stp_input = ""

    def assign_value(token, val):
        if val:
            return "ASSERT(%s);\n" % token
        return "ASSERT(NOT(%s));\n" % token

    stp_input += assign_value("$_3", value // 8)
    value %= 8
    stp_input += assign_value("$_2", value // 4)
    value %= 4
    stp_input += assign_value("$_1", value // 2)
    value %= 2
    stp_input += assign_value("$_0", value // 1)

    stp_input = stp_input.replace('$', var)
    return dedent(stp_input)


def inequate_vars(var1, var2):
    """ Inequate two variables so that they have different values in the
    sudoku puzzle.

    :param var1: the name of the first variable
    :param var2: the name of the second variable
    :return: the input string for inequating the two variables

    >>> print inequate_vars("v1", "v2") # doctest: +NORMALIZE_WHITESPACE
    ASSERT((v1_0 XOR v2_0) OR (v1_1 XOR v2_1) OR (v1_2 XOR v2_2) OR \
    (v1_3 XOR v2_3));
    <BLANKLINE>
    """
    stp_input = "ASSERT("
    stp_input += "($1_0 XOR $2_0)" + " OR "
    stp_input += "($1_1 XOR $2_1)" + " OR "
    stp_input += "($1_2 XOR $2_2)" + " OR "
    stp_input += "($1_3 XOR $2_3)"
    stp_input += ");\n"

    stp_input = stp_input.replace("$1", var1)
    stp_input = stp_input.replace("$2", var2)
    return dedent(stp_input)


def create_independent_set(set):
    """ Create a set of up to 9 independent variables, ie. variables that
    do not have the same value as any of the other variables in the set.

    :param set: the set of variables that have different values
    :return: the input string for creating an independent set of variables

    >>> set = map(lambda n: "v" + str(n), xrange(1, 6))
    >>> print create_independent_set(set) # doctest: +NORMALIZE_WHITESPACE
    ASSERT((v1_0 XOR v2_0) OR (v1_1 XOR v2_1) OR (v1_2 XOR v2_2) OR \
    (v1_3 XOR v2_3));
    ASSERT((v1_0 XOR v3_0) OR (v1_1 XOR v3_1) OR (v1_2 XOR v3_2) OR \
    (v1_3 XOR v3_3));
    ASSERT((v1_0 XOR v4_0) OR (v1_1 XOR v4_1) OR (v1_2 XOR v4_2) OR \
    (v1_3 XOR v4_3));
    ASSERT((v1_0 XOR v5_0) OR (v1_1 XOR v5_1) OR (v1_2 XOR v5_2) OR \
    (v1_3 XOR v5_3));
    ASSERT((v2_0 XOR v3_0) OR (v2_1 XOR v3_1) OR (v2_2 XOR v3_2) OR \
    (v2_3 XOR v3_3));
    ASSERT((v2_0 XOR v4_0) OR (v2_1 XOR v4_1) OR (v2_2 XOR v4_2) OR \
    (v2_3 XOR v4_3));
    ASSERT((v2_0 XOR v5_0) OR (v2_1 XOR v5_1) OR (v2_2 XOR v5_2) OR \
    (v2_3 XOR v5_3));
    ASSERT((v3_0 XOR v4_0) OR (v3_1 XOR v4_1) OR (v3_2 XOR v4_2) OR \
    (v3_3 XOR v4_3));
    ASSERT((v3_0 XOR v5_0) OR (v3_1 XOR v5_1) OR (v3_2 XOR v5_2) OR \
    (v3_3 XOR v5_3));
    ASSERT((v4_0 XOR v5_0) OR (v4_1 XOR v5_1) OR (v4_2 XOR v5_2) OR \
    (v4_3 XOR v5_3));
    <BLANKLINE>
    """
    stp_input = ""
    for var1, var2 in combinations(set, 2):
        stp_input += inequate_vars(var1, var2)
    return stp_input


def do_nothing():
    """ Does nothing. This is used to add empty lines to the input

    :return: the input string for doing nothing ie. "\n"
    """
    return "\n"


def get_variable_name(i, j):
    """ Returns a variable name for the given indices.

    :param i: the first index
    :param j: the second index
    :return: the variable name

    >>> print get_variable_name(2, 5)
    v25
    """
    return "v%d%d" % (i, j)


def input_puzzle(puzzle_def):
    """ Create the STP input for a given sudoku puzzle and return it

    :param puzzle_def: the puzzle represented as a 9x9 matrix
    :return: the input string for initializing the puzzle

    >>> puzzle_def = [[0, 0, 0, 0, 0, 0, 0, 0, 0 ],
    ...               [0, 0, 0, 0, 0, 3, 0, 8, 5 ],
    ...               [0, 0, 1, 0, 2, 0, 0, 0, 0 ],
    ...               [0, 0, 0, 5, 0, 7, 0, 0, 0 ],
    ...               [0, 0, 4, 0, 0, 0, 1, 0, 0 ],
    ...               [0, 9, 0, 0, 0, 0, 0, 0, 0 ],
    ...               [5, 0, 0, 0, 0, 0, 0, 7, 3 ],
    ...               [0, 0, 2, 0, 1, 0, 0, 0, 0 ],
    ...               [0, 0, 0, 0, 4, 0, 0, 0, 9 ] ]

    # >>> print input_puzzle(puzzle_def)
    """
    stp_input = ""

    # Initialize all variables (boxes) in the puzzle
    for i in xrange(9):
        for j in xrange(9):
            stp_input += initialize_var(get_variable_name(i, j))
            stp_input += do_nothing()

    stp_input += do_nothing()
    # Set up variables that are already known
    for i in xrange(9):
        for j in xrange(9):
            if puzzle_def[i][j]:
                stp_input += equate_var(get_variable_name(i, j),
                                        puzzle_def[i][j])
                stp_input += do_nothing()

    stp_input += do_nothing()
    stp_input += do_nothing()

    # Set up all rules of the puzzle
    # 1: Set up rows
    for row in xrange(9):
        set = map(lambda column: get_variable_name(row, column),
                  xrange(9))
        stp_input += create_independent_set(set)

    stp_input += do_nothing()
    # 2: Set up columns
    for column in xrange(9):
        set = map(lambda row: get_variable_name(row, column),
                  xrange(9))
        stp_input += create_independent_set(set)

    stp_input += do_nothing()
    # 3: Set up smaller squares
    for square_row in xrange(3):
        for square_column in xrange(3):
            set = [get_variable_name(3*square_row + r, 3*square_column + c)
                   for r in xrange(3) for c in xrange(3)]
            stp_input += create_independent_set(set)

    stp_input += do_nothing()

    return stp_input


def main(puzzle_def, input_file):
    r"""
    :param puzzle_def: json string containing the puzzle to be solved
    :param input_file: the name of the file in which the input string for the
        stp solver must be saved
    :return: None

    >>> puzzle_def = "[[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 3, 0, 8, 5\
    ... ], [0, 0, 1, 0, 2, 0, 0, 0, 0], [0, 0, 0, 5, 0, 7, 0, 0, 0], [0, 0, 4,\
    ... 0, 0, 0, 1, 0, 0], [0, 9, 0, 0, 0, 0, 0, 0, 0], [5, 0, 0, 0, 0, 0, 0, \
    ... 7, 3], [0, 0, 2, 0, 1, 0, 0, 0, 0], [0, 0, 0, 0, 4, 0, 0, 0, 9]]"
    >>> puzzle_def = json.loads(puzzle_def)

    # >>> main(puzzle_def, 'input.in')
    """
    puzzle_def = json.loads(puzzle_def)
    with open(input_file, 'w') as f:
        f.write(input_puzzle(puzzle_def))


if __name__ == "__main__":
    if len(sys.argv) >= 3:
        main(sys.argv[1], sys.argv[2])
