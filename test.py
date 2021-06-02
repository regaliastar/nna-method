from process import init_map_process
from process import swap_process
from utils import read_from_file
from utils import benchmark_manager

if __name__ == '__main__':
    benchmark = benchmark_manager()
    for name in benchmark:
        res = read_from_file(name)
        print('文件 '+name, '2-门数 '+str(len(res['gates'])), '\n')
        placement = init_map_process(benchmark[name]['raw'], benchmark[name]['col'], res['numvars'], res['gates'])
        print('\n', 'placement:', placement, '\n')
        swap_path = swap_process(benchmark[name]['raw'], benchmark[name]['col'], res['numvars'], res['gates'], placement['placement'])
        print(name, '总共插入交换门：', str(len(swap_path)))
