import numpy
import scipy

from dhbw import dasp


def poles(b, a):
    """Returns poles of the transfer function specified by b and a coefficients.
       See also: scipy.signal.tf2zpk"""

    a = numpy.array(a) / a[0]  # normalize by a0
    p = numpy.polynomial.polynomial.polyroots(a)

    return p


def zeros(b, a):
    """Returns zeros of the transfer function specified by b and a coefficients.
       See also: scipy.signal.tf2zpk"""

    b = numpy.array(b) / a[0]  # normalize by a0
    z = numpy.polynomial.polynomial.polyroots(b)

    return z


def impulse(b, a, n=10):
    i = numpy.zeros(n)
    i[0] = 1

    o = scipy.signal.lfilter(b, a, i)

    return o


def frequency(b, a, fs=None, fn=1024, log=False):
    """Returns frequency response of the transfer function specified by b and a coefficients.
       See also: scipy.signal.freqz"""

    fs = fs if fs is not None else dasp.FS

    # compute frequencies from 0 to pi or fs/2 but excluding the Nyquist frequency
    w = numpy.linspace(0, numpy.pi, fn, endpoint=False) \
        if not log else \
        numpy.logspace(numpy.log10(1), numpy.log10(numpy.pi), fn, endpoint=False, base=10)

    # compute the z-domain transfer function
    z = numpy.exp(-1j * w)
    x = numpy.polynomial.polynomial.polyval(z, a, tensor=False)
    y = numpy.polynomial.polynomial.polyval(z, b, tensor=False)
    h = y / x

    # normalize frequencies according to fs
    w = (w * fs) / (2 * numpy.pi)

    return w, h
