from ortools.linear_solver import pywraplp

"""
grid[raw][col]
qk: number of qubits
"""
def CP(raw, col, qk, gates):
    def num2grid(num):
        # 将一维距离转为坐标点
        j = num % raw
        i = int(num/raw)
        return [i, j]
    def countDist(i, j):
        # 曼哈顿距离
        list_i = num2grid(i)
        list_j = num2grid(j)
        return abs(list_i[0]-list_j[0])+abs(list_i[1]-list_j[1])
    def c3(l1, l2):
        # 约束3
        a = l1[0]
        b = l2[0]
        res = []
        res.append(countDist(a, b))
        return res

    
    # Create the mip solver with the SCIP backend.
    solver = pywraplp.Solver.CreateSolver('SCIP')

    x = {}
    num_grid = raw*col
    num_qubit = qk
    for i in range(num_grid):
        for j in range(num_qubit):
            x[i, j] = solver.IntVar(0, 1, '')

    print('Number of variables =', solver.NumVariables())

    # 约束1，每个qubit只有一个格子
    for j in range(num_qubit):
        solver.Add(solver.Sum([x[i, j] for i in range(num_grid)]) == 1)

    # 约束2，每个格子只能分配一个qubit
    for i in range(num_grid):
        solver.Add(solver.Sum([x[i, j] for j in range(num_qubit)]) <= 1)

    # 约束3，门约束
    for g in gates:
        # [k[0] for k in x.keys() if k[1] == g[0] and x[k] == 1], [k[0] for k in x.keys() if k[1] == g[1] and x[k] == 1] 对于x[i,j]==1，得到i的值
        # 若g=[0,3]，则取x[i1,0]中的i1，与x[i2,3]中的i2，计算i1与i2的曼哈顿距离
        # solver.Add(solver.Sum(c3([k[0] for k in x.keys() if k[1] == g[0] and x[k] == 1], [k[0] for k in x.keys() if k[1] == g[1] and x[k] == 1])) <= 1)
        item1 = [0]*num_qubit
        item2 = [0]*num_qubit
        item1[g[0]] = 1
        item2[g[1]] = 1
        # solver.Sum([i * item1[j] * x[i, j] for j in range(num_qubit)])      i1
        # solver.Sum([i * item2[j] * x[i, j] for j in range(num_qubit)])      i2
        for i in range(num_grid):
            # 若i=0，则相邻只能是1或3
            # 定义相邻矩阵
            near = [0]*num_grid
            now_j = i % raw
            now_i = int(i/raw)
            if now_i > 0:
                near[i-raw] = 1
            if now_i < raw-1:
                near[i+raw] = 1
            if now_j > 0:
                near[i-1] = 1
            if now_j < col-1:
                near[i+1] = 1
            solver.Add(solver.Sum([x[i, j] for j in range(num_qubit)]))
            # solver.Add(solver.Sum([i * item1[j] * x[i, j] for j in range(num_qubit)]) <= 2)
            pass
        

    print('Number of constraints =', solver.NumConstraints())

    status = solver.Solve()

    # Print solution.
    if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
        # print('Total cost = ', solver.Objective().Value(), '\n')
        for i in range(num_grid):
            for j in range(num_qubit):
                # Test if x[i,j] is 1 (with tolerance for floating point arithmetic).
                if x[i, j].solution_value() > 0.5:
                    [r, c] = num2grid(i)
                    print('grid %d %d  qubit = %d' %
                          (r, c, j))

    print('\nAdvanced usage:')
    print('Problem solved in %f milliseconds' % solver.wall_time())
    print('Problem solved in %d iterations' % solver.iterations())
    print('Problem solved in %d branch-and-bound nodes' % solver.nodes())


if __name__ == '__main__':
    # 量子门约束
    # gates = [[0, 3], [1, 3], [3, 4], [0, 2], [2, 3], [0, 1]]
    gates = [[0, 3], [1, 3], [3, 4], [0, 2]]
    CP(3, 3, 5, gates)