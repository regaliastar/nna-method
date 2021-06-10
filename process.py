"""
主流程文件
"""
from os import path
from dag import DAG
from utils import read_from_file
from utils import benchmark_manager
from cp import CP
import copy
from log import Log
import random
import sys
sys.setrecursionlimit(3000)  # 将默认的递归深度修改为3000

logger = Log()
logger.set_env('test')    # 若注释，则打印log

# swap门选择算法，复杂度O(raw*col)
def get_min_score_swap(raw, col, current_map, current):
    res = {
        'sum_dist': 9999999999999999,
        'swap': [],
        'map': [],
        'min_count': 1,  #存在多少个最优方法
        'min_swap_list': [],
    }
    min_count_list = []
    # print('get_min_score_swap', raw, col, current_map)
    logger.print('-----get_min_score_swap start------')
    logger.print_current(current, 'get_min_score_swap')
    for i in range(raw):
        for j in range(col):
            # 计算H
            if i+1 < raw:
                # 交换(i,j) <=> (i+1,j)
                # 更新map
                now_map = copy.deepcopy(current_map)
                [k1, k2] = [None, None]
                for k in range(len(now_map)): 
                    if now_map[k][0] == i and now_map[k][1] == j:
                        k1 = k
                    if now_map[k][0] == i+1 and now_map[k][1] == j:
                        k2 = k
                if k1 != None and k2 != None:
                    t = now_map[k1][2]
                    now_map[k1][2] = now_map[k2][2]
                    now_map[k2][2] = t
                elif k1 == None and k2 != None:
                    now_map[k2][0] = i
                    now_map[k2][1] = j
                elif k1 != None and k2 == None:
                    now_map[k1][0] = i+1
                    now_map[k1][1] = j
                sum_dist = 0
                for c in current:
                    dist = get_dist(now_map, c.value[0], c.value[1])
                    # print(dist, now_map, c.value[0], c.value[1], k1, k2)
                    sum_dist += dist
                min_count_list.append(sum_dist)
                if sum_dist == res['sum_dist']:
                    res['min_swap_list'].append([[i,j], [i+1,j]])
                if sum_dist < res['sum_dist']:
                    res['sum_dist'] = sum_dist
                    res['swap'] = [[i,j], [i+1,j]]
                    res['map'] = copy.deepcopy(now_map)
                    res['min_swap_list'].clear()
                    res['min_swap_list'].append([[i,j], [i+1,j]])
            if j+1 < col:
                # 交换(i,j) <=> (i,j+1)
                # 更新map
                now_map = copy.deepcopy(current_map)
                [k1, k2] = [None, None]
                for k in range(len(now_map)):
                    if now_map[k][0] == i and now_map[k][1] == j:
                        k1 = k
                    if now_map[k][0] == i and now_map[k][1] == j+1:
                        k2 = k
                if k1 != None and k2 != None:
                    t = now_map[k1][2]
                    now_map[k1][2] = now_map[k2][2]
                    now_map[k2][2] = t
                elif k1 == None and k2 != None:
                    now_map[k2][0] = i
                    now_map[k2][1] = j
                elif k1 != None and k2 == None:
                    now_map[k1][0] = i
                    now_map[k1][1] = j+1
                sum_dist = 0
                for c in current:
                    dist = get_dist(now_map, c.value[0], c.value[1])
                    sum_dist += dist
                min_count_list.append(sum_dist)
                if sum_dist == res['sum_dist']:
                    res['min_swap_list'].append([[i,j], [i,j+1]])
                if sum_dist < res['sum_dist']:
                    res['sum_dist'] = sum_dist
                    res['swap'] = [[i,j], [i,j+1]]
                    res['map'] = copy.deepcopy(now_map)
                    res['min_swap_list'].clear()
                    res['min_swap_list'].append([[i,j], [i,j+1]])
    min_count_list.sort()
    logger.print('min_count_list', min_count_list)
    for i in range(len(min_count_list)):
        if i == 0:
            continue
        if i > 0 and min_count_list[i] == min_count_list[i-1]:
            res['min_count'] += 1
        else:
            break
    logger.print('get_min_score_swap res:',res)
    logger.print('-----get_min_score_swap end------')
    return res


# 根据当前map关系，得到两个qubit之间的曼哈顿距离
def get_dist(current_map, q1, q2):
    [grid1, grid2] = [[], []]
    for c in current_map:
        if c[2] == q1:
            grid1 = c[:]
        if c[2] == q2:
            grid2 = c[:]
    if len(grid1) == 0 or len(grid2) == 0:
        raise ValueError('get_dist', grid1, grid2, q1, q2)
    return abs(grid1[0]-grid2[0])+abs(grid1[1]-grid2[1])

# 初始映射算法，回溯法
def init_map_process(raw, col, numvars, gates):
    dag = DAG(gates, numvars)
    # dag.print_current()
    def trace_back(dag, res, path):
        logger.print('init_map_process', raw, col, numvars, path)
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
            # 若和当前节点相同的门在path中，则continue ?
            # flag = False
            # for p in path:
            #     if node.value == p:
            #         flag = True
            # if flag:
            #     continue
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

SWAP_NUMBER = 0

# 插入swap算法
def swap_process(raw, col, numvars, gates, init_map):
    # 插入交换门的信息
    swap_path = []
    # 相邻门列表
    exec_list = []
    dag = DAG(gates, numvars)
    current_map = copy.deepcopy(init_map)
    while len(dag.current) > 0:
        # dag.print_current()
        for node in dag.current:
            if get_dist(current_map, node.value[0], node.value[1]) == 1:
                exec_list.append(node)
        # logger.print_exec_list(exec_list)
        if len(exec_list) > 0:
            for node in exec_list:
                dag.defer_del_gate(False, node)
            dag.defer_del_gate(True)
            exec_list.clear()
        else:
            # 启发式算法插入交换门
            res = get_min_score_swap(raw, col, current_map, dag.current)
            first_map = res['map']
            min_swap_list = res['min_swap_list']
            current_num = len(dag.current)
            MAXN = 10
            while res['min_count'] > 1 and current_num < len(dag.current)+MAXN:
                current_num += 1
                current_more = dag.get_current_more(current_num)
                res = get_min_score_swap(raw, col, current_map, current_more)
                logger.print('current_num',current_num)
                pass
            # 若找不到最佳交换，则选择最初的交换
            # 最佳交换必须是最初交换的其中之一
            if current_num >= len(dag.current)+MAXN or res['swap'] not in min_swap_list:
                current_map = copy.deepcopy(first_map)
            else:
                current_map = copy.deepcopy(res['map'])
            swap_path.append(res['swap'])
            global SWAP_NUMBER
            SWAP_NUMBER += 1
            logger.print('已插入swap:', SWAP_NUMBER)
    return swap_path

if __name__ == '__main__':
    name = 'ham7_104'
    benchmark = benchmark_manager()
    file = read_from_file(name)
    print('文件 '+name, '2-门数 '+str(len(file['gates'])), 'numvars',file['numvars'], '\n')
    print(file['gates'])
    placement = init_map_process(benchmark[name]['raw'], benchmark[name]['col'], file['numvars'], file['gates'])
    print('placement:')
    print(placement, '\n')
    swap_path = swap_process(benchmark[name]['raw'], benchmark[name]['col'], file['numvars'], file['gates'], placement['placement'])
    print('总共插入交换门：', str(len(swap_path)))
    print(swap_path)
    