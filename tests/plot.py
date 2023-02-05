import os, sys
src = os.path.join(os.path.dirname(__file__), '..')
sys.path.insert(0, src)

import numpy as np

from dhbw import dasp

x = dasp.timeline(1)
y = dasp.signal.harmonics(1000, 4, x)

dasp.plot.figure().spectrogram(x, y, 10e-3, 100e-3)
dasp.plot.figure().fft.abs(x, y)
dasp.plot.figure().signal(x, y)
dasp.plot.show()
