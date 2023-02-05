import os, sys
src = os.path.join(os.path.dirname(__file__), '..')
sys.path.insert(0, src)

import numpy as np
import unittest

from dhbw import dasp

class StftTest(unittest.TestCase):

    def test_stft(self):

        w = 1024
        h = w//4

        t = dasp.timeline(1)
        x = dasp.signal.noise(t)
        z = dasp.stft.stft(x, w, h)
        y = dasp.stft.istft(z, w, h)

        self.assertGreaterEqual(y.size, x.size)
        n = min(x.size, y.size)

        x.resize(n)
        y.resize(n)

        x = x[+w:-w]
        y = y[+w:-w]

        self.assertTrue(np.allclose(x, y))

if __name__ == '__main__':

    unittest.main()
