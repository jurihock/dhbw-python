import numpy

from dhbw import dasp


def window(name, size):
    """Returns coefficients of the specified window and size."""

    if 'rectangular'.startswith(name.lower()):
        return numpy.ones(size)

    if 'bartlett'.startswith(name.lower()):
        return numpy.bartlett(size)

    if 'blackman'.startswith(name.lower()):
        return numpy.blackman(size)

    if 'hamming'.startswith(name.lower()):
        return numpy.hamming(size)

    if 'hanning'.startswith(name.lower()):
        return numpy.hanning(size)

    if 'kaiser'.startswith(name.lower()):
        return numpy.kaiser(size, 14)

    raise Exception(f'Invalid or unsupported window "{name}"!')


def ft(x, window='hanning'):
    """Returns DFT of the specified real-valued array
       below the Nyquist frequency."""

    n = len(x)  # actual length
    m = dasp.math.pot(n)  # power of two length

    if window is not None:
        x = x * dasp.fft.window(window, n)

    dft = numpy.fft.rfft(x, n=m)[:-1] / m  # skip nyquist and normalize

    return dft


def abs(x, y, db=True, window='hanning'):
    """Returns DFT frequencies and corresponding absolute values
       of the specified timeline x and signal amplitudes y.
       Alternatively specify the sample rate instead of the timeline x."""

    sr = x if numpy.isscalar(x) \
           else int(len(x) / numpy.ptp(x))  # 1 / (duration / samples)

    dft = dasp.fft.ft(y, window=window)

    freqs = numpy.linspace(0, sr / 2, len(dft))
    power = dasp.math.abs(dft, db=db)

    return freqs, power


def arg(x, y, unwrap=True, window='hanning'):
    """Returns DFT frequencies and corresponding angle values
       of the specified timeline x and signal amplitudes y.
       Alternatively specify the sample rate instead of the timeline x."""

    sr = x if numpy.isscalar(x) \
           else int(len(x) / numpy.ptp(x))  # 1 / (duration / samples)

    dft = dasp.fft.ft(y, window=window)

    freqs = numpy.linspace(0, sr / 2, len(dft))
    phase = dasp.math.arg(dft, unwrap=unwrap)

    return freqs, phase


def stft(x, y, s, t, window='hanning', wola=False, crop=True):

    sr = x if numpy.isscalar(x) \
           else int(len(x) / numpy.ptp(x))  # 1 / (duration / samples)

    n = len(y)  # total input samples
    s = int(s * sr)  # samples per hop
    t = dasp.math.even(t * sr)  # samples per frame
    w = dasp.fft.window(window, t)  # window coefficients

    if wola:
        w /= numpy.sqrt(numpy.dot(w, w) / s)  # optionally prepare for wola

    frames = []  # frames to be extracted
    hops = [i * s for i in range(n // s)]  # hop indices

    for h in hops:

        # optionally skip too short fragments
        # at the end of the input
        if crop and (h+t) > y.size:
            continue

        frame = y[h:h+t]  # extract next frame

        if crop:
            assert frame.size == t  # check frame size
        else:
            frame = numpy.pad(frame, (0, t - frame.size))  # pad right to expected frame size

        frame = frame * w  # apply window
        frame = numpy.pad(frame, (dasp.math.pot(frame.size) - frame.size) // 2)  # pad left and right to pot
        frame = numpy.roll(frame, frame.size // 2)  # center frame data
        frame = dasp.fft.ft(frame, window=None)  # compute dft without window
        frames.append(frame)  # append to frame buffer

    hops = hops[:len(frames) - len(hops) if len(hops) > len(frames) else len(hops)]  # remove cropped hops
    frames = numpy.stack(frames)  # stack frames vertically (hop, dft)
    timestamps = numpy.array([h / sr for h in hops])  # compute hop timestamps in seconds
    frequencies = numpy.linspace(0, sr / 2, frames.shape[-1])  # compute dft frequencies

    assert (timestamps.size == frames.shape[0])
    assert (frequencies.size == frames.shape[1])

    return frames, timestamps, frequencies
