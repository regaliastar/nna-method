"""
约束规划(Constraint Programming, CP)

grid[raw][col]
qk: number of qubits

@return: {status=int, placement=[]}
@param status: 0:success, 2:fail
"""
from ortools.linear_solver import pywraplp

def CP(raw, col, qk, gates, next_gate=[]):
    def num2grid(num):
        # 将一维距离转为坐标点
        j = num % col
        i = int(num/col)
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

    # print('Number of variables =', solver.NumVariables())

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
        for i in range(num_grid):
            # 若i=0，则相邻只能是1或3
            # 定义相邻矩阵
            near = []
            now_j = i % col
            now_i = int(i/col)
            if now_i > 0:
                near.append(i-col)
            if now_i < raw-1:
                near.append(i+col)
            if now_j > 0:
                near.append(i-1)
            if now_j < col-1:
                near.append(i+1)
            g0 = [g[0]]
            g1 = [g[1]]
            solver.Add(solver.Sum([x[p, j] for p in near for j in g1]+[1-x[i, g[0]]]) >= 1)
            solver.Add(solver.Sum([x[p, j] for p in near for j in g0]+[1-x[i, g[1]]]) >= 1)
    
    # 约束4
    # 当x[i,j]=1时，support[i]==i
    if len(next_gate) == 2:
        support = range(num_grid)
        n1 = sum(support[i]*x[i, j] for i in range(num_grid) for j in [next_gate[0]])
        n2 = sum(support[i]*x[i, j] for i in range(num_grid) for j in [next_gate[1]])
        solver.Minimize(solver.Sum(
            [n1 - n2]    
        ))
    
    # print('Number of constraints =', solver.NumConstraints())

    status = solver.Solve()
    res = {}
    res['status'] = status
    res['placement'] = []
    # Print solution.
    if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
        # print('Total cost = ', solver.Objective().Value(), '\n')
        for i in range(num_grid):
            for j in range(num_qubit):
                # Test if x[i,j] is 1 (with tolerance for floating point arithmetic).
                if x[i, j].solution_value() > 0.5:
                    [r, c] = num2grid(i)
                    res['placement'].append([r, c, j])
                    # print('grid %d %d  qubit = %d' % (r, c, j))

    # print('\nAdvanced usage:')
    # print('Problem solved in %f milliseconds' % solver.wall_time())
    # print('Problem solved in %d iterations' % solver.iterations())
    # print('Problem solved in %d branch-and-bound nodes' % solver.nodes())
    res['NumVariables'] = solver.NumVariables()
    res['NumConstraints'] = solver.NumConstraints()
    res['cost'] = solver.Objective().Value()
    res['wall_time'] = solver.wall_time()
    res['iterations'] = solver.iterations()
    res['nodes'] = solver.nodes()
    
    return res
    
if __name__ == '__main__':
    # 量子门约束
    # gates = [[0, 3], [1, 3], [3, 4], [0, 2], [2, 3], [0, 1]]
    gates = [[3, 1], [2, 3]]
    next_gate = []
    res = CP(3, 2, 5, gates, next_gate)
    print(res)
