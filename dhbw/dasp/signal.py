import numpy
import scipy.stats


def harmonic(f, t):
    """
    Returns a sine wave of the specified frequency.

    Parameters
    ----------
    f : float
        Signal frequency in hertz.
    t : array
        Timeline array.
    """

    return numpy.sin(2 * numpy.pi * f * t)


def harmonics(f, n, t):
    """
    Returns a harmonic wave including the specified amount of overtones.

    Parameters
    ----------
    f : float
        Fundamental signal frequency in hertz.
    n : int
        Number of additional overtones.
    t : array
        Timeline array.
    """

    assert isinstance(n, int)

    n = numpy.abs(n)
    m = numpy.arange(1, n + 2)
    a = 1 / m
    o = [a[i - 1] * harmonic(f * i, t) for i in m]

    return numpy.stack(o).sum(axis=0) / numpy.sum(a)


def square(f, t):
    """
    Returns a square shaped wave of the specified frequency.

    Parameters
    ----------
    f : float
        Signal frequency in hertz.
    t : array
        Timeline array.
    """

    return numpy.sign(harmonic(f, t))


def sawtooth(f, t):
    """
    Returns a sawtooth shaped wave of the specified frequency.

    Parameters
    ----------
    f : float
        Signal frequency in hertz.
    t : array
        Timeline array.
    """

    return 2 * (f * t - numpy.floor(f * t + 0.5))


def triangle(f, t):
    """
    Returns a triangle shaped wave of the specified frequency.

    Parameters
    ----------
    f : float
        Signal frequency in hertz.
    t : array
        Timeline array.
    """

    return 2 * numpy.abs(sawtooth(f, t)) - 1


def chirp(f0, f1, t):
    """
    Returns a chirp signal in which the frequency alterates over the time.

    Parameters
    ----------
    f0 : float
        Start signal frequency in hertz.
    f1 : float
        End signal frequency in hertz.
    t : array
        Timeline array.
    """

    return numpy.sin(2 * numpy.pi * ((t ** 2) * (f1 - f0) / 2) + t * f0)


def noise(t, s=1):
    """
    Returns a random white noise based on the truncated normal distribution.

    Parameters
    ----------
    t : array
        Timeline array.
    s : float, optional
        Scale parameter between 0 and 1.
    """

    a = -1 / s
    b = +1 / s
    n = len(t)

    return scipy.stats.truncnorm(a, b, loc=0, scale=s).rvs(n)
