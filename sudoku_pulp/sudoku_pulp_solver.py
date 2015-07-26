"""
The Looping Sudoku Problem Formulation for the PuLP Modeller

Authors: Antony Phillips, Dr Stuart Mitcehll
"""

from sudoku import model
from pulp import LpProblem, LpMinimize, LpVariable, lpSum, LpStatus, value, LpBinary, solvers

def build_sudoku_problem():

    # The values, rows and cols sequences all follow this form
    values = range(9)
    rows = range(9)
    columns = range(9)

    # The boxes list is created, with the row and column index of each square in each box
    boxes = []
    for i in range(3):
        for j in range(3):
            box = [(rows[3 * i + k], columns[3 * j + l]) for k in range(3) for l in range(3)]
            boxes.append(box)

    # The problem variable is created to contain the problem data
    problem = LpProblem("Sudoku Problem", LpMinimize)
    # The problem variables are created
    choices = LpVariable.dicts("Choice", (rows, columns, values), 0, 1, LpBinary)
    # The arbitrary objective function is added
    problem += 0, "Arbitrary Objective Function"

    # A constraint ensuring that only one value can be in each square is created
    for r in rows:
        for c in columns:
            problem += lpSum(choices[r][c][v] for v in values) == 1, "unique_val_" + str(r) + '_' + str(c)

    # The row, column and box constraints are added for each value
    for v in values:
        for r in rows:
            problem += lpSum(choices[r][c][v] for c in columns) == 1, "row_" + str(v) + '_' + str(r)

        for c in columns:
            problem += lpSum(choices[r][c][v] for r in rows) == 1, "col_" + str(v) + '_' + str(c)

        for box_index, b in enumerate(boxes):
            problem += lpSum(choices[r][c][v] for (r, c) in b) == 1, "box_" + str(v) + '_' + str(box_index)

    return problem, choices, values, rows, columns


def fill_example_sudoku(problem, choices, sudoku_table):
    # The starting numbers are entered as constraints
    for (r, c), v in sudoku_table.iteritems():
        problem += choices[r][c][v - 1] == 1, "cell_" + str((r, c))


def solve_sudoku(problem, choices):
    while True:
        problem.solve()
        # problem.solve(solver=solvers.PULP_CBC_CMD())   # Default solver
        # problem.solve(solver=solvers.COIN())
        # problem.solve(solver=solvers.GLPK())
        # problem.solve(solver=solvers.GUROBI())
        # problem.solve(solver=solvers.GUROBI_CMD())
        # problem.solve(solver=solvers.CPLEX())
        if LpStatus[problem.status] == "Optimal":
            sudoku_table_solution = get_solution(choices)
            problem += lpSum(choices[r][c][v] for r in xrange(9) for c in xrange(9) for v in xrange(9)
                             if value(choices[r][c][v]) == 1) <= 80
            yield sudoku_table_solution
        else:
            break


def get_solution(choices):
    sudoku_table_solution = model.SudokuTable()
    for r in range(9):
        for c in range(9):
            sudoku_table_solution[(r, c)] = [value(choices[r][c][v]) for v in range(9)].index(1) + 1
    return sudoku_table_solution


def main():
    example_line = ".94...13..............76..2.8..1.....32.........2...6.....5.4.......8..7..63.4..8"
    sudoku_example = model.SudokuTable()
    sudoku_example.read_from_line(line=example_line)
    problem, choices, vals, rows, columns = build_sudoku_problem()
    fill_example_sudoku(problem, choices, sudoku_example)
    solutions = list(solve_sudoku(problem, choices))
    for s in solutions:
        print s


if __name__ == '__main__':
    main()
