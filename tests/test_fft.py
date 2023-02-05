import os, sys
src = os.path.join(os.path.dirname(__file__), '..')
sys.path.insert(0, src)

import numpy as np
import unittest

from dhbw import dasp

class FftTest(unittest.TestCase):

    def test_fft(self):

        t = dasp.timeline(1)
        x = dasp.signal.noise(t)
        z = dasp.fft.fft(x, window='rect')
        y = dasp.fft.ifft(z)

        self.assertTrue(np.allclose(x, y))

if __name__ == '__main__':

    unittest.main()
