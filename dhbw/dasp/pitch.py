import numpy

from dhbw import dasp


C0 = 2 ** (-(9 + 4*12) / 12)


def scale():

    return ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']


def note(semitone):

    return scale()[semitone % 12]


def frequency(semitone, octave=None, cp=None):

    cp = cp if cp is not None else dasp.CP

    c0 = dasp.pitch.C0 * cp

    return 2 ** (semitone / 12 + octave or 0) * c0


def octave(frequency, cp=None):

    cp = cp if cp is not None else dasp.CP

    c0 = dasp.pitch.C0 * cp

    return round(12 * numpy.log2(frequency / c0)) // 12


def semitone(frequency, relative=False, cp=None):

    cp = cp if cp is not None else dasp.CP

    c0 = dasp.pitch.C0 * cp

    if relative:
        return round(12 * numpy.log2(frequency / c0)) % 12
    else:
        return round(12 * numpy.log2(frequency / c0))
