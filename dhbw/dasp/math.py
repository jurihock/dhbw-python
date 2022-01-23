import numpy


def abs(x, db=True):
    """
    Returns the absolute value of the specified complex number sequence.

    Parameters
    ----------
    x : array_like
        Input array.
    db : bool, optional
        Option whether to express the output values in decibels.
    """

    return 20 * numpy.log10(numpy.abs(x)) \
        if db else numpy.abs(x)


def arg(x, unwrap=True):
    """
    Returns the angle value of the specified complex number sequence.

    Parameters
    ----------
    x : array_like
        Input array.
    unwrap : bool, optional
        Option whether to express the output values in 2*pi range.
    """

    return numpy.unwrap(numpy.angle(x)) \
        if unwrap else numpy.angle(x)


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
