"""
主流程文件
"""
from dag import DAG
from utils import read_from_file
from cp import CP

def main_process(gates, numvars):
    dag = DAG(gates, numvars)

if __name__ == '__main__':
    names = ['3_17_13', '4_49_17', '4gt10-v1_81']
    for name in names:
        res = read_from_file(name)
        print('文件 '+name, '2-门数 '+str(len(res['gates'])))
        main_process(res['gates'], res['numvars'])
