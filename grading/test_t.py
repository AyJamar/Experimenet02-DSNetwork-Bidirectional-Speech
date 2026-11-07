import numpy as np
import pytest
from src.t_switch import t_switch
from src.models import IDLE
def test_output_to_input():
    x=np.arange(32,dtype=np.uint8);y=t_switch(x,{1:3,3:1});assert y[1]==3 and y[3]==1
def test_empty_idle_and_reserved():
    x=np.arange(32,dtype=np.uint8);y=t_switch(x,{});assert y[0]==0 and y[16]==16 and y[7]==IDLE
def test_no_input_mutation():
    x=np.arange(32,dtype=np.uint8);before=x.copy();y=t_switch(x,{31:2});assert np.array_equal(x,before) and y[31]==2 and y.dtype==np.uint8
def test_reserved_rejected():
    for m in ({0:1},{1:16},{16:2}):
        with pytest.raises(ValueError):t_switch(np.zeros(32,dtype=np.uint8),m)
def test_out_of_range_rejected():
    for m in ({32:1},{1:-1}):
        with pytest.raises(ValueError):t_switch(np.zeros(32,dtype=np.uint8),m)
def test_arbitrary_byte_values():
    x=np.array([(i*37+19)%256 for i in range(32)],dtype=np.uint8);y=t_switch(x,{8:31,5:2});assert y[8]==x[31] and y[5]==x[2]
