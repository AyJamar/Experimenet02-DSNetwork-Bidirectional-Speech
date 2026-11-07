"""教师开发测试，不计入学生100分。"""
import importlib.util
from pathlib import Path
spec=importlib.util.spec_from_file_location('identity',Path(__file__).parents[1]/'automation/identity.py')
module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
students=[{'学号':'2023000001','姓名':'示例学生'}]
def test_match_requires_name_and_id():
    assert module.identify('现代交换实验02-示例学生-2023000001',students)['status']=='matched'
def test_wrong_name_not_matched():
    assert module.identify('现代交换实验02-别人-2023000001',students)['status']=='invalid'
def test_nickname_not_matched():
    assert module.identify('完成实验二',students)['status']=='invalid'
def test_demo_separate():
    assert module.identify('[流程测试] 实验二',students)['status']=='demo'
