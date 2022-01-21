from . import fft
from . import filter
from . import io
from . import math
from . import plot
from . import signal

import click
import numpy


FS = 44100  # default sample rate in hertz


def timeline(duration, fs=FS):
    """
    Returns an array of numbers representing a
    discrete timeline of the specified duration in seconds
    and sample rate in hertz which defaults to 44100 Hz.

    Parameters
    ----------
    duration : int, float
        Total timeline length in seconds.
    fs : int, float, optional
        Sample rate in hertz.
    """

    return numpy.arange(0, duration, 1 / fs)


class log:
    """
    Basic logger for package internal purposes.
    """

    enable = False

    def echo(what):

        if log.enable: click.echo(what)
        else: pass
