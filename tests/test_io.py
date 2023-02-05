import os, sys
src = os.path.join(os.path.dirname(__file__), '..')
sys.path.insert(0, src)

import numpy as np
import unittest

from dhbw import dasp

class IoTest(unittest.TestCase):

    def setUp(self):

        self.t = dasp.timeline(1)
        self.x = dasp.signal.harmonic(440, self.t)

    def test_write(self):

        dasp.io.write('/tmp/dasp', self.x)

    def test_read(self):

        y, t, sr = dasp.io.read('/tmp/dasp')

        self.assertEqual(sr, dasp.SR)
        self.assertTrue(np.allclose(t, self.t))
        self.assertTrue(np.allclose(y, self.x, atol=1e-7))

    def test_play(self):

        dasp.io.play('/tmp/dasp')

if __name__ == '__main__':

    unittest.main()
