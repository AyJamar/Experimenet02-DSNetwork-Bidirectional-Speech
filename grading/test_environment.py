import numpy as np
from src.models import Tables
from src.engine import sample_frame
def test_frame_shape():
    f=sample_frame();assert f.shape==(2,32) and f.dtype==np.uint8
def test_independent_tables():
    a,b=Tables(),Tables();a.t_maps[0][1]=3;assert b.t_maps==[{},{}] and a.t_maps[1]=={}
