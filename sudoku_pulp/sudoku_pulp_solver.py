"""
The Looping Sudoku Problem Formulation for the PuLP Modeller

Authors: Antony Phillips, Dr Stuart Mitcehll
"""

# Import PuLP modeler functions
from pulp import LpProblem, LpMinimize, LpVariable, lpSum, LpStatus, value, LpBinary

COLUMN_SEPARATOR = "| "

ROW_SEPARATOR = "+-------+-------+-------+\n"


def build_sudoku_problem():

    # The values, rows and cols sequences all follow this form
    values = range(1, 10)
    rows = range(1, 10)
    columns = range(1, 10)

    # The boxes list is created, with the row and column index of each square in each box
    boxes = []
    for i in range(3):
        for j in range(3):
            box = [(rows[3 * i + k], columns[3 * j + l]) for k in range(3) for l in range(3)]
            boxes.append(box)

    # The problem variable is created to contain the problem data
    problem = LpProblem("Sudoku Problem", LpMinimize)
    # The problem variables are created
    choices = LpVariable.dicts("Choice", (values,rows, columns), 0, 1, LpBinary)
    # The arbitrary objective function is added
    problem += 0, "Arbitrary Objective Function"

    # A constraint ensuring that only one value can be in each square is created
    for r in rows:
        for c in columns:
            problem += lpSum(choices[v][r][c] for v in values) == 1, ""

    # The row, column and box constraints are added for each value
    for v in values:
        for r in rows:
            problem += lpSum(choices[v][r][c] for c in columns) == 1, ""

        for c in columns:
            problem += lpSum(choices[v][r][c] for r in rows) == 1, ""

        for b in boxes:
            problem += lpSum(choices[v][r][c] for (r, c) in b) == 1, ""

    return problem, choices, values, rows, columns


def fill_example_sudoku(problem, choices):
    # The starting numbers are entered as constraints
    problem += choices[5][1][1] == 1, ""
    problem += choices[6][2][1] == 1, ""
    problem += choices[8][4][1] == 1, ""
    problem += choices[4][5][1] == 1, ""
    problem += choices[7][6][1] == 1, ""
    problem += choices[3][1][2] == 1, ""
    problem += choices[9][3][2] == 1, ""
    problem += choices[6][7][2] == 1, ""
    problem += choices[8][3][3] == 1, ""
    problem += choices[1][2][4] == 1, ""
    problem += choices[8][5][4] == 1, ""
    problem += choices[4][8][4] == 1, ""
    problem += choices[7][1][5] == 1, ""
    problem += choices[9][2][5] == 1, ""
    problem += choices[6][4][5] == 1, ""
    problem += choices[2][6][5] == 1, ""
    problem += choices[1][8][5] == 1, ""
    problem += choices[8][9][5] == 1, ""
    problem += choices[5][2][6] == 1, ""
    problem += choices[3][5][6] == 1, ""
    problem += choices[9][8][6] == 1, ""
    problem += choices[2][7][7] == 1, ""
    problem += choices[6][3][8] == 1, ""
    problem += choices[8][7][8] == 1, ""
    problem += choices[7][9][8] == 1, ""
    problem += choices[3][4][9] == 1, ""
    problem += choices[1][5][9] == 1, ""
    problem += choices[6][6][9] == 1, ""
    problem += choices[5][8][9] == 1, ""
    # return problem


def write_solution_to_file(problem, choices, vals, rows, columns):
    # The problem data is written to an .lp file
    problem.writeLP("Sudoku.lp")

    # A file called output_file.txt is created/overwritten for writing to
    sudoku_output_filename = 'output_file.txt'
    with open(sudoku_output_filename, 'w') as output_file:

        while True:
            problem.solve()
            # The status of the solution is printed to the screen
            print("Status:", LpStatus[problem.status])
            # The solution is printed if it was deemed "optimal" i.e met the constraints
            if LpStatus[problem.status] == "Optimal":
                # The solution is written to the output_file.txt file
                write_solution(choices, vals, rows, columns, output_file)
                # The constraint is added that the same solution cannot be returned again
                problem += lpSum(choices[v][r][c] for v in vals for r in rows for c in columns if value(choices[v][r][c]) == 1) <= 80

            else:
                # If a new optimal solution cannot be found, we end the program
                break

    # The location of the solutions is give to the user
    print("Solutions Written to {}".format(sudoku_output_filename))


def write_solution(choices, vals, rows, columns, output_file):
    for r in rows:
        if r == 1 or r == 4 or r == 7:
            output_file.write(ROW_SEPARATOR)
        for c in columns:
            if c == 1 or c == 4 or c == 7:
                output_file.write(COLUMN_SEPARATOR)
            for v in vals:
                if value(choices[v][r][c]) == 1:
                    output_file.write("{} ".format(v))
            if c == 9:
                output_file.write(COLUMN_SEPARATOR + "\n")
    output_file.write(ROW_SEPARATOR)


def main():
    problem, choices, vals, rows, columns = build_sudoku_problem()
    fill_example_sudoku(problem, choices)
    write_solution_to_file(problem, choices, vals, rows, columns)


if __name__ == '__main__':
    main()
