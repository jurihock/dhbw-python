import os, sys
src = os.path.join(os.path.dirname(__file__), '..')
sys.path.insert(0, src)

import numpy as np

from dhbw import dasp

sr = dasp.SR
cp = dasp.CP

t = dasp.timeline(1, sr)
x = dasp.signal.harmonic(cp, t)

dasp.io.write('/tmp/dasp', x)
y, t1, sr1 = dasp.io.read('/tmp/dasp')

assert sr == sr1
assert np.allclose(t, t1)
assert np.allclose(x, y, atol=1e-7)

dasp.io.play('/tmp/dasp')
