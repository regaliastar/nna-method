from ortools.linear_solver import pywraplp

"""
grid[raw][col]
qk: number of qubits
"""
def MIP(raw, col, qk):
    def distance(i, j):
        """
        将一维距离转为二维距离
        曼哈顿距离
        """
        pass

    # Create the mip solver with the SCIP backend.
    solver = pywraplp.Solver.CreateSolver('SCIP')

    # x is integer non-negative variables from 0 to raw*col-1.
    list_x = []
    for i in range(qk):
        list_x.append(solver.IntVar(0.0, raw*col-1, ''))

    print('Number of variables =', solver.NumVariables())

    # 约束1，所有值都不相等
    for i in range(len(list_x)-1):
        solver.Add(list_x[i] != list_x[i+1])
        pass
    
    # 约束2，门约束问题

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
    MIP(3, 3, 5)