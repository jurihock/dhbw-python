import numpy


def is_power_of_two(x):
    """Returns True if the specified number is power of two otherwise False."""

    assert isinstance(x, int)
    return (x != 0) and (x & (x - 1) == 0)


def next_power_of_two(x):
    """Returns power of two value next to the specified number."""

    assert isinstance(x, int)
    return int(2 ** numpy.ceil(numpy.log2(x)))


def abs(x, db=True):
    """Returns the absolute value of the specified complex number sequence."""

    return 20 * numpy.log10(numpy.abs(x)) \
        if db else numpy.abs(x)


def arg(x, unwrap=True):
    """Returns the angle value of the specified complex number sequence."""

    return numpy.unwrap(numpy.angle(x)) \
        if unwrap else numpy.angle(x)
