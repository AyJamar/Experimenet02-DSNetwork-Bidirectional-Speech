from copy import deepcopy
from src.models import Endpoint as E,Tables
from src.connections import connect_pair,disconnect_pair
def setup_pairs():
    t=Tables();connect_pair('A',E(0,1),E(1,5),t);connect_pair('B',E(0,2),E(1,6),t);return t
def test_remove_both_directions():
    t=Tables();connect_pair('A',E(0,1),E(1,5),t);assert disconnect_pair('A',t) is True and t==Tables()
def test_preserve_other_pair():
    t=setup_pairs();assert disconnect_pair('A',t);assert t.t_maps==[{6:2},{2:6}] and t.s_map=={(1,6):0,(0,2):1} and set(t.pairs)=={'B'}
def test_unknown_unchanged():
    t=setup_pairs();old=deepcopy(t);assert disconnect_pair('unknown',t) is False and t==old
def test_repeat_release():
    t=setup_pairs();disconnect_pair('A',t);old=deepcopy(t);assert disconnect_pair('A',t) is False and t==old
def test_reuse_after_release():
    t=setup_pairs();disconnect_pair('A',t);assert connect_pair('C',E(0,1),E(1,5),t)
