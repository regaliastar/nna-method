"""
主流程文件
"""
from os import path
from dag import DAG
from utils import read_from_file
from utils import benchmark_manager
from cp import CP
import copy

# swap门选择算法，复杂度O(raw*col)
def get_min_score_swap(raw, col, current_map, current):
    res = {
        'sum_dist': 9999999999999999,
        'swap': [],
        'map': []
    }
    # print('get_min_score_swap', raw, col, current_map)
    for i in range(raw):
        for j in range(col):
            # 计算H
            if i+1 < raw:
                # 交换(i,j) <=> (i+1,j)
                # 更新map
                now_map = current_map[:]
                [k1, k2] = [-1, -1]
                for k in range(len(now_map)): 
                    if now_map[k][0] == i and now_map[k][1] == j:
                        k1 = k
                    if now_map[k][0] == i+1 and now_map[k][1] == j:
                        k2 = k
                t = now_map[k1][2]
                now_map[k1][2] = now_map[k2][2]
                now_map[k2][2] = t
                sum_dist = 0
                for c in current:
                    dist = get_dist(now_map, c.value[0], c.value[1])
                    sum_dist += dist
                if sum_dist < res['sum_dist']:
                    res['sum_dist'] = sum_dist
                    res['swap'] = [[i,j], [i+1,j]]
                    res['map'] = copy.deepcopy(now_map)
            if j+1 < col:
                # 交换(i,j) <=> (i,j+1)
                # 更新map
                now_map = current_map[:]
                [k1, k2] = [-1, -1]
                for k in range(len(now_map)):
                    if now_map[k][0] == i and now_map[k][1] == j:
                        k1 = k
                    if now_map[k][0] == i and now_map[k][1] == j+1:
                        k2 = k
                t = now_map[k1][2]
                now_map[k1][2] = now_map[k2][2]
                now_map[k2][2] = t
                sum_dist = 0
                for c in current:
                    dist = get_dist(now_map, c.value[0], c.value[1])
                    sum_dist += dist
                # print('j+1 get_min_score_swap', sum_dist, now_map)
                if sum_dist < res['sum_dist']:
                    res['sum_dist'] = sum_dist
                    res['swap'] = [[i,j], [i,j+1]]
                    res['map'] = copy.deepcopy(now_map)
    return res

# 根据当前map关系，得到两个qubit之间的曼哈顿距离
def get_dist(current_map, q1, q2):
    [grid1, grid2] = [[], []]
    for c in current_map:
        if c[2] == q1:
            grid1 = c[:]
        if c[2] == q2:
            grid2 = c[:]
    return abs(grid1[0]-grid2[0])+abs(grid1[1]-grid2[1])

# 初始映射算法，回溯法
def init_map_process(raw, col, numvars, gates):
    dag = DAG(gates, numvars)
    def trace_back(dag, res, path):
        # if len(path) > raw*col:
        #     return
        cp_res = CP(raw, col, numvars, path)
        if cp_res['status'] == 0:
            if len(path) > len(res):
                res = copy.deepcopy(path)
                global outer_res
                outer_res = copy.deepcopy(path)
        else:
            return
        index = 0
        for node in dag.current:
            flag = False
            for p in path:
                if node.value == p:
                    flag = True
            if flag:
                continue
            path.append(node.value)
            dag_clone = copy.deepcopy(dag)
            dag_clone.del_gate(dag_clone.current[index])
            index += 1
            trace_back(dag_clone, res, path)
            path.pop()
    trace_back(dag, [], [])
    placement = CP(raw, col, numvars, outer_res, dag.current[0].value)
    placement['gates'] = outer_res
    return placement

# 插入swap算法
def swap_process(raw, col, numvars, gates, init_map):
    # 插入交换门的信息
    swap_path = []
    # 相邻门列表
    exec_list = []
    dag = DAG(gates, numvars)
    current_map = init_map[:]
    while len(dag.current) > 0:
        for node in dag.current:
            if get_dist(current_map, node.value[0], node.value[1]) == 1:
                exec_list.append(node)
        if len(exec_list) > 0:
            for node in exec_list:
                dag.defer_del_gate(False, node)
            dag.defer_del_gate(True)
            exec_list.clear()
        else:
            # 启发式算法插入交换门
            res = get_min_score_swap(raw, col, current_map, dag.current)
            current_map = res['map'][:]
            swap_path.append(res['swap'])
    return swap_path

if __name__ == '__main__':
    name = '3_17_13'
    benchmark = benchmark_manager()
    res = read_from_file(name)
    print('文件 '+name, '2-门数 '+str(len(res['gates'])), '\n')
    placement = init_map_process(benchmark[name]['raw'], benchmark[name]['col'], res['numvars'], res['gates'])
    print('placement:')
    print(placement, '\n')
    swap_path = swap_process(benchmark[name]['raw'], benchmark[name]['col'], res['numvars'], res['gates'], placement['placement'])
    print('总共插入交换门：', str(len(swap_path)))