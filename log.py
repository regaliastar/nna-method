"""
自定义日志，用于打印及调试
"""
class Log:
    def __init__(self) -> None:
        self.env = 'debug'
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
    
    def set_env(self, env):
        self.env = env

    def print_current(self, current, context):
        if self.env == 'debug':
            info = {
                'tags': [],
                'gates': []
            }
            for node in current:
                info['tags'].append(node.tag)
                info['gates'].append(node.value)
            print(context, 'print_current', info)

    def print(self, *args):
        if self.env == 'debug':
            print(args)
        