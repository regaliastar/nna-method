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
                node.refer += 1
                self.add_gate(node, father)
            elif self.end[node.value[0]] == -1 and self.end[node.value[1]] != -1:
                father = self.end[node.value[1]]
                node.refer += 1
                self.add_gate(node, father)
            elif self.end[node.value[0]] != -1 and self.end[node.value[1]] != -1:
                father0 = self.end[node.value[0]]
                father1 = self.end[node.value[1]]
                if father0.tag == father1.tag:
                    node.refer += 1
                    self.add_gate(node, father0)
                else:
                    node.refer += 2
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
            n.refer -= 1
            if n not in self.current and n.refer == 0:
                self.current.append(n)
    
    def get_current_node_by_tag(self, tag):
        for node in self.current:
            if node.tag == tag:
                return node
        return None

    # 取num个node，若不足则广度优先搜索
    def get_current_more(self, _num):
        if len(self.current) >= _num:
            return self.current[0:_num-1]
        next = self.current[:]
        num = _num - len(self.current)
        MAXN = 10
        while len(next) < MAXN and num > 0:
            old_len = len(next)
            _next = []
            for n in next:
                _next += n.next
            next += _next
            if len(next) == old_len:
                break
            num -= len(next)-old_len
        return next[0: _num]

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
    def print_all(self, nodes):
        if nodes == None or len(nodes) == 0:
            return
        for c in nodes:
            if not c.visited:
                print(c.tag)
                c.visited = True
                self.print(c.next)

    def print_current(self):
        tags = []
        for node in self.current:
            tags.append(node.tag)
        print('print_current', tags)

class Node:
    def __init__(self, value, tag=None) -> None:
        self.value = value
        self.tag = tag
        self.next = []
        self.fathers = []
        self.visited = False
        self.refer = 0  # 入度，表示当前被引用数

if __name__ == '__main__':
    gates = [[3, 1], [2, 3], [3, 1], [4, 3], [0, 4], [4, 3], [0, 3]]
    dag = DAG(gates, 5)
    dag.print_current()
    dag.del_gate(dag.current[0])
    dag.print_current()
    dag.del_gate(dag.current[0])
    dag.print_current()
    print('-----------')
    dag.print(dag.current)