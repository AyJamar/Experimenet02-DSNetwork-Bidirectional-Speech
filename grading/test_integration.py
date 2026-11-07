from copy import deepcopy
from src.models import Endpoint as E,Tables,IDLE
from src.connections import connect_pair,disconnect_pair
from src.engine import sample_frame,run_frames,exchange_frame
def test_bidirectional_bytes():
    t=Tables();connect_pair('A',E(0,1),E(1,5),t);x=sample_frame(2);y=exchange_frame(x,t)
    assert y[1,5]==x[0,1] and y[0,1]==x[1,5]
def test_one_frame_latency():
    t=Tables();connect_pair('A',E(0,1),E(1,5),t);frames=[sample_frame(k) for k in range(4)];out=run_frames(frames,t)
    for k,r in enumerate(out):assert r['input_frame_id']==k and r['available_frame_id']==k+1 and r['output'][1,5]==frames[k][0,1]
def test_conflict_keeps_original_transfer():
    t=Tables();connect_pair('A',E(0,1),E(1,5),t);assert not connect_pair('B',E(0,2),E(1,5),t)
    x=sample_frame();assert exchange_frame(x,t)[1,5]==x[0,1]
def test_release_idle_and_survivor():
    t=Tables();connect_pair('A',E(0,1),E(1,5),t);connect_pair('B',E(0,2),E(1,6),t);disconnect_pair('A',t)
    x=sample_frame();y=exchange_frame(x,t);assert y[0,1]==IDLE and y[1,5]==IDLE and y[1,6]==x[0,2] and y[0,2]==x[1,6]
def test_idle_byte_is_not_free_resource():
    t=Tables();connect_pair('A',E(0,1),E(1,5),t);x=sample_frame();x[0,1]=IDLE
    assert exchange_frame(x,t)[1,5]==IDLE and not connect_pair('B',E(0,1),E(1,6),t)
