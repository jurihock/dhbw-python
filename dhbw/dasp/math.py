import numpy


def db(x):
    """
    Converts the specified value into decibel scale.

    Parameters
    ----------
    x : array
        Input array to be converted.
    """

    with numpy.errstate(divide='ignore', invalid='ignore'):
        return 20 * numpy.log10(x)


def wrap(x):
    """
    Wraps the specified phase value into 2*pi range.

    Parameters
    ----------
    x : array
        Input phase values to be wrapped.
    """

    # https://stackoverflow.com/questions/15927755

    return (x + numpy.pi) % (2 * numpy.pi) - numpy.pi


def unwrap(x):
    """
    Unwraps the specified phase value.

    Parameters
    ----------
    x : array
        Input phase values to be unwrapped.
    """

    # https://stackoverflow.com/questions/15927755

    return numpy.unwrap(x)


def abs(x, db=True):
    """
    Returns the absolute value of the specified complex number sequence.

    Parameters
    ----------
    x : array
        Input array.
    db : bool, optional
        Option whether to express the output values in decibels.
    """

    with numpy.errstate(divide='ignore', invalid='ignore'):
        return 20 * numpy.log10(numpy.abs(x)) \
            if db else numpy.abs(x)


def arg(x, wrap=None):
    """
    Returns the angle value of the specified complex number sequence.

    Parameters
    ----------
    x : array
        Input array.
    wrap : bool, optional
        Option whether to express the output values in 2*pi range.
    """

    if wrap is None:
        return numpy.angle(x)

    if wrap:
        return (numpy.angle(x) + numpy.pi) % (2 * numpy.pi) - numpy.pi
    else:
        return numpy.unwrap(numpy.angle(x))


def even(x):
    """
    Returns even number next to the specified number.

    Parameters
    ----------
    x : int, float
        Input number.
    """

    return int(numpy.ceil(x / 2)) * 2


def odd(x):
    """
    Returns odd number next to the specified number.

    Parameters
    ----------
    x : int, float
        Input number.
    """

    return int(numpy.ceil(x)) // 2 * 2 + 1


def pot(x):
    """
    Returns power of two value next to the specified number.

    Parameters
    ----------
    x : int
        Input number.
    """

    assert isinstance(x, int)
    return int(2 ** numpy.ceil(numpy.log2(x)))


def rms(x):
    """
    Returns Root Mean Square value of the specified number sequence.

    Parameters
    ----------
    x : array
        Input array.
    """

    return numpy.sqrt(numpy.mean(x**2))
