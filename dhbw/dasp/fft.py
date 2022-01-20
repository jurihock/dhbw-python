import numpy

from dhbw import dasp


def transform(x):

    n = len(x)  # actual length
    m = dasp.math.next_power_of_two(n)  # power of two length

    window = numpy.hanning(n)
    dft = numpy.fft.rfft(x * window)[:-1] / m  # skip nyquist and normalize

    return dft


def abs(x, y, db=True):

    fs = x if numpy.isscalar(x) \
           else int(len(x) / numpy.ptp(x))  # 1 / (duration / samples)

    dft = transform(y)

    frequencies = numpy.linspace(0, fs / 2, len(dft))
    power = dasp.math.abs(dft, db=db)

    return frequencies, power


def arg(x, y, unwrap=True):

    fs = x if numpy.isscalar(x) \
           else int(len(x) / numpy.ptp(x))  # 1 / (duration / samples)

    dft = transform(y)

    frequencies = numpy.linspace(0, fs / 2, len(dft))
    power = dasp.math.arg(dft, unwrap=unwrap)

    return frequencies, power
