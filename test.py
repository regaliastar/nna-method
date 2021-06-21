from process import init_map_process
from process import swap_process
from utils import read_from_file
from utils import benchmark_manager
from log import Log

logger = Log()

if __name__ == '__main__':
    benchmark = benchmark_manager()
    improve = {}
    for name in benchmark:
        logger.log_in_file(name)
        res = read_from_file(name)
        if len(res['gates']) != benchmark[name]['2-gates']:
            print(name, '2-gates数量不匹配', len(res['gates']), benchmark[name]['2-gates'])
            logger.log_in_file(name, '2-gates数量不匹配', len(res['gates']), benchmark[name]['2-gates'])
        print('文件 '+name, '2-门数 '+str(len(res['gates'])), '\n')
        placement = init_map_process(benchmark[name]['raw'], benchmark[name]['col'], res['numvars'], res['gates'])
        print('\n', 'placement:', placement, '\n')
        swap_path = swap_process(benchmark[name]['raw'], benchmark[name]['col'], res['numvars'], res['gates'], placement['placement'])
        improve[name] = (benchmark[name]['result'] - len(swap_path))/benchmark[name]['result']
        logger.log_in_file(name, '总共插入交换门：', benchmark[name]['result'], '对照',  str(len(swap_path)), improve[name])
    avg_imp = 0
    for imp in improve:
        avg_imp += improve[imp]
    print('improve', improve)
    print('平均improve', str(avg_imp/len(improve)))
    logger.log_in_file('平均improve', str(avg_imp/len(improve)))