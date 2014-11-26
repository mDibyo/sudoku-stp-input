#!/usr/bin/env python
__author__ = 'dibyo'


import sys
import subprocess
import json
from input import input_puzzle
from output import output_solution


def main(puzzle_def, input_file = "input.in", output_file = "output.out"):
    # Load puzzle
    puzzle_def = json.loads(puzzle_def)

    # Write input to file
    with open(input_file, 'w') as f:
        f.write(input_puzzle(puzzle_def))

    # Execute the easystp algorithm and write out output
    with open(output_file, 'w') as f:
        subprocess.call(['easystp', input_file], stdout=f)

    # Retrieve output and display result
    with open(output_file, 'r') as f:
        solution = output_solution(f.read())
    if solution:
        for row in solution:
            print row
    else:
        print "No solution!"


if __name__ == "__main__":
    if len(sys.argv) == 1:
        raise Exception('Puzzle not defined!')
    input_file = sys.argv[2] if len(sys.argv) >= 3 else "input.in"
    output_file = sys.argv[3] if len(sys.argv) >= 4 else "output.out"
    main(sys.argv[1], input_file, output_file)