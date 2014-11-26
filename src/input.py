from __future__ import division
from textwrap import dedent


def initialize_var(var):
    """ Create a variable with a given name. They can only take 9 different
    values that represent the nine digits in a sudoku puzzle.

    :param var: the name given to the variable
    :return: the input string for initializing the variable
    """
    stp_input = """\
    $_0, $_1, $_2, $_3 : BOOLEAN;
    ASSERT($_3 AND NOT($_0 OR $_1 OR $_2));
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
    """ Inequate two variables so that they have different values

    :param var1: the name of the first variable
    :param var2: the name of the second variable
    :return: the input string for inequating the two variables
    """
    stp_input = """\
    ASSERT((#_0 XOR $_0) OR (#_1 XOR $_1) OR (#_2 XOR $_2) OR (#_3 XOR $_3))
    """

    stp_input.replace("#", var1)
    stp_input.replace("$", var2)
    return dedent(stp_input)
