import numpy
import scipy.signal

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


def response(b, a, n=None, sr=None):
    """Returns impulse response of the transfer function specified by b and a coefficients."""

    assert isinstance(n, (int, type(None)))
    assert isinstance(sr, (int, float, type(None)))

    sr = sr if sr is not None else dasp.SR
    n = n or sr

    x = [1] * (n > 0) + [0] * (n - 1)
    y = scipy.signal.lfilter(b, a, x)

    t = numpy.arange(0, n / sr, 1 / sr)

    return y, t


def frequency(b, a, n=None, sr=None, log=False):
    """Returns frequency response of the transfer function specified by b and a coefficients.
       See also: scipy.signal.freqz"""

    assert isinstance(n, (int, type(None)))
    assert isinstance(sr, (int, float, type(None)))

    sr = sr if sr is not None else dasp.SR
    n = n or int(sr / 2)

    # compute frequencies from 0 to pi or sr/2 but excluding the Nyquist frequency
    w = numpy.linspace(0, numpy.pi, n, endpoint=False) \
        if not log else \
        numpy.logspace(numpy.log10(1), numpy.log10(numpy.pi), n, endpoint=False, base=10)

    # compute the z-domain transfer function
    z = numpy.exp(-1j * w)
    x = numpy.polynomial.polynomial.polyval(z, a, tensor=False)
    y = numpy.polynomial.polynomial.polyval(z, b, tensor=False)
    h = y / x

    # normalize frequencies according to sr
    w = (w * sr) / (2 * numpy.pi)

    return h, w
