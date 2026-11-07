"""只下载学生任务文件和提交产物，不在教师进程中导入学生代码。"""
import io,json,os,shutil,stat,urllib.request,zipfile
from pathlib import Path

REPO=os.environ['GITHUB_REPOSITORY'];TOKEN=os.environ['GH_TOKEN']
def api(route):
    req=urllib.request.Request('https://api.github.com'+route,headers={'Authorization':'Bearer '+TOKEN,'Accept':'application/vnd.github+json'})
    with urllib.request.urlopen(req,timeout=45) as f:return json.load(f)

def main():
    number=int(os.environ['PR_NUMBER']);pr=api(f'/repos/{REPO}/pulls/{number}')
    if pr['state']!='open':raise RuntimeError('PR已关闭，本次不执行评分')
    stage=Path('submission-work');stage.mkdir()
    shutil.copytree('src',stage/'src');shutil.copytree('grading',stage/'grading')
    (stage/'student_tests').mkdir();(stage/'results').mkdir()
    meta={'pr_number':number,'head_sha':pr['head']['sha'],'title':pr['title'],'login':pr['user']['login'],'html_url':pr['html_url']}
    Path('reports').mkdir();Path('reports/submission.json').write_text(json.dumps(meta,ensure_ascii=False),encoding='utf-8')
    # 仅从API确认的当前提交读取，文件名不参与shell命令构造。
    url=f'https://api.github.com/repos/{pr["head"]["repo"]["full_name"]}/zipball/{pr["head"]["sha"]}'
    request=urllib.request.Request(url,headers={'Authorization':'Bearer '+TOKEN})
    with urllib.request.urlopen(request,timeout=60) as f:raw=f.read(20*1024*1024+1)
    if len(raw)>20*1024*1024:raise ValueError('提交归档超过20MiB，不能评分')
    total=0
    with zipfile.ZipFile(io.BytesIO(raw)) as archive:
        for item in archive.infolist():
            path=Path(*Path(item.filename).parts[1:]);name=path.as_posix()
            allowed=name in {'src/t_switch.py','src/s_switch.py','src/connections.py','REPORT.md','AI_LOG.md'} or \
                (len(path.parts)==2 and path.parts[0]=='student_tests' and path.name.startswith('test_') and path.suffix=='.py') or \
                name in {'results/transfer_check.json','results/control_tables.json','results/switch_mapping.png'}
            if not allowed:continue
            if '..' in path.parts or path.is_absolute() or stat.S_ISLNK(item.external_attr>>16):raise ValueError('提交包含非法路径或符号链接')
            total+=item.file_size
            if item.file_size>2*1024*1024 or total>10*1024*1024:raise ValueError('评分输入文件超过大小限制')
            dest=stage/path;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(archive.read(item))
    print(f'Prepared PR #{number}, commit {meta["head_sha"][:12]}; only designated files staged.')

if __name__=='__main__':main()
