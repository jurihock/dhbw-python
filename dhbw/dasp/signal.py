import numpy


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
