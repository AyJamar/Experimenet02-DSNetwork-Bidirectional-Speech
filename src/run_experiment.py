"""教师框架：执行双连接、冲突拒绝与释放，生成学生自己的结果。"""
import json
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from src.models import Endpoint, Tables, snapshot, IDLE
from src.connections import connect_pair, disconnect_pair
from src.engine import sample_frame,run_frames

def run(output='results'):
    dest=Path(output);dest.mkdir(parents=True,exist_ok=True)
    t=Tables();a,b=Endpoint(0,1),Endpoint(1,5);c,d=Endpoint(0,2),Endpoint(1,6)
    assert connect_pair('C1',a,b,t)
    assert connect_pair('C2',c,d,t)
    before=snapshot(t)
    rejected=connect_pair('conflict',a,Endpoint(1,7),t)
    assert rejected is False and snapshot(t)==before
    frames=[sample_frame(i) for i in range(4)]
    records=run_frames(frames,t);checks=[]
    for k,record in enumerate(records):
        out=record['output'];inp=frames[k]
        for name,x,y in [('C1',a,b),('C2',c,d)]:
            for src,dst in [(x,y),(y,x)]:
                checks.append({'connection':name,'input_frame_id':k,'available_frame_id':record['available_frame_id'],
                    'source':[src.link_id,src.timeslot],'destination':[dst.link_id,dst.timeslot],
                    'expected':int(inp[src.link_id,src.timeslot]),'actual':int(out[dst.link_id,dst.timeslot])})
    assert all(row['expected']==row['actual'] for row in checks)
    assert disconnect_pair('C1',t)
    after=run_frames([frames[0]],t)[0]['output']
    release_ok=bool(after[b.link_id,b.timeslot]==IDLE and after[a.link_id,a.timeslot]==IDLE)
    survivor_ok=bool(after[d.link_id,d.timeslot]==frames[0][c.link_id,c.timeslot] and after[c.link_id,c.timeslot]==frames[0][d.link_id,d.timeslot])
    assert release_ok and survivor_ok
    data={'checks':checks,'mismatches':sum(r['actual']!=r['expected'] for r in checks),'conflict_rejected':not rejected,
          'release_ok':release_ok,'survivor_ok':survivor_ok,'latency_frames':1}
    (dest/'transfer_check.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
    (dest/'control_tables.json').write_text(json.dumps({'before_release':before,'after_release':snapshot(t)},ensure_ascii=False,indent=2),encoding='utf-8')
    fig,ax=plt.subplots(figsize=(10,4))
    x=np.arange(32)
    ax.plot(x,frames[0][0],'.-',label='Input link 0');ax.plot(x,frames[0][1],'.-',label='Input link 1')
    ax.plot([1,2],[records[0]['output'][0,1],records[0]['output'][0,2]],'s',label='Connected outputs link 0')
    ax.plot([5,6],[records[0]['output'][1,5],records[0]['output'][1,6]],'x',markersize=10,label='Connected outputs link 1')
    ax.set(xlabel='Timeslot',ylabel='PCM byte',title='T-S bidirectional switching, input frame 0 -> output frame 1')
    ax.legend(fontsize=8);ax.grid(alpha=.25);fig.tight_layout();fig.savefig(dest/'switch_mapping.png',dpi=160);plt.close(fig)
    print('16 direction/frame checks passed; conflict rejected; release and surviving pair verified.')
    return data

if __name__=='__main__':run()
