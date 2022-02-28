import numpy
import os
import subprocess
import sys
import wave

from dhbw import dasp


def open(path, cmd='audacity', shell=False, wait=False):
    """
    Executes custom command with specified .wav file path as an argument.

    Parameters
    ----------
    path : string
        File path with or without the .wav extension.
    cmd : string
        Command to execute, e.g. audacity (https://www.audacityteam.org).
    shell : bool
        If true, the command will be executed through the shell.
    wait : bool
        If true, wait for child process to terminate.
    """

    if path.startswith('~'):
        path = os.path.expanduser(path)

    if not path.lower().endswith('.wav'):
        path += '.wav'

    process = subprocess.Popen([cmd, path], shell=shell)

    if wait:
        return process.wait()
    else:
        return process.pid


def play(path, cmd='play', shell=False, wait=True):
    """
    Executes custom command with specified .wav file path as an argument.

    Parameters
    ----------
    path : string
        File path with or without the .wav extension.
    cmd : string
        Command to execute, e.g. play (http://sox.sourceforge.net).
    shell : bool
        If true, the command will be executed through the shell.
    wait : bool
        If true, wait for child process to terminate.
    """

    return open(path, cmd=cmd, shell=shell, wait=wait)


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
    sr : integer
        Sample rate in hertz.
    """

    if path.startswith('~'):
        path = os.path.expanduser(path)

    if not path.lower().endswith('.wav'):
        path += '.wav'

    with wave.open(path, 'rb') as file:
        sr = file.getframerate()
        bytes = file.getsampwidth()
        channels = file.getnchannels()
        data = file.readframes(file.getnframes())

    dasp.log.echo(f'Reading data from file {path} {dict(sr=sr, bytes=bytes, channels=channels, n=len(data))}')

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

    time = dasp.timeline(len(data) / sr, sr=sr)
    data = data[:len(time), ...]
    data = data.flatten() if channels == 1 else data

    return data, time, sr


def write(path, data, sr=None, bits=24):
    """
    Writes a .wav file.

    Parameters
    ----------
    path : string
        File path with or without the .wav extension.
    data : ndarray
        Content of the .wav file.
    sr : integer, optional
        Sample rate in hertz.
    bits : integer, optional
        Sample bitwidth.
    """

    sr = sr if sr is not None else dasp.SR

    if path.startswith('~'):
        path = os.path.expanduser(path)

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

    dasp.log.echo(f'Writing data to file {path} {dict(sr=sr, bytes=bytes, channels=channels, n=len(data))}')

    with wave.open(path, 'wb') as file:
        file.setframerate(sr)
        file.setsampwidth(bytes)
        file.setnchannels(channels)
        file.writeframes(data)
