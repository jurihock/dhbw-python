from . import fft
from . import filter
from . import io
from . import math
from . import plot
from . import signal

import click
import numpy


SR = 44100  # default sample rate in hertz


def timeline(duration, sr=None):
    """
    Returns an array of numbers representing a
    discrete timeline of the specified duration in seconds
    and sample rate in hertz which defaults to 44100 Hz.

    Parameters
    ----------
    duration : int, float
        Total timeline length in seconds.
    sr : int, float, optional
        Sample rate in hertz.
    """

    sr = sr if sr is not None else SR

    return numpy.arange(0, duration, 1 / sr)


class log:
    """
    Basic logger for package internal purposes.
    """

    enable = False

    def echo(what):

        if log.enable: click.echo(what)
        else: pass
