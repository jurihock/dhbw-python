import numpy
import scipy.stats


def noise(s, t):

    a = -1 / s
    b = +1 / s
    n = len(t)

    crv = scipy.stats.truncnorm(a, b, loc=0, scale=s)
    return crv.rvs(n)


def harmonic(f, t):

    return numpy.sin(2 * numpy.pi * f * t)


def square(f, t):

    return numpy.sign(harmonic(f, t))


def sawtooth(f, t):

    return 2 * (f * t - numpy.floor(f * t + 0.5))


def triangle(f, t):

    return 2 * numpy.abs(sawtooth(f, t)) - 1


def chirp(f0, f1, t):

    return numpy.sin(2 * numpy.pi * ((t ** 2) * (f1 - f0) / 2) + t * f0)

def overtones(f, n, t):

    m = numpy.arange(1, n + 2)
    a = 1 / m
    o = [a[i - 1] * harmonic(f * i, t) for i in m]

    return numpy.stack(o).sum(axis=0) / numpy.sum(a)
