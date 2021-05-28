"""
根据gates生成DAG图
基于拓扑排序的选择算法
"""
class DAG:
    def __init__(self, gates, numvars) -> None:
        self.current = []
        # 记录每一条导线最后的gate
        self.end = [-1]*numvars
        index = 1
        for gate in gates:
            tag = 'g'+str(index)
            index += 1
            node = Node(gate, tag)
            if self.end[node.value[0]] == -1 and self.end[node.value[1]] == -1:
                self.current.append(node)
                self.end[node.value[0]] = node
                self.end[node.value[1]] = node
            elif self.end[node.value[0]] != -1:
                father = self.end[node.value[0]]
                self.add_gate(node, [father])
            elif self.end[node.value[1]] != -1:
                father = self.end[node.value[1]]
                self.add_gate(node, [father])

    def add_gate(self, now, fathers=None):
        for f in fathers:
            f.next.append(now)
            now.fathers.append(f)
    
    def del_gate(self):
        pass
    
    # 按层遍历
    def print(self, nodes):
        if nodes == None or len(nodes) == 0:
            return
        for c in nodes:
            print(c.tag)
            self.print(c.next)

class Node:
    def __init__(self, value, tag=None) -> None:
        self.value = value
        self.tag = tag
        self.next = []
        self.fathers = []

if __name__ == '__main__':
    gates = [[0, 3], [1, 3], [3, 4], [0, 2], [2, 3], [0, 1]]
    dag = DAG(gates, 5)
    print(dag.current[0].tag)
    print('-----------')
    dag.print(dag.current)