"""
主流程文件
"""
from dag import DAG
from utils import read_from_file
from cp import CP
import copy

# current选择算法
def dag_select(current):
    for c in current:
        pass

# 初始映射算法，回溯法
def init_map_process(raw, col, numvars, gates):
    dag = DAG(gates, numvars)
    path = []
    res = []
    def trace_back(dag, res, path):
        if len(path) >= raw*col:
            return
        cp_res = CP(raw, col, numvars, path)
        if cp_res['status'] == 0:
            if len(path) > len(res):
                res = copy.deepcopy(path)
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
    trace_back(dag, res, path)
    placement = CP(raw, col, numvars, res, dag.current[0].value)
    placement['gates'] = res
    return placement

# 门选择算法
def swap_process():
    # 当前执行门列表
    exec = []

if __name__ == '__main__':
    # names = ['3_17_13', '4_49_17', '4gt10-v1_81']
    test_names = ['3_17_13']
    for name in test_names:
        res = read_from_file(name)
        print('文件 '+name, '2-门数 '+str(len(res['gates'])))
        placement = init_map_process(2, 2, res['numvars'], res['gates'])
        print(placement)