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
            'x6':6, 'x7':7, 'x8':8, 'x9':9, 'x10':10
        }
        numvars = 0
        for item in list:
            if item[0] == '#':
                pass
            elif item[0] == '.':
                if 'numvars' in item:
                    numvars = int(item.split(' ')[1])
            elif item[0] == 't':
                item = item.rstrip('\n')
                line = item.split(' ')
                q_num = int(line[0][1:])
                g = []
                for index in range(len(line)):
                    if index == 0:
                        continue
                    if line[index] in chars_table:
                        g.append(chars_table[line[index]])
                    else:
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
        '3_17_13': {'raw':2, 'col':2, 'ex':6},
        '4_49_17': {'raw':2, 'col':2, 'ex':13},
        '4gt10-v1_81': {'raw':3, 'col':2, 'ex':16},

    }

if __name__ == '__main__':
    # names = ['3_17_13', '4_49_17', '4gt10-v1_81']
    test_names = ['3_17_13']
    for name in test_names:
        res = read_from_file(name)
        print('\n')
        print('文件 '+name+'\n')
        print(res['gates'])
