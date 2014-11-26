from textwrap import dedent

def init_variable(name):
    """ Create a variable with a given name. They can only take 9 different
    values that represent the nine digits in a sudoku puzzle.

    :param name: the name given to the variable
    :return: the input string for initializing the variable
    """
    stp_input = """\
    $_0, $_1, $_2, $_3 : BOOLEAN;
    ASSERT($_3 AND NOT($_0 OR $_1 OR $_2));
    """
    var_input = stp_input.replace('$', name)
    return dedent(stp_input)


def eq_variable(name, value):
    """ Equate the variable to the given value. This value can take on the 9
    different values in [1, 9] and represent the nine digits in a sudoku
    puzzle
    
    :param name: the name of the variable
    :param value: the value to which the variable must be equated
    :return: the input string for equating the variable to value
    """
    stp_input = """\

    """