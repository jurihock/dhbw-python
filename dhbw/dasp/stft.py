import numpy

from numpy.lib.stride_tricks import sliding_window_view


def stft(samples, framesize, hopsize):
    """
    Estimate the DFT matrix for the given sample array.

    Parameters
    ----------
    samples : ndarray, list, float
        Array of samples.

    Returns
    -------
    dfts : ndarray
        DFT matrix of shape (samples,frequencies).
    """

    samples = numpy.atleast_1d(samples)

    assert samples.ndim == 1, f'Expected 1D array (samples,), got {samples.shape}!'

    frames = sliding_window_view(samples, framesize, writeable=False)[::hopsize]
    dfts = numpy.zeros((len(frames), len(numpy.fft.rfftfreq(framesize))), complex)

    w = 0.5 - 0.5 * numpy.cos(2 * numpy.pi * numpy.arange(framesize) / framesize)

    for i, frame in enumerate(frames):

        dfts[i] = numpy.fft.rfft(w * frame, norm='forward')

    return dfts


def istft(dfts, framesize, hopsize):
    """
    Synthesize the sample array from the given DFT matrix.

    Parameters
    ----------
    dfts : ndarray
        DFT matrix of shape (samples,frequencies).

    Returns
    -------
    samples : ndarray
        Array of samples.
    """

    dfts = numpy.atleast_2d(dfts)

    assert dfts.ndim == 2, f'Expected 2D array (samples,frequencies), got {dfts.shape}!'

    samples = numpy.zeros((len(dfts) * hopsize + framesize), float)
    frames = sliding_window_view(samples, framesize, writeable=True)[::hopsize]

    w = 0.5 - 0.5 * numpy.cos(2 * numpy.pi * numpy.arange(framesize) / framesize)
    w *= hopsize / numpy.sum(w**2)  # unity gain

    for i, dft in enumerate(dfts):

        frames[i] += w * numpy.fft.irfft(dft, norm='forward')

    return samples
