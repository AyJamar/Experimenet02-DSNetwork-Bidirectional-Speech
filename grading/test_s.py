import numpy as np
import pytest
from src.s_switch import s_switch
from src.models import IDLE
from src.engine import sample_frame
def test_changes_link_not_slot():
    x=sample_frame();y=s_switch(x,{(0,3):1,(1,3):0});assert y[0,3]==x[1,3] and y[1,3]==x[0,3] and y[1,4]==IDLE
def test_independent_slot_choices():
    x=sample_frame();y=s_switch(x,{(0,2):1,(0,5):0});assert y[0,2]==x[1,2] and y[0,5]==x[0,5]
def test_reserved_and_idle():
    x=sample_frame();y=s_switch(x,{});assert np.array_equal(y[:,[0,16]],x[:,[0,16]]) and (y[:,7]==IDLE).all()
def test_invalid_mapping():
    for m in ({(2,1):0},{(0,1):2},{(0,16):1},{(0,32):1}):
        with pytest.raises(ValueError):s_switch(sample_frame(),m)
def test_input_unchanged():
    x=sample_frame();old=x.copy();y=s_switch(x,{(0,31):1});assert np.array_equal(x,old) and y.dtype==np.uint8
