"""使用名单中的姓名和完整学号关联，不按昵称猜测学生身份。"""
import re

def identify(title,students):
    if title.startswith('[流程测试]'):
        return {'status':'demo','student_id':'LAB02-DEMO','name':'模拟学生'}
    match=re.fullmatch(r'现代交换实验02-([^-]+)-(\d+)',title.strip())
    if not match:return {'status':'invalid','reason':'PR标题应为：现代交换实验02-本人姓名-完整学号'}
    name,sid=match.groups();student=next((s for s in students if s['学号']==sid),None)
    if student is None or student['姓名']!=name:
        return {'status':'invalid','reason':'姓名或学号与班级名单不一致，请修改PR标题'}
    return {'status':'matched','student_id':sid,'name':name}
