from pyomo.environ import *
from pyomo.opt import SolverFactory
# from pyomo.scripting import util
# from pyutilib.misc import Options

# This python file defines a function to create a
# model for the sudoku problem

# create a standard python dict for the map from
# subsq to (row,col) numbers
subsq_to_row_col = dict()

subsq_to_row_col[1] = [(i,j) for i in xrange(1, 4) for j in xrange(1, 4)]
subsq_to_row_col[2] = [(i,j) for i in xrange(1, 4) for j in xrange(4, 7)]
subsq_to_row_col[3] = [(i,j) for i in xrange(1, 4) for j in xrange(7, 10)]

subsq_to_row_col[4] = [(i,j) for i in xrange(4, 7) for j in xrange(1, 4)]
subsq_to_row_col[5] = [(i,j) for i in xrange(4, 7) for j in xrange(4, 7)]
subsq_to_row_col[6] = [(i,j) for i in xrange(4, 7) for j in xrange(7, 10)]

subsq_to_row_col[7] = [(i,j) for i in xrange(7, 10) for j in xrange(1, 4)]
subsq_to_row_col[8] = [(i,j) for i in xrange(7, 10) for j in xrange(4, 7)]
subsq_to_row_col[9] = [(i,j) for i in xrange(7, 10) for j in xrange(7, 10)]

# use this function to create the sudoku model defining a list
# of integer cuts. Entry i in cut_on lists all the (r,c,v) tuples
# where y[r,c,v] was 1. Entry i in cut_off lists the ones that were 0
# The input board is a list of the fixed numbers in the board in
# (r,c,v) tuples
def create_sudoku_model(cut_on, cut_off, board):

    model = ConcreteModel()
    # model = AbstractModel()

    # create sets for rows columns and squares
    model.ROWS = RangeSet(1, 9)
    model.COLS = RangeSet(1, 9)
    model.SUBSQUARES = RangeSet(1, 9)
    model.VALUES = RangeSet(1, 9)
    model.CUTS = RangeSet(1, len(cut_on))

    # create the binary variables to define the values
    def _y_rule(model, r, c, v):
        if (r, c, v) in board:
            model.y[r, c, v].fixed = True
            return 1
        return 0
    model.y = Var(model.ROWS, model.COLS, model.VALUES, initialize=_y_rule, within=Binary)

    # create the objective - this is a feasibility problem so we just make it a constant
    def _Obj(model):
        return 1
    model.obj = Objective(rule=_Obj)

    # @row_col_cons:
    def row_constraint(model, i, v):
        return sum(model.y[i, c, v] for c in xrange(1, 10)) == 1
    model.RowCon = Constraint(model.ROWS, model.VALUES, rule=row_constraint)

    # exactly one number in each column
    def column_constraint(model, j, v):
        return sum(model.y[r,j,v] for r in xrange(1,10)) == 1
    model.ColCon = Constraint(model.COLS, model.VALUES, rule=column_constraint)

    # exactly one number in each subsquare
    def subsquare_constraint(model, b, v):
        return sum(model.y[t[0], t[1], v] for t in subsq_to_row_col[b]) == 1
    model.SubSqCon = Constraint(model.SUBSQUARES, model.VALUES, rule=subsquare_constraint)

    # exactly one number in each cell
    def value_constraint(model, i, j):
        return sum(model.y[i, j, v] for v in xrange(1,10)) == 1
    model.ValueCon = Constraint(model.ROWS, model.COLS, rule=value_constraint)

    # integer cuts to prune previous solutions
    def integer_cuts(model, i):
        return sum((1.0-model.y[r, c, v]) for (r,c,v) in cut_on[i-1]) + sum(model.y[r, c, v] for (r, c, v) in cut_off[i-1]) >= 1

    model.IntCuts = Constraint(model.CUTS, rule=integer_cuts)

    return model


# define the board
board = [(1,1,5),(1,2,3),(1,5,7),
         (2,1,6),(2,4,1),(2,5,9),(2,6,5),
         (3,2,9),(3,3,8),(3,8,6),
         (4,1,8),(4,5,6),(4,9,3),
         (5,1,4),(5,4,8),(5,6,3),(5,9,1),
         (6,1,7),(6,5,2),(6,9,6),
         (7,2,6),(7,7,2),(7,8,8),
         (8,4,4),(8,5,1),(8,6,9),(8,9,5),
         (9,5,8),(9,8,7),(9,9,9)]

def main():

    # create the empty list of cuts to start
    cut_on = []
    cut_off = []

    done = False
    while not done:
        model = create_sudoku_model(cut_on, cut_off, board)

        # options = Options()
        # options.solver = 'glpk'
        # options.quiet = True
        # options.tee = True

        # results, opt = util.apply_optimizer(options, model)
        # instance.load(results)

        ## SOLVE ##
        opt = SolverFactory('glpk')

        # create model instance, solve
        # instance = model.create_instance()
        results = opt.solve(model)
        model.solutions.load_from(results)

        if str(results.Solution.Status) != 'optimal':
            break

        # add cuts
        new_cut_on = []
        new_cut_off = []
        for r in model.ROWS:
            for c in model.COLS:
                for v in model.VALUES:
                    # check if the binary variable is on or off
                    # note, it may not be exactly 1
                    if value(model.y[r,c,v]) >= 0.5:
                        new_cut_on.append((r,c,v))
                    else:
                        new_cut_off.append((r,c,v))

        cut_on.append(new_cut_on)
        cut_off.append(new_cut_off)

        print "Solution #" + str(len(cut_on))
        for i in xrange(1,10):
            for j in xrange(1,10):
                for v in xrange(1,10):
                    if value(model.y[i,j,v]) >= 0.5:
                        print v, " ",
            print

if __name__ == '__main__':
    main()