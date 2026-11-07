"""独立的可信反馈进程；不导入学生代码，使用GitHub当前PR信息关联结果。"""
import csv,io,json,math,os,sys,urllib.request
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from identity import identify

REPO=os.environ['GITHUB_REPOSITORY'];TOKEN=os.environ['GH_TOKEN'];MARKER='<!-- lab02-grade:'
def api(route,method='GET',data=None):
    req=urllib.request.Request('https://api.github.com'+route,method=method,data=None if data is None else json.dumps(data).encode(),headers={'Authorization':'Bearer '+TOKEN,'Accept':'application/vnd.github+json','Content-Type':'application/json'})
    with urllib.request.urlopen(req,timeout=45) as f:return json.loads(f.read() or '{}')

def pages(route):
    result=[];page=1
    while True:
        batch=api(route+('&' if '?' in route else '?')+f'per_page=100&page={page}');result.extend(batch)
        if len(batch)<100:return result
        page+=1

def own_grade(comments):
    for comment in reversed(comments):
        if comment['user']['login']!='github-actions[bot]' or MARKER not in comment['body']:continue
        encoded=comment['body'].split(MARKER,1)[1].split(' -->',1)[0]
        return json.loads(encoded)
    return None

def main():
    number=int(os.environ['PR_NUMBER']);pr=api(f'/repos/{REPO}/pulls/{number}')
    students=json.loads(os.environ['CLASS_ROSTER_JSON'])
    who=identify(pr['title'],students);run_url=f'https://github.com/{REPO}/actions/runs/{os.environ["GITHUB_RUN_ID"]}'
    report_path=Path('reports/grade_report.json');meta_path=Path('reports/submission.json')
    score=None;status='评分运行失败';details='查看运行链接中的失败步骤；本次未产生有效成绩。'
    if os.environ['GRADE_JOB_RESULT']=='success':
        report=json.loads(report_path.read_text(encoding='utf-8'));meta=json.loads(meta_path.read_text(encoding='utf-8'))
        if meta['pr_number']!=number:raise ValueError('报告PR编号不匹配')
        # 补交可能在前一次运行完成前发生，旧提交不能覆盖新提交的成绩。
        if meta['head_sha']!=pr['head']['sha']:
            print('Skipped stale revision; current revision has a separate grading run.');return
        score=report['score']
        if report['status']!='completed' or not isinstance(score,(int,float)) or not math.isfinite(score) or not 0<=score<=100:raise ValueError('评分报告值无效')
        status='已评分';details='\n'.join(f'- {k}：{v["score"]}/{v["max"]}，通过{v["passed"]}/{v["total"]}，{v["status"]}' for k,v in report['parts'].items())
    elif os.environ['GRADE_JOB_RESULT']=='cancelled':
        print('Cancelled superseded run; no current score overwritten.');return
    data={'sha':pr['head']['sha'],'score':score,'status':status,'identity':who,'run_url':run_url}
    identity_text=(who.get('name','')+' '+who.get('student_id','')) if who['status']!='invalid' else who['reason']
    text=f'## 实验二自动评分\n\n身份关联：{identity_text}\n\n'
    text+=(f'**自动成绩：{score}/100**' if score is not None else '**评分未完成，请查看失败日志；不是0分。**')
    text+=f'\n\n提交：`{pr["head"]["sha"]}`\n\n{details}\n\n[运行日志与评分附件]({run_url})\n\n'
    if who['status']=='invalid':text+='**成绩尚未关联班级名单。修改PR标题后会自动重评并关联，无需教师操作。**\n\n'
    text+='报告与AI记录分仅评价结构及交付完整性，不代表内容质量评价。\n\n'+MARKER+json.dumps(data,ensure_ascii=False)+' -->'
    comments=pages(f'/repos/{REPO}/issues/{number}/comments')
    existing=next((c for c in comments if c['user']['login']=='github-actions[bot]' and MARKER in c['body']),None)
    if existing:api(f'/repos/{REPO}/issues/comments/{existing["id"]}','PATCH',{'body':text})
    else:api(f'/repos/{REPO}/issues/{number}/comments','POST',{'body':text})
    refresh_board(students,publish=False)

def refresh_board(students,publish=True):
    prs=pages(f'/repos/{REPO}/pulls?state=all&sort=updated&direction=desc')
    records={};extras=[]
    for pr in prs:
        who=identify(pr['title'],students)
        result=own_grade(pages(f'/repos/{REPO}/issues/{pr["number"]}/comments'))
        row={'PR':str(pr['number']),'账号':pr['user']['login'],'提交':pr['head']['sha'],'链接':pr['html_url'],'状态':'待评分','成绩':''}
        if result and result['sha']==pr['head']['sha']:
            row['状态']=result['status'];row['成绩']='' if result['score'] is None else str(result['score'])
        if who['status']=='matched':
            sid=who['student_id']
            if sid not in records:records[sid]=row
        else:extras.append({**row,'身份状态':who['status']})
    fields=['序号','学号','姓名','是否提交','PR','账号','提交','状态','成绩','链接'];rows=[]
    for student in students:
        record=records.get(student['学号'])
        rows.append({'序号':student['序号'],'学号':student['学号'][:4]+'****'+student['学号'][-2:],'姓名':student['姓名'][0]+'**','是否提交':'是' if record else '否',
            'PR':'','账号':'','提交':'','状态':'未提交','成绩':'','链接':'',**(record or {})})
    folder=Path('tracking');folder.mkdir(exist_ok=True)
    with (folder/'student_grades.csv').open('w',encoding='utf-8-sig',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=fields);writer.writeheader();writer.writerows(rows)
    (folder/'unmatched_and_demo.json').write_text(json.dumps(extras,ensure_ascii=False,indent=2),encoding='utf-8')
    md='# 实验二37人成绩记录\n\n最新提交尚未评分时不沿用旧成绩；空白表示未提交或未完成评分。\n\n'
    md+='|名单序号|学号脱敏|姓名脱敏|提交|PR|状态|自动成绩|\n|---|---|---|---|---|---|---|\n'
    md+='\n'.join(f'|{r["序号"]}|{r["学号"]}|{r["姓名"]}|{r["是否提交"]}|{r["PR"]}|{r["状态"]}|{r["成绩"]}|' for r in rows)
    md+=f'\n\n未匹配或模拟提交：{len(extras)}，单独记录，不计入37人成绩。\n'
    (folder/'student_grades.md').write_text(md,encoding='utf-8')
    Path(os.environ['GITHUB_STEP_SUMMARY']).write_text(md,encoding='utf-8')
    if not publish:return
    issue=int(os.environ['TRACKING_ISSUE_NUMBER']);marker='<!-- lab02-class-board -->'
    comments=pages(f'/repos/{REPO}/issues/{issue}/comments')
    old=next((c for c in comments if c['user']['login']=='github-actions[bot]' and marker in c['body']),None)
    if old:api(f'/repos/{REPO}/issues/comments/{old["id"]}','PATCH',{'body':marker+'\n'+md})
    else:api(f'/repos/{REPO}/issues/{issue}/comments','POST',{'body':marker+'\n'+md})

if __name__=='__main__':main()
