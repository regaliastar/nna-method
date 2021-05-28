from ortools.linear_solver import pywraplp
import re
from functools import reduce


def test_CP():
       
    def num2grid(num):
        # 将一维距离转为坐标点
        raw = 3 
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

    x = {}
    for i in range(9):
        for j in range(5):
            x[i, j] = 0
    x[0, 0] = 1
    x[1, 1] = 1
    x[2, 2] = 1
    x[3, 3] = 1
    x[4, 4] = 1

    gates = [[0, 3], [1, 3], [3, 4], [0, 2], [2, 3], [0, 1]]
    # for g in gates:
    #     print(c3([k[0] for k in x.keys() if k[1] == g[0] and x[k] == 1], [k[0] for k in x.keys() if k[1] == g[1] and x[k] == 1]))
    for g in gates:
        print(sum([x[i, j] for j in range(g[0])]))

def test_read_from_file():
    numvars_pattern = r'numvars'
    s1 = '.numvars 3'
    s2 = '.variables a b c'
    numvars1 = re.match(numvars_pattern, s1)
    numvars2 = re.match(numvars_pattern, s2)
    if('numvars' in s1):
        print(1)
    if('numvars' in s2):
        print(2)
    print(numvars1, numvars2)

def test_decompose():
    numvars = 5
    gate = [0, 4, 2, 1]
    candidate = list(set(range(numvars)).difference(gate))
    dist = []
    for c in candidate:
        dist.append(reduce(lambda x,y: x+abs(y-c), gate)+abs(gate[0]-c))
    print(candidate, dist)
        
if __name__ == '__main__':
    # test_CP()
    # test_read_from_file()
    test_decompose()