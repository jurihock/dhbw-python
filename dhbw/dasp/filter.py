import numpy
import scipy.signal

from dhbw import dasp


def poles(b, a):
    """
    Returns poles of the transfer function specified by b and a coefficients.

    Parameters
    ----------
    b : array
        The numerator coefficient array.
    a : array
        The denominator coefficient array.

    Returns
    -------
    p : array
        Poles of the transfer function.

    See also
    --------
        scipy.signal.tf2zpk
    """

    a = numpy.array(a) / a[0]  # normalize by a0
    p = numpy.polynomial.polynomial.polyroots(a)

    return p


def zeros(b, a):
    """
    Returns zeros of the transfer function specified by b and a coefficients.

    Parameters
    ----------
    b : array
        The numerator coefficient array.
    a : array
        The denominator coefficient array.

    Returns
    -------
    z : array
        Zeros of the transfer function.

    See also
    --------
        scipy.signal.tf2zpk
    """

    b = numpy.array(b) / a[0]  # normalize by a0
    z = numpy.polynomial.polynomial.polyroots(b)

    return z


def impulse(b, a, n=None, sr=None):
    """
    Returns impulse response of the transfer function specified by b and a coefficients.

    Parameters
    ----------
    b : array
        The numerator coefficient array.
    a : array
        The denominator coefficient array.
    n : int, optional
        Optional number of samples.
    sr : int, float, optional
        Optional sample rate in hertz.

    Returns
    -------
    t : array
        Corresponding time values.
    y : array
        Filter impulse response values.

    See also
    --------
        scipy.signal.lfilter
    """

    assert isinstance(n, (int, type(None)))
    assert isinstance(sr, (int, float, type(None)))

    sr = sr if sr is not None else dasp.SR
    n = n or sr

    x = numpy.array([1] * (n > 0) + [0] * (n - 1), dtype=float)
    y = scipy.signal.lfilter(b, a, x)

    t = numpy.arange(0, n / sr, 1 / sr)

    return t, y


def response(b, a, n=None, sr=None, norm=False, log=False):
    """
    Returns frequency and phase response of the transfer function specified by b and a coefficients.

    Parameters
    ----------
    b : array
        The numerator coefficient array.
    a : array
        The denominator coefficient array.
    n : int, optional
        Optional number of samples.
    sr : int, float, optional
        Optional sample rate in hertz.
    norm : bool
        Option whether to normalize the output frequency response.
    log : bool
        Option whether to express the output frequency values logarithmically.

    Returns
    -------
    w : array
        Corresponding frequency values.
    h : array
        Complex filter response values.

    See also
    --------
        scipy.signal.freqz
    """

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

    # normalize frequency amplitudes
    h /= len(h) if norm else 1

    # normalize frequency values according to sr
    w = (w * sr) / (2 * numpy.pi)

    return w, h
