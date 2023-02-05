import os, sys
src = os.path.join(os.path.dirname(__file__), '..')
sys.path.insert(0, src)

import numpy as np

from dhbw import dasp

t = dasp.timeline(1)
x = dasp.signal.noise(t)
z = dasp.fft.fft(x, window='rect')
y = dasp.fft.ifft(z)

assert np.allclose(x, y)
