"""环境自检，不调用尚未实现的学生函数。"""
import numpy,matplotlib,pytest
from src.models import Tables,IDLE
if __name__=='__main__':
    assert len(Tables().t_maps)==2 and 0<=IDLE<=255
    print('Environment OK: NumPy, Matplotlib, pytest; 2 links x 32 slots.')
