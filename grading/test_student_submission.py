"""只检查自拟测试的最低可执行要求，不判断创新性。"""
import ast,subprocess,sys
from pathlib import Path
def test_student_case_exists_and_runs():
    files=list(Path('student_tests').glob('test_*.py'));assert files,'请提交自拟test_*.py'
    tree=ast.parse('\n'.join(p.read_text(encoding='utf-8') for p in files))
    assert any(isinstance(n,ast.Assert) for n in ast.walk(tree))
    names={'t_switch','s_switch','connect_pair','disconnect_pair','exchange_frame'}
    assert any(isinstance(n,ast.Call) and (getattr(n.func,'id',None) in names or getattr(n.func,'attr',None) in names) for n in ast.walk(tree))
    r=subprocess.run([sys.executable,'-m','pytest','student_tests','-q','-p','no:cacheprovider'],capture_output=True,text=True,timeout=30)
    assert r.returncode==0,r.stdout+r.stderr
