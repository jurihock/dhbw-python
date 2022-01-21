import numpy

from dhbw import dasp


def transform(x):
    """Returns DFT of the specified real-valued array
       below the Nyquist frequency."""

    n = len(x)  # actual length
    m = dasp.math.next_power_of_two(n)  # power of two length

    win = numpy.hanning(n)  # since an audio signal is expected
    dft = numpy.fft.rfft(x * win, n=m)[:-1] / m  # skip nyquist and normalize

    return dft


def abs(x, y, db=True):
    """Returns DFT frequencies and corresponding absolute values
       of the specified timeline x and signal amplitudes y.
       Alternatively specify the sample rate instead of the timeline x."""

    fs = x if numpy.isscalar(x) \
           else int(len(x) / numpy.ptp(x))  # 1 / (duration / samples)

    dft = transform(y)

    freqs = numpy.linspace(0, fs / 2, len(dft))
    power = dasp.math.abs(dft, db=db)

    return freqs, power


def arg(x, y, unwrap=True):
    """Returns DFT frequencies and corresponding angle values
       of the specified timeline x and signal amplitudes y.
       Alternatively specify the sample rate instead of the timeline x."""

    fs = x if numpy.isscalar(x) \
           else int(len(x) / numpy.ptp(x))  # 1 / (duration / samples)

    dft = transform(y)

    freqs = numpy.linspace(0, fs / 2, len(dft))
    phase = dasp.math.arg(dft, unwrap=unwrap)

    return freqs, phase
