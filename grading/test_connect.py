from copy import deepcopy
import pytest
from src.models import Endpoint as E,Tables
from src.connections import connect_pair
def test_both_directions():
    t=Tables();assert connect_pair('A',E(0,1),E(1,5),t) is True
    assert t.t_maps==[{5:1},{1:5}] and t.s_map=={(1,5):0,(0,1):1} and set(t.pairs)=={'A'}
def test_two_pairs():
    t=Tables();assert connect_pair('A',E(0,1),E(1,5),t);assert connect_pair('B',E(0,2),E(1,6),t);assert len(t.pairs)==2
def test_same_link():
    t=Tables();assert connect_pair('A',E(0,1),E(0,3),t);assert t.t_maps[0]=={3:1,1:3} and t.s_map=={(0,3):0,(0,1):0}
def test_endpoint_conflict_atomic():
    t=Tables();connect_pair('A',E(0,1),E(1,5),t);old=deepcopy(t)
    assert connect_pair('B',E(0,2),E(1,5),t) is False and t==old
def test_duplicate_id_atomic():
    t=Tables();connect_pair('A',E(0,1),E(1,5),t);old=deepcopy(t)
    assert connect_pair('A',E(0,2),E(1,6),t) is False and t==old
def test_internal_t_conflict_atomic():
    t=Tables();connect_pair('A',E(0,1),E(1,5),t);old=deepcopy(t)
    assert connect_pair('B',E(0,2),E(0,5),t) is False and t==old
def test_same_timeslot_other_links():
    t=Tables();assert connect_pair('A',E(0,7),E(1,7),t);assert t.s_map=={(1,7):0,(0,7):1}
def test_invalid_endpoints():
    for a,b in [(E(0,0),E(1,5)),(E(2,1),E(1,5)),(E(0,1),E(0,1))]:
        t=Tables()
        with pytest.raises(ValueError):connect_pair('A',a,b,t)
        assert t==Tables()
