"""
自定义日志，用于打印及调试
"""
class Log:
    def __init__(self) -> None:
        pass

    def print_exec_list(self, exec_list):
        tags = []
        for node in exec_list:
            tags.append(node.tag+' '+str(node.value[0])+' '+str(node.value[1]))
        print('exec_list', tags)
    
    def log_in_file(self, *args):
        msg = ''
        for a in args:
            msg += str(a)+' '
        with open('logger.log', 'a') as f:
            f.write(msg+'\n')
            pass