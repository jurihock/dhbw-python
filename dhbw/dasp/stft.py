import numpy

from numpy.lib.stride_tricks import sliding_window_view


def stft(x, framesize, hopsize):

    frames = sliding_window_view(x, framesize, writeable=False)[::hopsize]

    M, N = frames.shape

    data = numpy.zeros((M, N//2+1), complex)

    w = 0.5 - 0.5 * numpy.cos(2 * numpy.pi * numpy.arange(framesize) / framesize)

    for i, frame in enumerate(frames):

        data[i] = numpy.fft.rfft(w * frame, norm='forward')

    return data


def istft(frames, framesize, hopsize):

    M, N = frames.shape

    y = numpy.zeros((M * hopsize + framesize), float)

    data = sliding_window_view(y, framesize, writeable=True)[::hopsize]

    w = 0.5 - 0.5 * numpy.cos(2 * numpy.pi * numpy.arange(framesize) / framesize)

    w *= hopsize / numpy.sum(w**2)  # force unity gain

    for i, frame in enumerate(frames):

        data[i] += w * numpy.fft.irfft(frame, norm='forward')

    return y
