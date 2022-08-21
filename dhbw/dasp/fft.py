import numpy

from dhbw import dasp


def window(name, size):
    """
    Returns coefficients of the specified window and size.

    Parameters
    ----------
    name : string
        Window function name (rectangular, bartlett, blackman, hamming, hanning, kaiser).
    size : int
        Number of window coefficients to compute.
    """

    # TODO https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.windows.get_window.html

    assert isinstance(name, str)
    assert isinstance(size, int)

    if 'rectangular'.startswith(name.lower()):
        return numpy.ones(size)

    if 'bartlett'.startswith(name.lower()):
        return numpy.bartlett(size)

    if 'blackman'.startswith(name.lower()):
        return numpy.blackman(size)

    if 'hamming'.startswith(name.lower()):
        return numpy.hamming(size)

    if 'hanning'.startswith(name.lower()):
        return numpy.hanning(size)

    if 'kaiser'.startswith(name.lower()):
        return numpy.kaiser(size, 14)

    raise Exception(f'Invalid or unsupported window "{name}"!')


def fft(x, norm=True, window='hanning'):
    """
    Returns DFT of the specified real-valued array excluding the Nyquist component,
    so that the size of the resulting array will be exactly `dasp.math.pot(len(x)) / 2`.

    Parameters
    ----------
    x : array
        Real input array.
    norm : bool, optional
        Option whether to scale the output array by `1/N`.
    window : str, optional
        Window name.

    Returns
    -------
    y : array
        Complex output array of length `dasp.math.pot(len(x)) / 2`.
    """

    n = len(x)  # actual length
    m = dasp.math.pot(n)  # power of two length

    if window is not None:
        x = x * dasp.fft.window(window, n)

    y = numpy.fft.rfft(x, n=m, norm=('forward' if norm else 'backward'))
    y = y[:-1]  # skip Nyquist component

    return y


def ifft(x, norm=True):
    """
    Returns IDFT of the specified complex-valued array with inserted Nyquist component.

    Parameters
    ----------
    x : array
        Complex input array of length `len(x) == dasp.math.pot(len(x))` without Nyquist component.
    norm : bool, optional
        Option whether to scale the output array by `1*N`.

    Returns
    -------
    y : array
        Real output array of length `dasp.math.pot(len(x)) * 2`.
    """

    x = numpy.concatenate((x, [0]))  # append Nyquist component skipped in ft
    y = numpy.fft.irfft(x, norm=('forward' if norm else 'backward'))

    return y


def abs(x, y, db=True, window='hanning'):
    """
    Returns DFT frequencies and corresponding absolute values
    of the specified timeline x and signal amplitudes y.

    Alternatively specify the sample rate instead of the timeline x.

    Parameters
    ----------
    x : array or float
        Timeline or sample rate.
    y : array
        Input signal amplitudes.
    db : bool, optional
        Express frequencies in decibel.
    window : str, optional
        Window name.

    Returns
    -------
    freqs : array
        Frequency array.
    power : array
        Corresponding absolute values.
    """

    sr = x if numpy.isscalar(x) \
           else int(len(x) / numpy.ptp(x))  # 1 / (duration / samples)

    dft = dasp.fft.fft(y, window=window)

    freqs = numpy.linspace(0, sr / 2, len(dft))
    power = dasp.math.abs(dft, db=db)

    return freqs, power


def arg(x, y, wrap=None, window='hanning'):
    """
    Returns DFT frequencies and corresponding argument values
    of the specified timeline x and signal amplitudes y.

    Alternatively specify the sample rate instead of the timeline x.

    Parameters
    ----------
    x : array or float
        Timeline or sample rate.
    y : array
        Input signal amplitudes.
    wrap : bool, optional
        Explicitly wrap or unwrap argument values.
    window : str, optional
        Window name.

    Returns
    -------
    freqs : array
        Frequency array.
    phase : array
        Corresponding argument values.
    """

    sr = x if numpy.isscalar(x) \
           else int(len(x) / numpy.ptp(x))  # 1 / (duration / samples)

    dft = dasp.fft.fft(y, window=window)

    freqs = numpy.linspace(0, sr / 2, len(dft))
    phase = dasp.math.arg(dft, wrap=wrap)

    return freqs, phase
