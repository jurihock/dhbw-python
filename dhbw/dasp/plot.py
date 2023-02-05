"""
Collection of plot functions.
Each function returns an instance of this module.
"""

import matplotlib.pyplot as plotpy
import numpy
import os
import sys

from dhbw import dasp


def exit():
    """
    Exit from Python.
    """

    sys.exit()


def save(path, size=None, dpi=None):
    """
    Save current figure to specified image file.

    Parameters
    ----------
    path : str
        Output image file path.
    size : tuple, optional
        Output image size (w, h) in inches.
    dpi : int, optional
        Output image resolution in dots per inch.
    """

    assert isinstance(path, str)
    assert isinstance(size, (tuple, type(None)))
    assert isinstance(dpi, (int, type(None)))

    if path.startswith('~'):
        path = os.path.expanduser(path)

    figure = plotpy.gcf()

    origin = figure.get_size_inches()

    if size is not None:
        figure.set_size_inches(size, forward=True)

    if dpi is not None:
        figure.savefig(path, dpi=dpi)
    else:
        figure.savefig(path)

    if size is not None:
        figure.set_size_inches(origin, forward=True)

    return dasp.plot


def show(*args, **kwargs):
    """
     Display all open figures.
    """

    plotpy.show(*args, **kwargs)
    return dasp.plot


def tight(*args, **kwargs):
    """
    Adjust the padding between and around subplots.
    """

    plotpy.tight_layout(*args, **kwargs)
    return dasp.plot


def figure(*args, **kwargs):
    """
    Create a new figure.
    """

    plotpy.figure(*args, **kwargs)
    return dasp.plot


def plot(*args, **kwargs):
    """
    Plot y versus x.
    """

    plotpy.plot(*args, **kwargs)
    return dasp.plot


def signal(x, y=None, xlim=None, ylim=1.1):
    """
    Plot one or multiple audio signals.

    Parameters
    ----------
    x : array or same as y
        Timeline array if y is not None.
    y : array, tuple or list of arrays, optional
        Audio signal(s) to plot, e.g. mono (y) or stereo (y0, y1).
    xlim : float, tuple, optional
        Time limits.
    ylim : float, tuple, optional
        Amplitude limits.
    """

    def lim():

        if xlim is not None:
            if isinstance(xlim, (list, tuple)):
                plotpy.xlim(xlim)
            else:
                plotpy.xlim(0, xlim)

        if ylim is not None:
            if isinstance(ylim, (list, tuple)):
                plotpy.ylim(ylim)
            else:
                plotpy.ylim(-ylim, +ylim)

    if y is None:

        assert x is not None
        y = x
        x = None

    if isinstance(y, dict):
        axes = []
        for i, (k, v) in enumerate(y.items()):
            axes += [plotpy.gcf().add_subplot(len(y), 1, i + 1, title=k)]
            if x is not None:
                plotpy.plot(x, v)
            else:
                plotpy.plot(v)
            lim()
        if len(axes) > 1:
            axes[0].get_shared_x_axes().join(*axes)
            axes[0].get_shared_y_axes().join(*axes)
    elif isinstance(y, (list, tuple)):
        axes = []
        for i, v in enumerate(y):
            axes += [plotpy.gcf().add_subplot(len(y), 1, i + 1)]
            if x is not None:
                plotpy.plot(x, v)
            else:
                plotpy.plot(v)
            lim()
        if len(axes) > 1:
            axes[0].get_shared_x_axes().join(*axes)
            axes[0].get_shared_y_axes().join(*axes)
    else:
        if x is not None:
            plotpy.plot(x, y)
        else:
            plotpy.plot(y)
        lim()

    if x is not None:

        plotpy.xlabel('s')

    return dasp.plot


def spectrogram(x, y, s, t, xlim=None, ylim=None, clim=-120, cmap='inferno', **kwargs):
    """
    Plot STFT amplitude of the audio signal.

    Parameters
    ----------
    x : array
        Timeline array.
    y : array
        Signal amplitude array.
    s : float
        STFT step size in seconds.
    t : float
        STFT time span in seconds.
    xlim : float, tuple, optional
        Time limits.
    ylim : float, tuple, optional
        STFT frequency limits in Hz.
    clim : float, tuple, optional
        STFT amplitude limits in dB.
    cmap : str, optional
        Plot color map.
    """

    def lim():

        if xlim is not None:
            if isinstance(xlim, (list, tuple)):
                plotpy.xlim(xlim)
            else:
                plotpy.xlim(0, xlim)

        if ylim is not None:
            if isinstance(ylim, (list, tuple)):
                plotpy.ylim(ylim)
            else:
                plotpy.ylim(0, ylim)

        if clim is not None:
            if isinstance(clim, (list, tuple)):
                plotpy.clim(clim)
            else:
                plotpy.clim(clim, 0)

    sr = x if numpy.isscalar(x) \
           else int(len(x) / numpy.ptp(x))  # 1 / (duration / samples)

    fs = int(t * sr)  # compute framesize in samples
    hs = int(s * sr)  # compute hopsize in samples

    s = dasp.stft.stft(y, fs, hs)
    s = dasp.math.abs(s, db=True)

    t = numpy.array([h * hs / sr for h in range(s.shape[0])])  # compute hop timestamps in seconds
    f = numpy.fft.rfftfreq(fs, 1 / sr)  # compute dft frequencies in hertz

    # prefer real coordinates to indices (left, right, bottom, top)
    extent = (numpy.min(t), numpy.max(t), numpy.min(f), numpy.max(f))

    plotpy.imshow(s.T, aspect='auto', cmap=cmap, extent=extent, interpolation='nearest', origin='lower')
    colorbar = plotpy.colorbar()

    plotpy.xlabel('s')
    plotpy.ylabel('Hz')
    colorbar.set_label('dB')

    lim()

    return dasp.plot


def phasogram(x, y, s, t, xlim=None, ylim=None, clim=None, cmap='twilight', **kwargs):
    """
    Plot STFT phase of the audio signal.

    Parameters
    ----------
    x : array
        Timeline array.
    y : array
        Signal amplitude array.
    s : float
        STFT step size in seconds.
    t : float
        STFT time span in seconds.
    xlim : float, tuple, optional
        Time limits.
    ylim : float, tuple, optional
        STFT frequency limits in Hz.
    clim : float, tuple, optional
        STFT phase value limits in dB.
    cmap : str, optional
        Plot color map.
    """

    def lim():

        if xlim is not None:
            if isinstance(xlim, (list, tuple)):
                plotpy.xlim(xlim)
            else:
                plotpy.xlim(0, xlim)

        if ylim is not None:
            if isinstance(ylim, (list, tuple)):
                plotpy.ylim(ylim)
            else:
                plotpy.ylim(0, ylim)

        if clim is not None:
            if isinstance(clim, (list, tuple)):
                plotpy.clim(clim)
            else:
                plotpy.clim(-clim, +clim)
        else:
            plotpy.clim(-numpy.pi, +numpy.pi)

    sr = x if numpy.isscalar(x) \
           else int(len(x) / numpy.ptp(x))  # 1 / (duration / samples)

    fs = int(t * sr)  # compute framesize in samples
    hs = int(s * sr)  # compute hopsize in samples

    s = dasp.stft.stft(y, fs, hs)
    s = dasp.math.arg(s, wrap=True)

    t = numpy.array([h * hs / sr for h in range(s.shape[0])])  # compute hop timestamps in seconds
    f = numpy.fft.rfftfreq(fs, 1 / sr)  # compute dft frequencies in hertz

    # prefer real coordinates to indices (left, right, bottom, top)
    extent = (numpy.min(t), numpy.max(t), numpy.min(f), numpy.max(f))

    plotpy.imshow(s.T, aspect='auto', cmap=cmap, extent=extent, interpolation='nearest', origin='lower')
    colorbar = plotpy.colorbar()

    plotpy.xlabel('s')
    plotpy.ylabel('Hz')
    colorbar.set_label('rad')

    lim()

    return dasp.plot


class fft:

    def abs(x, y, xlim=None, ylim=-120, **kwargs):
        """
        Plot DFT amplitude of the audio signal.

        Parameters
        ----------
        x : array
            Timeline array.
        y : array
            Signal amplitude array.
        xlim : float, tuple, optional
            Frequency limits in Hz.
        ylim : float, tuple, optional
            DFT amplitude limits in dB.
        """

        def lim():

            if xlim is not None:
                if isinstance(xlim, (list, tuple)):
                    plotpy.xlim(xlim)
                else:
                    plotpy.xlim(0, xlim)

            if ylim is not None:
                if isinstance(ylim, (list, tuple)):
                    plotpy.ylim(ylim)
                else:
                    plotpy.ylim(ylim, 0)

        assert x is not None
        assert y is not None

        if isinstance(y, dict):
            for i, (k, v) in enumerate(y.items()):
                plotpy.gcf().add_subplot(len(y), 1, i + 1, title=k)
                f, a = dasp.fft.abs(x, v, **kwargs)
                plotpy.plot(f, a)
                plotpy.ylabel('dB')
                lim()
        elif isinstance(y, (list, tuple)):
            for i, v in enumerate(y):
                plotpy.gcf().add_subplot(len(y), 1, i + 1)
                f, a = dasp.fft.abs(x, v, **kwargs)
                plotpy.plot(f, a)
                plotpy.ylabel('dB')
                lim()
        else:
            f, a = dasp.fft.abs(x, y, **kwargs)
            plotpy.plot(f, a)
            plotpy.ylabel('dB')
            lim()

        plotpy.xlabel('Hz')

        return dasp.plot

    def arg(x, y, xlim=None, ylim=None, **kwargs):
        """
        Plot DFT phase of the audio signal.

        Parameters
        ----------
        x : array
            Timeline array.
        y : array
            Signal amplitude array.
        xlim : float, tuple, optional
            Frequency limits in Hz.
        ylim : float, tuple, optional
            DFT phase value limits.
        """

        def lim():

            if xlim is not None:
                if isinstance(xlim, (list, tuple)):
                    plotpy.xlim(xlim)
                else:
                    plotpy.xlim(0, xlim)

            if ylim is not None:
                if isinstance(ylim, (list, tuple)):
                    plotpy.ylim(ylim)
                else:
                    plotpy.ylim(+ylim, -ylim)

        assert x is not None
        assert y is not None

        if isinstance(y, dict):
            for i, (k, v) in enumerate(y.items()):
                plotpy.gcf().add_subplot(len(y), 1, i + 1, title=k)
                f, a = dasp.fft.arg(x, v, **kwargs)
                plotpy.plot(f, a)
                plotpy.ylabel('rad')
                lim()
        elif isinstance(y, (list, tuple)):
            for i, v in enumerate(y):
                plotpy.gcf().add_subplot(len(y), 1, i + 1)
                f, a = dasp.fft.arg(x, v, **kwargs)
                plotpy.plot(f, a)
                plotpy.ylabel('rad')
                lim()
        else:
            f, a = dasp.fft.arg(x, y, **kwargs)
            plotpy.plot(f, a)
            plotpy.ylabel('rad')
            lim()

        plotpy.xlabel('Hz')

        return dasp.plot


class filter:

    def impulse(b, a, clip=1e3, xlim=None, ylim=None, **kwargs):
        """
        Plot impulse response of the transfer function specified by b and a coefficients.

        Parameters
        ----------
        b : array
            The numerator coefficient array.
        a : array
            The denominator coefficient array.
        clip : float, optional
            Clip response amplitudes outside the specified interval.
        xlim : float, tuple, optional
            Time limits.
        ylim : float, tuple, optional
            Amplitude limits.
        """

        def lim():

            if xlim is not None:
                if isinstance(xlim, (list, tuple)):
                    plotpy.xlim(xlim)
                else:
                    plotpy.xlim(0, xlim)

            if ylim is not None:
                if isinstance(ylim, (list, tuple)):
                    plotpy.ylim(ylim)
                else:
                    plotpy.ylim(-ylim, +ylim)

        x, y = dasp.filter.impulse(b, a, **kwargs)

        if isinstance(clip, (list, tuple)):
            y = numpy.clip(y, clip[0], clip[1])
        elif clip is not None:
            y = numpy.clip(y, -clip, +clip)

        plotpy.stem(x, y)
        plotpy.xlabel('s')
        plotpy.ylabel('')

        lim()

        return dasp.plot

    def frequency(b, a, xlim=None, ylim=None, **kwargs):
        """
        Plot frequency response of the transfer function specified by b and a coefficients.

        Parameters
        ----------
        b : array
            The numerator coefficient array.
        a : array
            The denominator coefficient array.
        xlim : float, tuple, optional
            Frequency limits in Hz.
        ylim : float, tuple, optional
            Amplitude value limits in dB.
        """

        def lim():

            if xlim is not None:
                if isinstance(xlim, (list, tuple)):
                    plotpy.xlim(xlim)
                else:
                    plotpy.xlim(0, xlim)

            if ylim is not None:
                if isinstance(ylim, (list, tuple)):
                    plotpy.ylim(ylim)
                else:
                    plotpy.ylim(ylim, 0)

        x, y = dasp.filter.response(b, a, **kwargs)

        plotpy.plot(x, dasp.math.abs(y, db=True))
        plotpy.xlabel('Hz')
        plotpy.ylabel('dB')

        lim()

        return dasp.plot

    def phase(b, a, xlim=None, ylim=None, **kwargs):
        """
        Plot phase response of the transfer function specified by b and a coefficients.

        Parameters
        ----------
        b : array
            The numerator coefficient array.
        a : array
            The denominator coefficient array.
        xlim : float, tuple, optional
            Frequency limits in Hz.
        ylim : float, tuple, optional
            Phase value limits in rad.
        """

        def lim():

            if xlim is not None:
                if isinstance(xlim, (list, tuple)):
                    plotpy.xlim(xlim)
                else:
                    plotpy.xlim(0, xlim)

            if ylim is not None:
                if isinstance(ylim, (list, tuple)):
                    plotpy.ylim(ylim)
                else:
                    plotpy.ylim(-ylim, +ylim)
            else:
                plotpy.ylim(-numpy.pi, +numpy.pi)

        x, y = dasp.filter.response(b, a, **kwargs)

        plotpy.plot(x, dasp.math.arg(y, wrap=True))
        plotpy.xlabel('Hz')
        plotpy.ylabel('rad')

        lim()

        return dasp.plot

    def poleszeros(b, a):
        """
        Plot poles and zeros in Z plane for the transfer function specified by b and a coefficients.

        Parameters
        ----------
        b : array
            The numerator coefficient array.
        a : array
            The denominator coefficient array.
        """

        # https://gist.github.com/endolith/4625838

        p = dasp.filter.poles(b, a)
        z = dasp.filter.zeros(b, a)

        c = plotpy.Circle((0, 0), radius=1, linestyle=':', linewidth=1, color='black', fill=False, alpha=0.3)
        r = numpy.amax(numpy.concatenate((numpy.abs(p), numpy.abs(z), [1]))) + 0.1

        axis = plotpy.gca()

        axis.add_patch(c)
        axis.axvline(0, linestyle=':', linewidth=1, color='black', alpha=0.3)
        axis.axhline(0, linestyle=':', linewidth=1, color='black', alpha=0.3)

        if len(p):
            axis.plot(p.real, p.imag, 'x', markersize=10, color='red', alpha=0.7, label='Pole')

        if len(z):
            axis.plot(z.real, z.imag, 'o', markersize=10, color='none', markeredgecolor='blue', alpha=0.7, label='Zero')

        axis.legend()
        axis.set_xlabel('Re(z)')
        axis.set_ylabel('Im(z)')

        axis.axis('scaled')
        axis.axis([-r, +r, -r, +r])

        return dasp.plot
