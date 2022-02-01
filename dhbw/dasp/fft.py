import numpy
import numpy as np

from dhbw import dasp


def window(name, size):
    """
    Returns coefficients of the specified window and size.

    Parameters
    ----------
    name : string
        Window function name (rectangular, bartlett, blackman, hamming, hanning, kaiser).
    size : int
        Number of window coefficients to compute.
    """

    assert isinstance(name, str)
    assert isinstance(size, int)

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


def ft(x, norm=True, window='hanning'):
    """
    Returns DFT of the specified real-valued array excluding the DC component,
    so that the size of the resulting array will be exactly `dasp.math.pot(len(x)) / 2`.

    Parameters
    ----------
    x : array
        Real input array.
    norm : bool, optional
        Option whether to scale the output array by `1/N`.
    window : str, optional
        Window name.

    Returns
    -------
    y : array
        Complex output array of length `dasp.math.pot(len(x)) / 2`.
    """

    n = len(x)  # actual length
    m = dasp.math.pot(n)  # power of two length

    if window is not None:
        x = x * dasp.fft.window(window, n)

    y = numpy.fft.rfft(x, n=m)
    y /= len(y) if norm else 1  # normalize
    y = y[1:]  # skip dc component

    return y


def ift(x, norm=True):
    """
    Returns IDFT of the specified complex-valued array with inserted DC component.

    Parameters
    ----------
    x : array
        Complex input array of length `len(x) == dasp.math.pot(len(x))` without DC component.
    norm : bool, optional
        Option whether to scale the output array by `1*N`.

    Returns
    -------
    y : array
        Real output array of length `dasp.math.pot(len(x)) * 2`.
    """

    x = np.concatenate(([0 + 0j], x))  # prepend dc component skipped in ft
    x *= len(x) if norm else 1  # denormalize
    y = numpy.fft.irfft(x)

    return y


def abs(x, y, db=True, window='hanning'):
    """
    Returns DFT frequencies and corresponding absolute values
    of the specified timeline x and signal amplitudes y.

    Alternatively specify the sample rate instead of the timeline x.

    Parameters
    ----------
    x : array or float
        Timeline or sample rate.
    y : array
        Input signal amplitudes.
    db : bool, optional
        Express frequencies in decibel.
    window : str, optional
        Window name.

    Returns
    -------
    freqs : array
        Frequency array.
    power : array
        Corresponding absolute values.
    """

    sr = x if numpy.isscalar(x) \
           else int(len(x) / numpy.ptp(x))  # 1 / (duration / samples)

    dft = dasp.fft.ft(y, window=window)

    freqs = numpy.linspace(0, sr / 2, len(dft))
    power = dasp.math.abs(dft, db=db)

    return freqs, power


def arg(x, y, wrap=None, window='hanning'):
    """
    Returns DFT frequencies and corresponding argument values
    of the specified timeline x and signal amplitudes y.

    Alternatively specify the sample rate instead of the timeline x.

    Parameters
    ----------
    x : array or float
        Timeline or sample rate.
    y : array
        Input signal amplitudes.
    wrap : bool, optional
        Explicitly wrap or unwrap argument values.
    window : str, optional
        Window name.

    Returns
    -------
    freqs : array
        Frequency array.
    phase : array
        Corresponding argument values.
    """

    sr = x if numpy.isscalar(x) \
           else int(len(x) / numpy.ptp(x))  # 1 / (duration / samples)

    dft = dasp.fft.ft(y, window=window)

    freqs = numpy.linspace(0, sr / 2, len(dft))
    phase = dasp.math.arg(dft, wrap=wrap)

    return freqs, phase


def stft(x, y, s, t, window='hanning', wola=False, crop=True, debug=False):
    """
    Computes STFT matrix.

    Parameters
    ----------
    x : array or float
        Timeline or sample rate.
    y : array
        Input signal amplitudes.
    s : float
        STFT step hop in seconds.
    t : float
        STFT time span in seconds.
    window : bool, optional
        Window name.
    wola : bool, optional
        Perform WOLA weighting.
    crop : bool, optional
        Skip the last hop if the input array is too short.
    debug : bool, optional
        Visualize STFT hop processing.

    Returns
    -------
    frames : matrix
        STFT matrix (hop, dft).
    timestamps : array
        Hop timestamps.
    frequencies : array
        DFT frequencies.
    """

    def show(hop, hops, step, steps, data):

        if not debug:
            return

        if data.dtype == numpy.complex:
            data = dasp.math.abs(data, db=True)

        dasp.plot.figure(f'STFT Hop {hop}/{hops} Step {step}/{steps}').plot(data).show()

    sr = x if numpy.isscalar(x) \
           else int(len(x) / numpy.ptp(x))  # 1 / (duration / samples)

    s = max(1, int(s * sr))  # samples per hop
    t = dasp.math.even(t * sr)  # samples per frame
    n = len(y)  # total input samples

    assert s > 0
    assert t > 0
    assert n > 0

    w = dasp.fft.window(window, t)  # window coefficients
    w /= numpy.sqrt(numpy.dot(w, w) / s) if wola else 1  # optionally prepare for wola

    frames = []  # frames to be extracted
    hops = [i * s for i in range(n // s)]  # hop indices

    for i, h in enumerate(hops):

        # optionally skip too short fragments
        # at the end of the input
        if crop and (h+t) > y.size:
            continue

        frame = y[h:h+t]  # extract next frame
        show(i + 1, len(hops), 1, 5, frame)

        if crop:
            assert frame.size == t  # check frame size
        else:
            frame = numpy.pad(frame, (0, t - frame.size))  # pad right to expected frame size

        frame = frame * w  # apply window
        show(i + 1, len(hops), 2, 5, frame)

        frame = numpy.pad(frame, (dasp.math.pot(frame.size) - frame.size) // 2)  # pad left and right to pot
        show(i + 1, len(hops), 3, 5, frame)

        frame = numpy.roll(frame, frame.size // 2)  # center frame data
        show(i + 1, len(hops), 4, 5, frame)

        frame = dasp.fft.ft(frame, window=None)  # compute dft without window
        show(i + 1, len(hops), 5, 5, frame)

        frames.append(frame)  # append to frame buffer

    hops = hops[:len(frames) - len(hops) if len(hops) > len(frames) else len(hops)]  # remove cropped hops
    frames = numpy.stack(frames)  # stack frames vertically (hop, dft)
    timestamps = numpy.array([h / sr for h in hops])  # compute hop timestamps in seconds
    frequencies = numpy.linspace(0, sr / 2, frames.shape[-1])  # compute dft frequencies

    assert (timestamps.size == frames.shape[0])
    assert (frequencies.size == frames.shape[1])

    return frames, timestamps, frequencies


def istft(x, y, s, t, window='hanning', wola=False, debug=False):
    """
    Synthesizes STFT matrix.

    Parameters
    ----------
    x : array or float
        Timeline or sample rate of the original signal (not hop timestamps).
    y : array
        STFT matrix (hop, dft).
    s : float
        ISTFT hop size in seconds.
    t : float
        ISTFT time span in seconds.
    window : bool, optional
        Window name.
    wola : bool, optional
        Perform WOLA weighting.
    debug : bool, optional
        Visualize ISTFT hop processing.

    Returns
    -------
    frames : array
        Synthesized output signal.
    """

    def show(hop, hops, step, steps, data):

        if not debug:
            return

        if data.dtype == numpy.complex:
            data = dasp.math.abs(data, db=True)

        dasp.plot.figure(f'ISTFT Hop {hop}/{hops} Step {step}/{steps}').plot(data).show()

    sr = x if numpy.isscalar(x) \
           else int(len(x) / numpy.ptp(x))  # 1 / (duration / samples)

    s = max(1, int(s * sr))  # samples per hop
    t = dasp.math.even(t * sr)  # samples per frame
    n = len(y) * s + t  # total output samples

    assert s > 0
    assert t > 0
    assert n > 0

    w = dasp.fft.window(window, t)  # window coefficients
    w /= numpy.sqrt(numpy.dot(w, w) / s) if wola else 1  # optionally prepare for wola

    frames = np.zeros(n)  # frames to be extracted
    hops = [i * s for i in range(len(y))]  # hop indices

    for i, h in enumerate(hops):

        frame = y[i]  # extract next frame
        show(i + 1, len(hops), 1, 5, frame)

        frame = dasp.fft.ift(frame)  # compute idft
        show(i + 1, len(hops), 2, 5, frame)

        frame = numpy.roll(frame, frame.size // 2)  # center frame data
        show(i + 1, len(hops), 3, 5, frame)

        frame = numpy.roll(frame, (t - frame.size) // 2)[:t]  # crop to t
        show(i + 1, len(hops), 4, 5, frame)

        frame = frame * w  # apply window
        show(i + 1, len(hops), 5, 5, frame)

        frames[h:h+t] += frame  # append to frame buffer

    return frames
