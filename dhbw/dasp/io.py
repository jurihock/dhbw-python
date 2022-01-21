import numpy
import sys
import wave

from dhbw import dasp


def read(path):
    """
    Reads a .wav file.

    Parameters
    ----------
    path : string
        File path with or without the .wav extension.

    Returns
    -------
    data : ndarray
        Content of the .wav file.
    time : ndarray
        Corresponding timeline array.
    fs : integer
        Sample rate in hertz.
    """

    if not path.lower().endswith('.wav'):
        path += '.wav'

    with wave.open(path, 'rb') as file:
        fs = file.getframerate()
        bytes = file.getsampwidth()
        channels = file.getnchannels()
        data = file.readframes(file.getnframes())

    dasp.log.echo(f'Reading data from file {path} {dict(fs=fs, bytes=bytes, channels=channels, fn=len(data))}')

    assert bytes in [1, 2, 3, 4]
    bits = bytes * 8
    scaler = 2 ** (bits - 1) - 1

    data = numpy.frombuffer(data, dtype=numpy.uint8).reshape(-1, bytes)
    data = numpy.asarray([
        int.from_bytes(frame, signed=(bits != 8), byteorder=sys.byteorder)
        for frame in data])
    data = data.astype(float).reshape(-1, channels)

    data -= 128 if bits == 8 else 0  # to signed 8bit
    data = (data + 0.5) / (scaler + 0.5)
    data = data.clip(-1, +1)

    time = dasp.timeline(len(data) / fs, fs=fs)
    data = data[:len(time), ...]
    data = data.flatten() if channels == 1 else data

    return data, time, fs


def write(path, data, fs=None, bits=24):
    """
    Writes a .wav file.

    Parameters
    ----------
    path : string
        File path with or without the .wav extension.
    data : ndarray
        Content of the .wav file.
    fs : integer, optional
        Sample rate in hertz.
    bits : integer, optional
        Sample bitwidth.
    """

    fs = fs if fs is not None else dasp.FS

    if not path.lower().endswith('.wav'):
        path += '.wav'

    data = numpy.asarray(data)
    assert data.dtype in [float, complex]
    assert data.ndim in [1, 2]
    assert data.size > 0

    if numpy.iscomplex(data).any():
        assert data.ndim == 1
        data = numpy.stack((numpy.real(data), numpy.imag(data)))

    if data.ndim == 2:
        if data.shape[0] == 2:
            channels = data.shape[0]
            data = data.ravel('F')
        else:
            channels = data.shape[1]
            data = data.ravel('C')
    else:
        channels = 1

    assert bits in [8, 16, 24, 32]
    bytes = bits // 8
    scaler = 2 ** (bits - 1) - 1

    data = data.clip(-1, +1)
    data = (data * (scaler + 0.5)) - 0.5
    data += 128 if bits == 8 else 0  # to unsigned 8bit

    data = b''.join([
        int(frame).to_bytes(length=bytes, signed=(bits != 8), byteorder=sys.byteorder)
        for frame in data])

    dasp.log.echo(f'Writing data to file {path} {dict(fs=fs, bytes=bytes, channels=channels, fn=len(data))}')

    with wave.open(path, 'wb') as file:
        file.setframerate(fs)
        file.setsampwidth(bytes)
        file.setnchannels(channels)
        file.writeframes(data)
