"""
读取benchmark中的文件，将其转换成门约束格式如：[[0, 3], [1, 3], [3, 4], [0, 2], [2, 3], [0, 1]]

benckmark: Qubit placement to minimize communication overhead in 2D quantum architectures
"""

def read_from_file(names):
    res = []
    if len(names) == 0:
        return res
    for name in names:
        filename = 'benchmark/'+name+'.real'
        with open(filename, 'r') as f:
            list = f.readlines()
            chars = []
            for item in list:
                if item[0] == '#':
                    pass
                elif item[0] == '.':
                    if('numvars' in item):
                        vars = item.split(' ')
                        
    return res

"""
分解3比特门
[a,b,c] => [[b,c],[a,b],[b,c],[a,b],[a,c]], [[a,c],[a,b],[b,c],[a,b],[b,c]]
"""
def decompose(gate):
    pass

if __name__ == '__main__':
    names = ['4mod5-v1_22', 'mod5mils_65']
    read_from_file(names)
    pass