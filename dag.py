"""
根据gates生成DAG图
基于拓扑排序的选择算法
"""
class DAG:
    def __init__(self, gates, numvars) -> None:
        self.current = []
        # 记录每一条导线最后的gate
        self.end = [-1]*numvars
        self.defer_gates = []
        index = 1
        for gate in gates:
            tag = 'g'+str(index)
            index += 1
            node = Node(gate, tag)
            if self.end[node.value[0]] == -1 and self.end[node.value[1]] == -1:
                self.current.append(node)
            elif self.end[node.value[0]] != -1 and self.end[node.value[1]] == -1:
                father = self.end[node.value[0]]
                self.add_gate(node, father)
            elif self.end[node.value[0]] == -1 and self.end[node.value[1]] != -1:
                father = self.end[node.value[1]]
                self.add_gate(node, father)
            elif self.end[node.value[0]] != -1 and self.end[node.value[1]] != -1:
                father0 = self.end[node.value[0]]
                father1 = self.end[node.value[1]]
                self.add_gate(node, father0)
                self.add_gate(node, father1)
            self.end[node.value[0]] = node
            self.end[node.value[1]] = node
            
    def add_gate(self, now, father):
        if now in father.next:
            return
        father.next.append(now)
        now.fathers.append(father)
    
    def del_gate(self, node):
        if node not in self.current:
            raise ValueError('del_gate必须在dag.current内', node.tag)
        self.current.remove(node)
        for n in node.next:
            if n not in self.current:
                self.current.append(n)
    
    def get_current_node_by_tag(self, tag):
        for node in self.current:
            if node.tag == tag:
                return node
        return None

    # 批量删除，若flag为True，则执行删除操作
    def defer_del_gate(self, flag, node=None):
        if not flag:
            self.defer_gates.append(node)
        else:
            for node in self.defer_gates:
                n = self.get_current_node_by_tag(node.tag)
                self.del_gate(n)
            self.defer_gates.clear()

    # dfs遍历
    def print(self, nodes):
        if nodes == None or len(nodes) == 0:
            return
        for c in nodes:
            if not c.visited:
                print(c.tag)
                c.visited = True
                self.print(c.next)

class Node:
    def __init__(self, value, tag=None) -> None:
        self.value = value
        self.tag = tag
        self.next = []
        self.fathers = []
        self.visited = False

if __name__ == '__main__':
    gates = [[0, 3], [1, 3], [3, 4], [0, 2], [2, 3], [0, 1]]
    dag = DAG(gates, 5)
    print('dag.current[0]', dag.current[0].tag)
    dag.del_gate(dag.current[0])
    print('dag.current[0]', dag.current[0].tag)
    print('-----------')
    dag.print(dag.current)