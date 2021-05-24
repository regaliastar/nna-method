from ortools.linear_solver import pywraplp

"""
grid[raw][col]
qk: number of qubits
"""
def main(raw, col, qk):
    # Create the mip solver with the SCIP backend.
    solver = pywraplp.Solver.CreateSolver('SCIP')

    # x is integer non-negative variables from 0 to raw*col-1.
    list_x = []
    for i in range(qk):
        list_x.append(solver.IntVar(0.0, raw*col-1, 'x'))

    print('Number of variables =', solver.NumVariables())

    # conditions

    print('Number of constraints =', solver.NumConstraints())

    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        print('Solution:')
        print('Objective value =', solver.Objective().Value())
        for x in list_x:
            print(x.solution_value())
    else:
        print('The problem does not have an optimal solution.')

    print('\nAdvanced usage:')
    print('Problem solved in %f milliseconds' % solver.wall_time())
    print('Problem solved in %d iterations' % solver.iterations())
    print('Problem solved in %d branch-and-bound nodes' % solver.nodes())


if __name__ == '__main__':
    main(3, 3, 5)