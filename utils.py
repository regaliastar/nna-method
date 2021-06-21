"""
读取benchmark中的文件，将其转换成门约束格式如：[[0, 3], [1, 3], [3, 4], [0, 2], [2, 3], [0, 1]]

reference:
benckmark - Qubit placement to minimize communication overhead in 2D quantum architectures
"""
from functools import reduce

def read_from_file(name):
    res = []
    if len(name) == 0:
        return {
            'gates': []
        }
    filename = 'benchmark/'+name+'.real'
    with open(filename, 'r') as f:
        list = f.readlines()
        chars_table = {
            'a':0, 'b':1, 'c':2, 'd':3, 'e':4, 'f':5, 
            'g':6, 'h':7, 'i':8, 'j':9, 'k':10,
            'x0':0, 'x1':1, 'x2':2, 'x3':3, 'x4':4, 'x5':5, 
            'x6':6, 'x7':7, 'x8':8, 'x9':9, 'x10':10,
            
        }
        numvars = 0
        begin = False
        prefix = ['t', 'p', 'v']
        for item in list:
            if item[0] == '#':
                pass
            elif item[0] == '.':
                if '.begin' in item:
                    begin = True
                if 'numvars' in item:
                    numvars = int(item.split(' ')[1])
                if 'variables' in item:
                    item = item.rstrip('\n')
                    item.strip()
                    line = item.split(' ')[1:]
                    for i in range(len(line)):
                        chars_table[line[i]] = i
            elif item[0] in prefix and begin:
                item = item.rstrip('\n')
                item.strip()
                line = item.split(' ')
                if line[0] == 'p':
                    q_num = len(line)-1
                else:
                    s = line[0][1:]
                    if s.isdigit():
                        q_num = int(line[0][1:])
                    else:
                        q_num = len(line)-1
                g = []
                for index in range(len(line)):
                    if index == 0:
                        continue
                    if line[index] == '':
                        continue
                    if line[index] in chars_table:
                        g.append(chars_table[line[index]])
                    else:
                        print(chars_table, line[index])
                        raise ValueError(name+' 解析门失败: '+'index: '+str(index)+' '+' '.join(line)+' '+name)
                de_g = decompose(q_num, g, numvars)
                res += de_g
    return {
        'gates': res,
        'numvars': numvars
    }

"""
@param qubit: 当前gate影响比特数量
@param gate: 量子门
@param numvars: 量子比特总数

分解量子门算法
[a,b,c] => [[b,c],[a,b],[b,c],[a,b],[a,c]], [[a,c],[a,b],[b,c],[a,b],[b,c]]

n-qubit门与分解成的2-qubit门数量对应关系
3 => 5
4 => 14
5 == 3+4+3+4 =>  

referece:
* Elementary quantum gate realizations for multiple-control Toffoli gates
* Quantum Circuit Simplification and Level Compaction
Lower Cost Quantum Gate Realizations of Multiple-control Toffoli Gates
Multi-strategy based quantum cost reduction of linear nearest-neighbor quantum circuit
"""
def decompose(qubit, gate, numvars):
    if numvars == 0:
        raise ValueError('numvars 不能为 0')
    res = []
    if qubit == 1:
        pass
    elif qubit == 2:
        res.append(gate)
    elif qubit == 3:
        res = [[gate[1],gate[2]],[gate[0],gate[1]],[gate[1],gate[2]],[gate[0],gate[1]],[gate[0],gate[2]]]
    elif qubit == 4:
        # 这里需要利用辅助比特
        # 求gate的差集，得到可用的辅助比特
        candidate = list(set(range(numvars)).difference(gate))
        dist = []
        for c in candidate:
            dist.append(reduce(lambda x,y: x+abs(y-c), gate)+abs(gate[0]-c))
        min = 999999999
        index = 0
        for i in range(len(dist)):
            if min > dist[i]:
                min = dist[i]
                index = i
        aux_bit = candidate[index]
        # res += decompose(3, [gate[2], aux_bit, gate[3]], numvars)
        # res += decompose(3, [gate[0], aux_bit, gate[1]], numvars)
        # res += decompose(3, [gate[2], aux_bit, gate[3]], numvars)
        # res += decompose(3, [gate[0], aux_bit, gate[1]], numvars)
        res = [[aux_bit,gate[3]],[gate[2],aux_bit],[aux_bit,gate[3]],
                [gate[1],aux_bit],[gate[0],gate[1]],[gate[1],aux_bit],[gate[0],aux_bit],
                [aux_bit,gate[3]],[gate[2],aux_bit],[aux_bit,gate[3]],
                [gate[0],aux_bit],[gate[1],aux_bit],[gate[0],gate[1]],[gate[1],aux_bit]]
    elif qubit == 5:
        # 这里需要利用辅助比特
        # 求gate的差集，得到可用的辅助比特
        candidate = list(set(range(numvars)).difference(gate))
        dist = []
        for c in candidate:
            dist.append(reduce(lambda x,y: x+abs(y-c), gate)+abs(gate[0]-c))
        min = 999999999
        index = 0
        for i in range(len(dist)):
            if min > dist[i]:
                min = dist[i]
                index = i
        # print(candidate, dist, index, gate, numvars)
        aux_bit = candidate[index]
        res += decompose(3, [gate[3], aux_bit, gate[4]], numvars)
        res += decompose(4, [gate[0], gate[1], gate[2], aux_bit], numvars)
        res += decompose(3, [gate[3], aux_bit, gate[4]], numvars)
        res += decompose(4, [gate[0], gate[1], gate[2], aux_bit], numvars)
    else:
        raise ValueError('当前不支持量子门比特 '+str(qubit))
    return res

"""
Reference:
Qubit placement to minimize communication overhead in 2D quantum architectures
"""
def benchmark_manager():
    return {
        '3_17_13': {'raw':2, 'col':2, '2-gates': 13, 'result':6},
        '4_49_17': {'raw':2, 'col':2, '2-gates': 30, 'result':13},
        '4gt10-v1_81': {'raw':3, 'col':2, '2-gates': 36, 'result':16},
        '4gt11_84': {'raw':2, 'col':3, '2-gates': 7, 'result':2},
        # '4gt12-v1_89': {'raw':3, 'col':2, '2-gates': 52, 'result':19}, 
        '4gt13-v1_93': {'raw':3, 'col':3, '2-gates': 16, 'result':2},
        # '4gt4-v0_80': {'raw':2, 'col':3, '2-gates': 43, 'result':17},
        '4gt5_75': {'raw':2, 'col':4, '2-gates': 22, 'result':8},
        '4mod5-v1_23': {'raw':2, 'col':3, '2-gates': 24, 'result':11},
        # '4mod7-v0_95': {'raw':3, 'col':3, '2-gates': 40, 'result':13}, #4mod7-v0_95
        # 'aj-e11_165': {'raw':2, 'col':3, '2-gates': 59, 'result':24},
        'alu-v4_36': {'raw':2, 'col':3, '2-gates': 31, 'result':10},
        'decod24-v3_46': {'raw':3, 'col':2, '2-gates': 9, 'result':3},
        'ham7_104': {'raw':3, 'col':3, '2-gates': 87, 'result':48},
        'hwb4_52': {'raw':2, 'col':2, '2-gates': 23, 'result':9},
        'hwb5_55': {'raw':2, 'col':3, '2-gates': 106, 'result':45},
        'hwb6_58': {'raw':3, 'col':2, '2-gates': 146, 'result':79},
        # 'hwb7_62': {'raw':3, 'col':3, '2-gates': 2659, 'result':1688},
        # 'hwb8_118': {'raw':3, 'col':3, '2-gates': 16608, 'result':11027},
        # 'hwb9_123': {'raw':4, 'col':3, '2-gates': 20405, 'result':15022},
        'mod5adder_128': {'raw':3, 'col':2, '2-gates': 81, 'result':41},
        # 'mod8-10_177': {'raw':3, 'col':3, '2-gates': 108, 'result':45},
        'rd32-v0_67': {'raw':2, 'col':3, '2-gates': 8, 'result':2},
        # 'rd53_135': {'raw':5, 'col':2, '2-gates': 78, 'result':39},
        'rd73_140': {'raw':4, 'col':3, '2-gates': 76, 'result':37},
        # 'sym9_148': {'raw':4, 'col':4, '2-gates': 4452, 'result':2363},
        'sys6-v0_144': {'raw':4, 'col':4, '2-gates': 62, 'result':31},
        # 'urf1_149': {'raw':3, 'col':3, '2-gates': 57770, 'result':38555},
        'urf2_152': {'raw':4, 'col':2, '2-gates': 25150, 'result':16822},
        # 'urf5_158': {'raw':3, 'col':3, '2-gates': 51380, 'result':34406},
        # 'QFT5': {'raw':3, 'col':2, '2-gates': 10, 'result':5},
        # 'QFT6': {'raw':5, 'col':2, '2-gates': 15, 'result':6},
        # 'QFT7': {'raw':2, 'col':4, '2-gates': 21, 'result':18},
        # 'QFT8': {'raw':5, 'col':2, '2-gates': 28, 'result':18},
        # 'QFT9': {'raw':3, 'col':4, '2-gates': 36, 'result':34},
        # 'QFT10': {'raw':4, 'col':3, '2-gates': 45, 'result':53},
    }

if __name__ == '__main__':
    # names = ['3_17_13', '4_49_17', '4gt10-v1_81']
    test_names = ['3_17_13']
    for name in test_names:
        res = read_from_file(name)
        print('\n')
        print('文件 '+name+'\n')
        print(res['gates'])
