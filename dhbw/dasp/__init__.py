"""
Digital Audio Signal Processing.
"""


import numpy

from . import fft
from . import filter
from . import io
from . import math
from . import pitch
from . import plot
from . import signal
from . import stft


CP = 440
"""Default concert pitch in hertz."""

SR = 44100
"""Default sample rate in hertz."""


def timeline(d, sr=None):
    """
    Returns an array of time points representing a
    discrete timeline of the specified duration in seconds
    and sample rate in hertz which defaults to 44100 Hz.

    Parameters
    ----------
    d : int, float
        Total timeline length in seconds.
    sr : int, float, optional
        Sample rate in hertz.
    """

    sr = sr if sr is not None else SR

    return numpy.arange(0, d, 1 / sr)


class log:
    """
    Basic logger for package internal purposes.
    """

    enable = False
    """Enable or disable the log output."""

    def echo(message):
        """
        Print a message and newline.
        """

        if not log.enable:
            return

        print(message)
