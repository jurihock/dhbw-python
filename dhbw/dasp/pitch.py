import numpy

from dhbw import dasp


C0 = 2 ** (-(9 + 4*12) / 12)


def scale():
    """
    Returns the `12` chromatic tone names.
    """

    return ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']


def note(semitone):
    """
    Returns note name for the specified semitone index.

    Parameters
    ----------
    semitone : int
        Semitone index in range `[0..12)` or multiple of `12`.
    """

    assert isinstance(semitone, int)

    return scale()[semitone % 12]


def tone(notename):
    """
    Returns semitone index for the specified note name.

    Parameters
    ----------
    notename : str
        Scale note name.
    """

    assert isinstance(notename, str)

    return scale().index(notename.upper())


def frequency(semitone, octave=None, cp=None):
    """
    Returns frequency in hertz for the specified semitone index.

    Parameters
    ----------
    semitone : int
        Semitone index in range `[0..12)` or multiple of `12`.
    octave : int, optional
        Octave index.
    cp : float, optional
        Concert pitch in hertz.
    """

    assert isinstance(semitone, int)
    assert isinstance(octave, int)

    cp = cp if cp is not None else dasp.CP

    c0 = dasp.pitch.C0 * cp

    return 2 ** (semitone / 12 + octave or 0) * c0


def octave(frequency, cp=None):
    """
    Returns octave index of the specified frequency value.

    Parameters
    ----------
    frequency : float
        Frequency in hertz.
    cp : float, optional
        Concert pitch in hertz.
    """

    cp = cp if cp is not None else dasp.CP

    c0 = dasp.pitch.C0 * cp

    return round(12 * numpy.log2(frequency / c0)) // 12


def semitone(frequency, relative=False, cp=None):
    """
    Returns semitone index of the specified frequency value.

    Parameters
    ----------
    frequency : float
        Frequency in hertz.
    relative : bool
        Compute relative semitone index in range `[0..12)` or multiple of `12`.
    cp : float, optional
        Concert pitch in hertz.
    """

    cp = cp if cp is not None else dasp.CP

    c0 = dasp.pitch.C0 * cp

    if relative:
        return round(12 * numpy.log2(frequency / c0)) % 12
    else:
        return round(12 * numpy.log2(frequency / c0))
