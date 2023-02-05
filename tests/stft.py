import os, sys
src = os.path.join(os.path.dirname(__file__), '..')
sys.path.insert(0, src)

import numpy as np

from dhbw import dasp

w = 1024
h = w//4

t = dasp.timeline(1)
x = dasp.signal.noise(t)
z = dasp.stft.stft(x, w, h)
y = dasp.stft.istft(z, w, h)

assert y.size >= x.size
n = min(x.size, y.size)

x.resize(n)
y.resize(n)

x = x[+w:-w]
y = y[+w:-w]

assert np.allclose(x, y)
