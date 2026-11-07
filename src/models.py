"""教师提供的端口与控制表；控制表统一采用输出指向输入。"""
from dataclasses import dataclass, field

SLOTS=32
LINKS=2
RESERVED={0,16}
IDLE=0xD5

@dataclass
class Endpoint:
    link_id: int
    timeslot: int

@dataclass
class Tables:
    t_maps: list = field(default_factory=lambda:[{},{}])
    s_map: dict = field(default_factory=dict)
    pairs: dict = field(default_factory=dict)

def validate_endpoint(endpoint):
    if endpoint.link_id not in range(LINKS) or endpoint.timeslot not in range(SLOTS) or endpoint.timeslot in RESERVED:
        raise ValueError('端口必须使用链路0/1与TS1至TS31中的业务时隙，不能使用TS16')

def directions(a,b):
    """每个方向先在输入链路改成目的时隙，再在S单元改链路。"""
    return [(a,b),(b,a)]

def snapshot(tables):
    return {'t_maps':[{str(k):v for k,v in m.items()} for m in tables.t_maps],
            's_map':{f'{link}:{slot}':src for (link,slot),src in tables.s_map.items()},
            'pairs':{k:[[a.link_id,a.timeslot],[b.link_id,b.timeslot]] for k,(a,b) in tables.pairs.items()}}
