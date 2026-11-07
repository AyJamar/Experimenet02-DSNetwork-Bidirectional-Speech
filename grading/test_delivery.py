import ast,json
from pathlib import Path
def test_transfer_evidence():
    obj=json.loads(Path('results/transfer_check.json').read_text(encoding='utf-8'))
    assert len(obj['checks'])==16 and obj['mismatches']==0 and obj['latency_frames']==1
    for row in obj['checks']:
        assert row['expected']==row['actual'] and row['available_frame_id']==row['input_frame_id']+1
        link,slot=row['source'];assert row['expected']==(link*101+slot*3+row['input_frame_id']*17)%256
    assert obj['release_ok'] and obj['survivor_ok'] and obj['conflict_rejected']
def test_control_evidence():
    obj=json.loads(Path('results/control_tables.json').read_text(encoding='utf-8'))
    assert obj['before_release']['t_maps']==[{'5':1,'6':2},{'1':5,'2':6}]
    assert obj['after_release']['t_maps']==[{'6':2},{'2':6}] and set(obj['after_release']['pairs'])=={'C2'}
def test_result_image():
    from PIL import Image
    with Image.open('results/switch_mapping.png') as im:
        im.verify()
    assert Path('results/switch_mapping.png').stat().st_size>1000
def test_report_structure():
    text=Path('REPORT.md').read_text(encoding='utf-8');assert len(text)>=300
    assert all('# '+title in text for title in ['原理与手算','结果分析','反例与验证','局限'])
    assert 'TODO' not in text and '待填写' not in text
def test_ai_record_structure():
    text=Path('AI_LOG.md').read_text(encoding='utf-8');assert len(text)>=120
    assert all('# '+title in text for title in ['需求','建议与采纳','验证证据'])
    assert 'TODO' not in text and '待填写' not in text
