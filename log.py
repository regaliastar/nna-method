"""
自定义日志，用于打印及调试
"""
class Log:
    def __init__(self) -> None:
        pass

    def print_exec_list(self, exec_list):
        tags = []
        for node in exec_list:
            tags.append(node.tag)
        print('exec_list', tags)