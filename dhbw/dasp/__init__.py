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
    """Returns a timeline of the specified duration in seconds
       and sample rate in hertz which defaults to 44100 Hz."""

    return numpy.arange(0, duration, 1 / fs)


class log:

    enable = False

    def echo(what):

        if log.enable: click.echo(what)
        else: pass
