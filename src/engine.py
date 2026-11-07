"""教师框架：一帧缓存与可手算的字节模式，不要求操作系统实时调度。"""
import numpy as np
from src.models import SLOTS, LINKS
from src.t_switch import t_switch
from src.s_switch import s_switch

def sample_frame(frame_id=0):
    return np.array([[(link*101+slot*3+frame_id*17)%256 for slot in range(SLOTS)] for link in range(LINKS)],dtype=np.uint8)

def exchange_frame(frames,tables):
    temporal=np.stack([t_switch(frames[i],tables.t_maps[i]) for i in range(LINKS)])
    return s_switch(temporal,tables.s_map)

def run_frames(frames,tables):
    """输入帧k的交换结果在输出帧k+1可用；S不再追加一帧。"""
    return [{'input_frame_id':k,'available_frame_id':k+1,'output':exchange_frame(frame,tables)} for k,frame in enumerate(frames)]
