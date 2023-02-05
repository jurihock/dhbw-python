import os, sys
src = os.path.join(os.path.dirname(__file__), '..')
sys.path.insert(0, src)

import numpy as np
import unittest

from dhbw import dasp

class PlotTest(unittest.TestCase):

    def test_plot(self):

        x = dasp.timeline(1)
        y = dasp.signal.harmonics(1000, 4, x)

        dasp.plot.figure().spectrogram(x, y, 10e-3, 100e-3)
        dasp.plot.figure().fft.abs(x, y)
        dasp.plot.figure().signal(x, y)
        dasp.plot.show()

if __name__ == '__main__':

    unittest.main()
